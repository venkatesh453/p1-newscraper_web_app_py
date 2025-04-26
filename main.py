from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup
from db import NewsArticle, Session
from starlette.responses import HTMLResponse
import pandas as pd
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def form_page(request: Request):
    session = Session()
    articles = session.query(NewsArticle).all()
    session.close()
    return templates.TemplateResponse("index.html", {"request": request, "articles": articles})

@app.post("/extract", response_class=HTMLResponse)
async def extract_news(request: Request, url: str = Form(...)):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    # Extract Title
    title_tag = soup.find('h1')
    title = title_tag.text.strip() if title_tag else "No title found"

    # Extract Published Date
    published_date = None
    date_tag = soup.find(lambda tag: tag.name in ['div', 'span'] and tag.text.strip().startswith("Published on:"))
    if date_tag:
        published_date = date_tag.text.strip().replace("Published on:", "").strip()

    # Extract Full Description
    summary = ""
    article_body = soup.find("div", class_="article-content")
    if article_body:
        paragraphs = article_body.find_all("p")
        summary = " ".join(p.get_text(strip=True) for p in paragraphs)
    else:
        paragraphs = soup.find_all("p")
        summary = " ".join(p.get_text(strip=True) for p in paragraphs)

    session = Session()
    article = NewsArticle(
        url=url,
        title=title,
        published_date=published_date,
        summary=summary,
        html_content=res.text
    )
    session.merge(article)
    session.commit()
    session.close()

    return RedirectResponse("/", status_code=303)

@app.get("/export")
async def export_excel():
    session = Session()
    articles = session.query(NewsArticle).all()
    session.close()

    data = [{
        "URL": a.url,
        "Title": a.title,
        "Published Date": a.published_date,
        "Summary": a.summary
    } for a in articles]

    df = pd.DataFrame(data)
    excel_path = "articles.xlsx"
    df.to_excel(excel_path, index=False)

    return FileResponse(excel_path, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename="articles.xlsx")


@app.post("/delete")
async def delete_article(article_id: int = Form(...)):
    session = Session()
    article = session.query(NewsArticle).filter(NewsArticle.id == article_id).first()
    if article:
        session.delete(article)
        session.commit()
    session.close()
    return RedirectResponse("/", status_code=303)