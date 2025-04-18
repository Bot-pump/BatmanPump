
import os
import time
import requests
import telebot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "@BatmanPump")
PROXY_URL = os.getenv("PROXY_URL")

bot = telebot.TeleBot(BOT_TOKEN)
sent_tokens = set()

def fetch_tokens(chain):
    url = f"{PROXY_URL}/v1/token/new?chain={chain}&limit=10"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        tokens = []
        for token in data.get("pairs", []):
            name = token.get("baseToken", {}).get("name", "Unknown")
            symbol = token.get("baseToken", {}).get("symbol", "Unknown")
            price = token.get("priceUsd", "0.00")
            url = f"https://dexscreener.com/{chain}/{token.get('pairAddress', '')}"
            tokens.append({
                "name": name,
                "symbol": symbol,
                "price": price,
                "url": url
            })
        return tokens
    except Exception as e:
        print(f"[{chain.upper()}] Error:", e)
        return []

def send_new_tokens():
    chains = ["solana", "bsc", "ethereum", "base"]
    for chain in chains:
        tokens = fetch_tokens(chain)
        for token in tokens:
            name = token["name"]
            symbol = token["symbol"]
            price = token["price"]
            url = token["url"]
            key = f"{symbol}:{price}"
            if key not in sent_tokens:
                msg = f"🚀 *New Token Detected on {chain.upper()}*

*Name:* {name}
*Symbol:* {symbol}
*Price:* ${price}
[Chart]({url})"
                try:
                    bot.send_message(CHANNEL_USERNAME, msg, parse_mode="Markdown")
                    sent_tokens.add(key)
                except Exception as e:
                    print("Telegram Error:", e)

# رسالة ترحيب
try:
    bot.send_message(CHANNEL_USERNAME, "✅ BatmanPump Bot is now running and monitoring new tokens on Solana, Ethereum, BSC, and Base!")
except Exception as e:
    print("Failed to send startup message:", e)

while True:
    send_new_tokens()
    time.sleep(30)
