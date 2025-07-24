# 🏫 School Profile Scraper

This project is a two-part Python toolset to download and extract detailed school profile information from Niche.com school pages.

## 📁 Project Structure

```
.
├── download.py          # Downloads HTML pages from school URLs
├── scraper.py           # Parses downloaded HTML files for structured data
├── requirements.txt     # Dependencies needed to run the scripts
├── schools.txt          # A text file containing the list of school URLs (not included)
├── downloaded_pages/    # Directory where downloaded HTML files are saved
└── school_results.json  # Output file with all scraped data
```

## 🚀 Setup Instructions

1. **Install Dependencies**

Make sure you have Python 3.7+ installed.

```bash
pip install -r requirements.txt
```

2. **Prepare Input URLs**

Create a file named `schools.txt` in the root directory with school profile URLs separated by commas or new lines.

Example:
```
https://www.niche.com/k12/some-high-school-name-city/
https://www.niche.com/k12/another-school/
```

3. **Download HTML Pages**

Run:

```bash
python download.py
```

This will:
- Read URLs from `schools.txt`
- Download and save each school's HTML page into `downloaded_pages/`

4. **Extract School Data**

After downloading the pages:

```bash
python scraper.py
```

This will:
- Parse all `.html` files in `downloaded_pages/`
- Extract school name, grades, contact info, and more
- Save results in a structured JSON format: `school_results.json`

## ✅ Extracted Fields

For each school, the following data is collected:
- School Name
- Overall Niche Grade
- Academics
- Diversity
- Teachers
- College Prep
- Clubs & Activities
- Administration
- Sports
- Food
- Resources & Facilities
- Website
- Contact
- Address

## 🛠 Requirements

From `requirements.txt`:

```
requests
beautifulsoup4
selenium
webdriver-manager
undetected-chromedriver
```

> *Note: Only `requests` and `beautifulsoup4` are needed for `scraper.py`. Selenium-related packages are unused in the current implementation but can support future automation.*

## 📌 Notes

- The scraper depends on the class names used in Niche.com's HTML structure. If the website changes its layout or class names, `scraper.py` may need to be updated.
- Add random delays in `download.py` to avoid being flagged for aggressive scraping.
