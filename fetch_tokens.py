import requests
import os

APIFY_TOKEN = os.getenv("APIFY_TOKEN")  # Your Apify personal token

def fetch_tokens(chain=None):
    url = f"https://api.apify.com/v2/acts/muhammetakkurtt~gmgn-new-pair-scraper/run-sync-get-dataset-items?token={APIFY_TOKEN}"

    try:
        print("[DEBUG] Fetching tokens from Apify Pump.fun actor...")
        response = requests.get(url, timeout=30)
        print(f"[DEBUG] Status Code: {response.status_code}")
        data = response.json()
        tokens = []

        for token in data:
            base_info = token.get("base_token_info", {})
            name = base_info.get("name")
            symbol = base_info.get("symbol")
            price = base_info.get("price", 0)
            pool_id = base_info.get("pool_id")

            if name and symbol and pool_id and price and float(price) > 0:
                chart_url = f"https://pump.fun/{pool_id}"

                tokens.append({
                    "name": name,
                    "symbol": symbol,
                    "price": price,
                    "url": chart_url
                })

        print(f"[INFO] Total tokens returned: {len(tokens)}")
        return tokens

    except Exception as e:
        print("[ERROR] Failed to fetch tokens from Apify:", e)
        return []
