# Nagaland Lottery Result Scraper

This Python script automates the process of fetching the latest Nagaland State Lottery results. It scrapes the official website, downloads the result PDFs, extracts the winning numbers, and saves the data into structured JSON files.

## Features

- Scrapes the lottery website for the latest result PDF links.
- Downloads the PDFs for the Morning, Day, and Evening draws.
- Parses the PDFs to extract draw names and winning numbers.
- Saves the latest results into `json_results/today.json`.
- Appends new results to a historical archive at `json_results/archive.json`.
- Designed to be run automatically via cron jobs or other schedulers.

## Setup

1.  **Prerequisites:**
    - Python 3.6+
    - `pip` for installing packages

2.  **Installation:**
    - Clone this repository or download the files.
    - Install the required Python libraries using the `requirements.txt` file:
      ```bash
      pip install -r requirements.txt
      ```

## Usage

To run the scraper manually, execute the script from your terminal:

```bash
python scraper.py
```

The script will perform the following actions:
- Create a `pdf_results/` directory to store the downloaded PDFs.
- Create a `json_results/` directory.
- Generate `today.json` with the latest fetched results.
- Create or update `archive.json` with the historical data.

## Automation (Cron Job Example)

To automate the script to run at specific times, you can use a cron job on a Linux server. The lottery results are typically released after 1:00 PM, 6:00 PM, and 8:00 PM. You can set up a cron job to run shortly after these times.

1.  Open your crontab for editing:
    ```bash
    crontab -e
    ```

2.  Add lines to schedule the script. For example, to run the script at 1:15 PM, 6:15 PM, and 8:15 PM daily:
    ```cron
    # Note: The path to python and the script must be absolute paths.
    # Use `which python` and `pwd` to find the correct paths.

    15 13 * * * /usr/bin/python3 /path/to/your/project/scraper.py >> /path/to/your/project/cron.log 2>&1
    15 18 * * * /usr/bin/python3 /path/to/your/project/scraper.py >> /path/to/your/project/cron.log 2>&1
    15 20 * * * /usr/bin/python3 /path/to/your/project/scraper.py >> /path/to/your/project/cron.log 2>&1
    ```
    - `15 13 * * *`: Runs at 1:15 PM (13:15) every day.
    - `/usr/bin/python3`: The absolute path to your Python interpreter.
    - `/path/to/your/project/scraper.py`: The absolute path to the scraper script.
    - `>> /path/to/your/project/cron.log 2>&1`: This redirects all output (both stdout and stderr) to a log file, which is useful for debugging.

---
**Disclaimer:** The parsing logic for the PDF is based on its current format and may break if the lottery organizers change the layout of the result sheets. Regular maintenance may be required.
