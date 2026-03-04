import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://www.bbc.com"
START_URL = "https://www.bbc.com/news"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(START_URL, headers=headers)
soup = BeautifulSoup(response.text, "lxml")

# STEP 1: Collect article links
article_links = set()

for a in soup.find_all("a", href=True):
    href = a["href"]

    if href.startswith("/news/") and "live" not in href:
        full_link = BASE_URL + href
        article_links.add(full_link)

print("Total article links found:", len(article_links))

# STEP 2: Scrape articles
data = []

for link in list(article_links)[:10]:  # limit to 10
    print("Scraping:", link)

    try:
        article_response = requests.get(link, headers=headers)
        article_soup = BeautifulSoup(article_response.text, "lxml")

        headline = article_soup.find("h1")
        paragraphs = article_soup.find_all("p")

        if not headline or len(paragraphs) < 3:
            continue

        article_text = " ".join(p.text for p in paragraphs)

        data.append({
            "headline": headline.text.strip(),
            "text": article_text.strip(),
            "source": "BBC",
            "url": link
        })

        time.sleep(2)

    except Exception as e:
        print("Error:", e)

# STEP 3: Save to CSV
df = pd.DataFrame(data)
df.to_csv("live_news.csv", index=False)

print("\nSaved", len(df), "articles to live_news.csv")

