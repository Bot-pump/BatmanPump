import requests
import os

APIFY_TOKEN = os.getenv("APIFY_TOKEN")

def fetch_tokens(chain=None):
    url = f"https://api.apify.com/v2/acts/muhammetakkurtt~gmgn-new-pair-scraper/run-sync-get-dataset-items?token={APIFY_TOKEN}"

    try:
        print("[DEBUG] Fetching tokens from gmgn.ai via Apify...")
        response = requests.get(url, timeout=30)
        print(f"[DEBUG] Status Code: {response.status_code}")
        data = response.json()
        tokens = []

        for item in data:
            name = item.get("name")
            symbol = item.get("symbol")
            price = item.get("price_usd", "0.00")
            url = item.get("chart_url", "#")

            if name and symbol:
                tokens.append({
                    "name": name,
                    "symbol": symbol,
                    "price": price,
                    "url": url
                })

        print(f"[INFO] Total tokens from gmgn.ai: {len(tokens)}")
        return tokens

    except Exception as e:
        print("[ERROR] Failed to fetch tokens from gmgn.ai:", e)
        return []
