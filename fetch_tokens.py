import requests
import os

MORALIS_API_KEY = os.getenv("MORALIS_API_KEY")

HEADERS = {
    "accept": "application/json",
    "X-API-Key": MORALIS_API_KEY
}

def get_tokens(chain):
    url = f"https://token-api.moralis.io/v1/token/new?chain={chain}&limit=10"
    tokens = []

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()

        for token in data.get("tokens", []):
            name = token.get("name", "Unknown")
            symbol = token.get("symbol", "Unknown")
            price = token.get("price_usd", 0)
            dex = token.get("dex_name", "").lower()
            pool_url = token.get("dex_url", "#")

            if chain == "solana" and "pumpswap" not in dex:
                continue
            if chain == "bsc" and "pancakeswap" not in dex:
                continue

            tokens.append({
                "name": name,
                "symbol": symbol,
                "price": price,
                "url": pool_url
            })

    except Exception as e:
        print(f"[{chain.upper()}] Error:", e)

    return tokens