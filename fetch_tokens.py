import os
import requests

# Get proxy URL from environment variable
PROXY_URL = os.getenv("PROXY_URL")  # Example: https://your-dexproxy.onrender.com/proxy

def fetch_tokens(chain):
    """
    Fetch the latest tokens for a given chain using DexProxy + Moralis API.
    Returns a list of token dictionaries.
    """
    # Prepare target Moralis API URL and wrap it through DexProxy
    target = f"https://token-api.moralis.io/v1/token/new?chain={chain}&limit=10"
    url = f"{PROXY_URL}?url={target}"

    try:
        response = requests.get(url, timeout=10)
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
        print(f"[{chain.upper()}] Error fetching tokens:", e)
        return []
