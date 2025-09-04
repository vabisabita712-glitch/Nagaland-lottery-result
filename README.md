# Automated Nagaland Lottery Results Website

This repository contains a complete, automated system for scraping, storing, and displaying Nagaland State Lottery results. The system is composed of two main parts: a backend Python scraper and a static HTML frontend.

## How It Works

1.  **Backend Scraper:** A Python script (`lottery_scraper.py`) is run on a schedule by a GitHub Actions workflow.
2.  The script visits the official lottery website, downloads the latest result PDF, and extracts the winning numbers.
3.  The extracted data is appended to the `data/archive.json` file.
4.  The GitHub Actions workflow detects the change in `data/archive.json` and automatically commits it back to this repository.
5.  **Frontend Website:** A simple, static HTML website reads the `data/archive.json` file to display the results.
6.  When the `archive.json` file is updated by the scraper, hosting platforms like Vercel or Netlify can be configured to automatically redeploy the site, ensuring the results are always up-to-date.

---

## Backend: Python Scraper

The `lottery_scraper.py` script is the engine of this system.

### Setup

1.  **Prerequisites:** Python 3.6+ and `pip`.
2.  **Installation:** Install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```

### Automation

The scraping process is automated by the `.github/workflows/scraper.yml` file. It is configured to run three times a day to fetch the Morning, Day, and Evening results. It will automatically update the `data/archive.json` file in this repository. No manual intervention is needed.

---

## Frontend: HTML Website

The frontend consists of three static pages:
- `index.html`: Displays the results for the most recent day.
- `archive.html`: Displays all historical results from the archive.
- `contact.html`: A simple contact and disclaimer page.

The pages are built with pure HTML and styled with Tailwind CSS via a CDN. They use vanilla JavaScript to dynamically fetch and display the data from `data/archive.json`.

### Viewing Locally

You can open the `.html` files directly in your web browser to view the website. Note that due to browser security policies (CORS), the `fetch()` request for the JSON file may not work when opening the file directly from your local filesystem (`file:///...`). To test it properly locally, you should serve the files with a simple local web server. For example, using Python:

```bash
# From the root of the project, run:
python -m http.server
```
Then open `http://localhost:8000` in your browser.

## Deployment

1.  **Connect to a Host:** Connect this GitHub repository to a static hosting provider like [Vercel](https://vercel.com/) or [Netlify](https://www.netlify.com/).
2.  **Configure Settings:**
    - The default settings should work correctly. Vercel/Netlify will automatically detect that this is a static site (no framework).
    - The build command can be left empty.
    - The publish directory should be the root of the repository.
3.  **Deploy:** After the initial deployment, the site will be live.
4.  **Automatic Updates:** Because the GitHub Action commits data changes directly to the `main` branch, Vercel/Netlify will see this new commit and automatically trigger a new deployment, ensuring your website always displays the latest lottery results.
