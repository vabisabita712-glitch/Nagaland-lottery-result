import requests
from bs4 import BeautifulSoup
import pdfplumber
import json
import os
import re
import sys
from datetime import datetime

# --- Configuration ---
BASE_URL = "https://nagalandstatelottery.in/"
PDF_DIR = "pdf_results"
DATA_FILE = "data/archive.json"

# --- Main Functions ---

def get_pdf_url_for_draw(draw_time):
    """
    Scrapes the website to find the PDF URL for a specific draw time ('morning', 'day', 'evening').
    """
    print(f"Searching for {draw_time} draw PDF link...")
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error: Could not fetch website at {BASE_URL}. {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    # Map our internal draw_time to the text found on the website's headings
    draw_map = {
        'morning': '1PM Result',
        'day': '6PM Result',
        'evening': '8PM Result'
    }
    search_text = draw_map.get(draw_time)
    if not search_text:
        print(f"Error: Invalid draw_time '{draw_time}' specified.")
        return None

    section_header = soup.find(['h2', 'h3'], string=re.compile(search_text, re.IGNORECASE))
    if not section_header:
        print(f"Info: Could not find the section for '{search_text}'. It might not be published yet.")
        return None

    pdf_link_tag = section_header.find_next('a', href=re.compile(r'\.pdf$', re.IGNORECASE))
    if pdf_link_tag and pdf_link_tag.get('href'):
        url = pdf_link_tag.get('href')
        print(f"Found PDF URL: {url}")
        return url
    else:
        print(f"Info: Found the '{search_text}' section, but no PDF link was present.")
        return None

def download_pdf(url):
    """
    Downloads a PDF from a URL and saves it to a temporary path.
    """
    if not url:
        return None

    print(f"Downloading PDF from {url}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error: Could not download PDF. {e}")
        return None

    if not os.path.exists(PDF_DIR):
        os.makedirs(PDF_DIR)

    # Use a predictable temporary name
    filepath = os.path.join(PDF_DIR, "latest_result.pdf")
    with open(filepath, 'wb') as f:
        f.write(response.content)

    print(f"Successfully downloaded PDF to {filepath}")
    return filepath

def parse_pdf(pdf_path):
    """
    Parses a downloaded PDF to extract the draw name and 1st prize winning number.
    """
    if not pdf_path:
        return None

    print("Parsing PDF...")
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text(x_tolerance=2, y_tolerance=2)
                if page_text:
                    text += page_text + "\n"

            draw_name_match = re.search(r'DEAR\s+[A-Z]+\s+(?:MORNING|EVENING|DAY)', text, re.IGNORECASE)
            draw_name = draw_name_match.group(0).strip() if draw_name_match else "Unknown Draw"

            prize_match = re.search(r'1st\s+Prize.*?([\w\d]+\s*\d{5})', text, re.IGNORECASE | re.DOTALL)
            winning_number = prize_match.group(1).strip() if prize_match else "Not Found"

            print(f"Parsing complete. Draw: {draw_name}, Number: {winning_number}")
            return {"name": draw_name, "number": winning_number}

    except Exception as e:
        print(f"Error: Could not parse PDF file. {e}")
        return None

def update_archive(draw_time, result_data):
    """
    Updates the archive JSON file with the new result data.
    """
    print("Updating archive file...")
    today_str = datetime.now().strftime("%Y-%m-%d")

    # Ensure data directory exists
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

    archive = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            try:
                archive = json.load(f)
            except json.JSONDecodeError:
                print("Warning: Archive file is corrupted. Starting a new one.")
                archive = []

    # Find today's entry in the archive
    today_entry = next((item for item in archive if item.get('date') == today_str), None)

    if today_entry:
        # Check if this draw time is already recorded for today
        draw_exists = any(draw.get('time') == draw_time.capitalize() for draw in today_entry['draws'])
        if draw_exists:
            print(f"Info: {draw_time} result for {today_str} already exists in archive. Skipping.")
            return
        else:
            # Add the new draw to today's entry
            today_entry['draws'].append({"time": draw_time.capitalize(), **result_data})
    else:
        # Create a new entry for today
        new_entry = {
            "date": today_str,
            "draws": [{"time": draw_time.capitalize(), **result_data}]
        }
        archive.insert(0, new_entry) # Prepend to keep it sorted

    # Write the updated data back to the archive file
    with open(DATA_FILE, 'w') as f:
        json.dump(archive, f, indent=2)

    print("Archive file updated successfully.")

# --- Main Execution ---

def main():
    """
    Main function to orchestrate the scraper.
    """
    if len(sys.argv) != 2 or sys.argv[1] not in ['morning', 'day', 'evening']:
        print("Usage: python lottery_scraper.py [morning|day|evening]")
        sys.exit(1)

    draw_time = sys.argv[1]

    pdf_url = get_pdf_url_for_draw(draw_time)
    if not pdf_url:
        print("Could not find a valid PDF URL. Exiting.")
        return

    pdf_path = download_pdf(pdf_url)
    if not pdf_path:
        print("Could not download the PDF. Exiting.")
        return

    result_data = parse_pdf(pdf_path)
    if not result_data:
        print("Could not parse the PDF. Exiting.")
        return

    update_archive(draw_time, result_data)

    print(f"\nScraping process for {draw_time} draw completed successfully.")

if __name__ == "__main__":
    main()
