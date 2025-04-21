import os
import requests

PROXY_URL = os.getenv("PROXY_URL")  # Example: https://dexproxy-xxxxx.onrender.com/proxy

def fetch_tokens(chain):
    target = f"https://token-api.moralis.io/v1/token/new?chain={chain}&limit=10"
    url = f"{PROXY_URL}?url={target}"

    try:
        print(f"[DEBUG] Fetching tokens for chain: {chain}")
        print(f"[DEBUG] Full URL: {url}")

        response = requests.get(url, timeout=10)
        print(f"[DEBUG] Status Code: {response.status_code}")
        print(f"[DEBUG] Raw Response: {response.text}")

        data = response.json()
        tokens = []

        for token in data.get("pairs", []):
            name = token.get("baseToken", {}).get("name", "Unknown")
            symbol = token.get("baseToken", {}).get("symbol", "Unknown")
            price = token.get("priceUsd", "0.00")
            pair_address = token.get("pairAddress", "unknown")

            chart_url = f"https://dexscreener.com/{chain}/{pair_address}"
            print(f"[INFO] New token: {symbol} - ${price} - {chart_url}")

            tokens.append({
                "name": name,
                "symbol": symbol,
                "price": price,
                "url": chart_url
            })

        return tokens
    except Exception as e:
        print(f"[ERROR] Failed to fetch tokens for {chain.upper()}: {e}")
        return []
