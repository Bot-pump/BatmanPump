import os
import requests

PROXY_URL = os.getenv("PROXY_URL")  # مثل: https://dexproxy-xxxxx.onrender.com/proxy

def fetch_tokens(chain):
    target = f"https://token-api.moralis.io/v1/token/new?chain={chain}&limit=10"
    url = f"{PROXY_URL}?url={target}"

    try:
        response = requests.get(url, timeout=10)
        print(f"[DEBUG] URL: {url}")
        print(f"[DEBUG] STATUS: {response.status_code}")
        print(f"[DEBUG] RESPONSE: {response.text}")

        data = response.json()
        tokens = []

        for token in data.get("pairs", []):
            name = token.get("baseToken", {}).get("name", "Unknown")
            symbol = token.get("baseToken", {}).get("symbol", "Unknown")
            price = token.get("priceUsd", "0.00")
            chart_url = f"https://dexscreener.com/{chain}/{token.get('pairAddress', '')}"

            tokens.append({
                "name": name,
                "symbol": symbol,
                "price": price,
                "url": chart_url
            })

        return tokens
    except Exception as e:
        print(f"[ERROR] Failed fetching from Moralis: {e}")
        return []
