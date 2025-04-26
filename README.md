# 📰 News Scraper Web App (Python)

A simple web application built with **Python (FastAPI)** that extracts news content (title, summary, publish date, full HTML) from any given URL and displays it in a browser-friendly format.

---

## 🚀 Features

- 🔍 Extracts title, publish date, summary & full HTML content
- 💾 Stores extracted data in a database
- 🌐 Frontend to view scraped news
- 📤 Export scraped content to Excel/CSV (coming soon!)
- 🕒 Background crawler (scheduler) support (optional)

---

## 🛠️ Tech Stack

- **Backend**: FastAPI + SQLite
- **Frontend**: HTML + Jinja2 Templates
- **Scraping**: BeautifulSoup, Requests
- **Deployment**: Localhost or any Python hosting

---

## 📦 Setup & Run

```bash
# Clone the repo
git clone https://github.com/venkatesh453/p1-newscraper_web_app_py.git
cd p1-newscraper_web_app_py

# Install dependencies
pip install -r requirements.txt

# Run the app
uvicorn main:app --reload
