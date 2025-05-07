# 🕷️ Screaming Frog Automation Suite

This project automates website crawling using the **Screaming Frog SEO Spider CLI**, processes the results, categorizes URLs, and updates data in **Google Sheets**. It's designed for SEO teams and analysts who need scalable, auditable, and automated crawling workflows.

---

## 📁 Project Structure

| File | Purpose |
|------|---------|
| `main.py` | Full pipeline: crawl → process → categorize → upload to Google Sheets |
| `script.py` | Lightweight script to crawl websites manually |
| `screaming_frog.py` | Function to run Screaming Frog CLI with logging |
| `log_utils.py` | Sets up a rotating logging system based on day |
| `categorize_urls.py` | Contains logic for URL categorization and custom sorting |
| `google_sheets.py` | Handles Google Sheets authentication and data updates |

---

## 🔧 Setup Instructions

### 1. Requirements

- Python 3.7+
- Screaming Frog SEO Spider (CLI enabled)
- Google Sheets API credentials (`credentials.json`)

Install Python dependencies:
```bash
pip install pandas python-dotenv gspread oauth2client
```

### 2. Environment Variables

Create a `.env` file in the root folder:
```env
OUTPUT_DIRECTORY_BASE=/absolute/path/to/output
SCREAMING_FROG_CLI_PATH=/absolute/path/to/screamingfrogseospider
SPREADSHEET_URL=https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID
GOOGLE_SHEETS_CREDENTIALS_JSON=credentials.json
```

---

## 🚀 How to Use

### Option A: Full Automation (`main.py`)
- Add domains in the `websites` dictionary:
```python
websites = {
    "Example": "https://example.com",
    "MySite": "https://mysite.com"
}
```
- Run:
```bash
python main.py
```
- Automatically:
  - Checks for existing CSV
  - Crawls if missing
  - Categorizes URLs (e.g., home, about, contact, blog)
  - Updates relevant sheet tab

### Option B: Simple Batch Crawling (`script.py`)
- Define websites manually
- Set CLI path and output directory
- Run:
```bash
python script.py
```

---

## 🧠 Categorization Logic

`categorize_urls.py` handles:
- Static rules (`/about`, `/contact`, `/blog`)
- Dynamic fallback: uses first path segment
- Custom sort prioritizing homepage, service pages, etc.

---

## 📊 Google Sheets Integration

`google_sheets.py`:
- Connects using Google API credentials
- Automatically creates or updates worksheet tabs per domain
- Uploads crawl data (excluding headers) starting at cell A2

---

## 📂 Logging

`log_utils.py` creates log files organized like:
```
logs/
  Monday/
    2025-05-07_13-45-23.log
```

Each run logs:
- Crawl execution
- Errors
- Google Sheets sync status

---

## ✅ Sample Output Flow

1. Crawl `example.com`
2. Save `internal_all.csv` to `/output/example_com/`
3. Parse and categorize URLs
4. Update Google Sheet tab `example_com` with results
