import requests
from bs4 import BeautifulSoup
import pdfplumber
import json
import os
import re
from datetime import datetime

BASE_URL = "https://nagalandstatelottery.in/"
RESULT_URL_BASE = "https://nagalandstatelotterysambad.com"
PDF_DIR = "pdf_results"
JSON_DIR = "json_results"

def find_pdf_urls():
    """
    Scrapes the Nagaland Lottery website to find the links to today's result PDFs.
    This version is more robust, looking for specific sections for each draw time.
    Returns a dictionary mapping draw time to its full, absolute PDF URL.
    """
    print("Fetching the main website to find PDF links...")
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching website: {e}")
        return {}

    soup = BeautifulSoup(response.content, 'html.parser')
    pdf_links = {}

    # Define the sections to look for
    draw_sections = {
        "1pm": "1PM Result",
        "6pm": "6PM Result",
        "8pm": "8PM Result"
    }

    for key, text in draw_sections.items():
        # Find the heading for the section (e.g., <h2>8PM Result</h2>)
        section_header = soup.find(['h2', 'h3'], string=re.compile(text, re.IGNORECASE))
        if section_header:
            # Find the next 'a' tag after the header, which should be the PDF link
            pdf_link_tag = section_header.find_next('a', href=re.compile(r'\.pdf$', re.IGNORECASE))
            if pdf_link_tag and pdf_link_tag.get('href'):
                relative_url = pdf_link_tag.get('href')
                # Ensure the link is for today. The date check is now implicit
                # as we assume the website updates its main page daily.
                # A more robust check could be added if needed.
                full_url = relative_url if relative_url.startswith('http') else RESULT_URL_BASE + relative_url
                pdf_links[key] = full_url

    print(f"Found PDF links: {pdf_links}")
    return pdf_links

def download_pdf(url, draw_time):
    """
    Downloads a PDF from a URL and saves it locally.
    """
    if not os.path.exists(PDF_DIR):
        os.makedirs(PDF_DIR)

    print(f"Downloading PDF for {draw_time} from {url}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error downloading PDF for {draw_time}: {e}")
        return None

    filename = f"result_{draw_time}_{datetime.now().strftime('%Y%m%d')}.pdf"
    filepath = os.path.join(PDF_DIR, filename)

    with open(filepath, 'wb') as f:
        f.write(response.content)

    print(f"Successfully downloaded {filepath}")
    return filepath

def extract_text_from_pdf(pdf_path):
    """
    Extracts all text from a given PDF file using pdfplumber.
    """
    if not pdf_path:
        return ""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                # Use a layout-aware text extraction
                page_text = page.extract_text(x_tolerance=2, y_tolerance=2)
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return ""
    return text

def parse_text_for_results(text, draw_time_map):
    """
    Parses the raw text from a PDF to find the draw name and 1st prize number.
    This version uses a more robust regex to find the winning number.
    """
    draw_name = "Unknown Draw"
    winning_number = "Not Found"

    # Find draw name (usually in the format "DEAR <NAME> <MORNING/EVENING>")
    name_match = re.search(r'DEAR\s+[A-Z]+\s+(?:MORNING|EVENING|DAY)', text, re.IGNORECASE)
    if name_match:
        draw_name = name_match.group(0).strip()

    # Find the 1st Prize winning number.
    # The pattern looks for "1st Prize", some characters, and then a number
    # in the format of XX 12345 or X12345 etc.
    prize_match = re.search(r'1st\s+Prize.*?([\w\d]+\s*\d{5})', text, re.IGNORECASE | re.DOTALL)
    if prize_match:
        # The winning number is in the second captured group
        winning_number = prize_match.group(1).strip()
    else:
        # Fallback for simpler patterns if the above fails
        simple_match = re.search(r'1st\s+Prize.*?\n.*?(\d{5})', text, re.IGNORECASE | re.DOTALL)
        if simple_match:
            winning_number = simple_match.group(1).strip()

    return {
        "time": draw_time_map.get("time_of_day", "Unknown"),
        "name": draw_name,
        "number": winning_number
    }

def save_today_results(data):
    """Saves the latest results to today.json."""
    if not os.path.exists(JSON_DIR):
        os.makedirs(JSON_DIR)

    filepath = os.path.join(JSON_DIR, "today.json")
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Successfully saved today's results to {filepath}")
    except IOError as e:
        print(f"Error saving today's json: {e}")

def update_archive(data):
    """Appends today's results to the archive.json file if not already present."""
    if not os.path.exists(JSON_DIR):
        os.makedirs(JSON_DIR)

    filepath = os.path.join(JSON_DIR, "archive.json")
    archive_data = []

    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                archive_data = json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            print(f"Could not read or parse archive file. Starting fresh. Error: {e}")
            archive_data = []

    # Check if today's date is already in the archive
    date_exists = any(item.get('date') == data['date'] for item in archive_data)

    if not date_exists:
        archive_data.insert(0, data)
        try:
            with open(filepath, 'w') as f:
                json.dump(archive_data, f, indent=2)
            print(f"Successfully updated archive at {filepath}")
        except IOError as e:
            print(f"Error updating archive json: {e}")
    else:
        print("Today's results are already in the archive. No update needed.")


if __name__ == "__main__":
    urls = find_pdf_urls()
    if not urls:
        print("No result PDFs found for today.")
    else:
        today_results = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "draws": []
        }

        draw_time_mapping = {
            "1pm": {"time_of_day": "Morning"},
            "6pm": {"time_of_day": "Day"},
            "8pm": {"time_of_day": "Evening"}
        }

        for draw_key, url in urls.items():
            pdf_path = download_pdf(url, draw_key)
            if pdf_path:
                text = extract_text_from_pdf(pdf_path)
                if text:
                    print(f"Parsing results for {draw_key}...")
                    result_data = parse_text_for_results(text, draw_time_mapping.get(draw_key, {}))
                    today_results["draws"].append(result_data)
                    print(f"Parsed data: {result_data}")

        if today_results["draws"]:
            save_today_results(today_results)
            update_archive(today_results)
        else:
            print("No new draw data was successfully parsed. JSON files not updated.")
