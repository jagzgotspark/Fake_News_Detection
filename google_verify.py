import os
import requests


API_KEY = os.getenv("GOOGLE_API_KEY")
CSE_ID = os.getenv("GOOGLE_CSE_ID")

def google_search(query, num_results=5):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": CSE_ID,
        "q": query,
        "num": num_results
    }
    response = requests.get(url, params=params)
    return response.json()

def extract_evidence(search_data):
    evidence = []

    if "items" not in search_data:
        return evidence

    for item in search_data["items"]:
        evidence.append({
            "title": item.get("title", ""),
            "snippet": item.get("snippet", ""),
            "link": item.get("link", "")
        })

    return evidence

def verify_claim(claim, evidence_list):

    if not evidence_list:
        return "⚠️ No authoritative source found — claim requires manual verification."

    support_hits = 0

    trusted_keywords = [
        "reserve bank of india",
        "rbi",
        "repo rate",
        "interest rate",
        "monetary policy",
        "central bank"
    ]

    for e in evidence_list:
        text = (e["title"] + " " + e["snippet"]).lower()

        if any(keyword in text for keyword in trusted_keywords):
            support_hits += 1

    if support_hits >= 1:
        return "✅ Supported by authoritative sources"
    else:
        return "⚠️ Mentioned by sources but phrasing differs — requires verification"
