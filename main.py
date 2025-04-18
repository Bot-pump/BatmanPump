import os
import time
import requests
import telebot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")
MORALIS_API_KEY = os.getenv("MORALIS_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
sent_tokens = set()

headers = {
    "accept": "application/json",
    "X-API-Key": MORALIS_API_KEY
}

def fetch_tokens(chain):
    url = f"https://token-api.moralis.io/v1/token/new?chain={chain}&limit=10"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get("tokens", [])
        else:
            print(f"[{chain.upper()}] Failed to fetch tokens: {response.status_code}")
    except Exception as e:
        print(f"[{chain.upper()}] Error: {e}")
    return []

def send_token_message(display, token):
    name = token.get("name", "Unknown")
    symbol = token.get("symbol", "Unknown")
    price = token.get("price_usd", "0.00")
    url = f"https://dexscreener.com/token/{token.get('address', '')}"

    unique_key = f"{display}:{symbol}:{price}"
    if unique_key not in sent_tokens:
        msg = f"🚀 *New Token Detected on {display.upper()}*\n\n*Name:* {name}\n*Symbol:* {symbol}\n*Price:* ${price}\n[Chart]({url})"
        try:
            bot.send_message(CHANNEL_USERNAME, msg, parse_mode="Markdown")
            sent_tokens.add(unique_key)
        except Exception as e:
            print(f"Telegram Error: {e}")

def process_chain(chain, display, filter_dex=None):
    tokens = fetch_tokens(chain)
    for token in tokens:
        dex = token.get("dex_name", "").lower()
        if (filter_dex and filter_dex.lower() in dex) or not filter_dex:
            print(f"[{chain.upper()}] Token: {token.get('name')} - {token.get('symbol')} - {dex}")
            send_token_message(display, token)

def start_monitoring():
    try:
        bot.send_message(CHANNEL_USERNAME, "✅ BatmanPump Bot is now running and monitoring new tokens on Solana, Ethereum, BSC, and Base!", parse_mode="Markdown")
    except Exception as e:
        print(f"Failed to send welcome message: {e}")

    while True:
        process_chain("solana", "solana", "pumpswap")
        process_chain("bsc", "bsc", "pancakeswap")
        process_chain("eth", "ethereum")
        process_chain("base", "base")
        time.sleep(30)

if __name__ == "__main__":
    start_monitoring()
