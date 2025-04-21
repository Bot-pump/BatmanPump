import requests
import os

APIFY_TOKEN = os.getenv("APIFY_TOKEN")  # Your Apify personal token

def fetch_tokens(chain=None):
    # chain is unused but kept for compatibility with main bot logic
    url = f"https://api.apify.com/v2/acts/muhammetakkurtt~gmgn-new-pair-scraper/run-sync-get-dataset-items?token={APIFY_TOKEN}"

    try:
        print("[DEBUG] Fetching tokens from Apify Pump.fun actor...")
        response = requests.get(url, timeout=30)
        print(f"[DEBUG] Status Code: {response.status_code}")
        print(f"[DEBUG] Raw Response: {response.text[:500]}")  # Limit output for safety

        data = response.json()
        tokens = []

        for token in data:
            if token.get("status", "").lower() == "graduated":
                name = token.get("name", "Unknown")
                symbol = token.get("symbol", "Unknown")
                price = token.get("price_usd", "0.00")
                url = token.get("chart_url", "#")

                tokens.append({
                    "name": name,
                    "symbol": symbol,
                    "price": price,
                    "url": url
                })

        print(f"[INFO] Total graduated tokens found: {len(tokens)}")
        return tokens

    except Exception as e:
        print("[ERROR] Failed to fetch tokens from Apify:", e)
        return []
