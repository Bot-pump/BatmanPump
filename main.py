import os
import time
import requests
import telebot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "@BatmanPump")
PROXY_URL = os.getenv("PROXY_URL")  # رابط السيرفر الوسيط على Replit

bot = telebot.TeleBot(BOT_TOKEN)
sent_tokens = set()

def get_tokens(chain):
    try:
        url = f"{PROXY_URL}/new_tokens/{chain}"
        res = requests.get(url)
        return res.json().get("tokens", [])
    except Exception as e:
        print(f"[{chain.upper()}] Error fetching tokens:", e)
        return []

def send_tokens(chain_name, tokens):
    for token in tokens:
        name = token.get("name", "Unknown")
        symbol = token.get("symbol", "Unknown")
        price = token.get("price", "0.00")
        url = token.get("url", "#")
        unique_key = f"{chain_name}:{symbol}:{price}"

        if unique_key not in sent_tokens:
            msg = f"🚀 *New Token Detected on {chain_name.upper()}*\n\n" \
                  f"*Name:* {name}\n" \
                  f"*Symbol:* {symbol}\n" \
                  f"*Price:* ${price}\n" \
                  f"[Chart]({url})"
            try:
                bot.send_message(CHANNEL_USERNAME, msg, parse_mode="Markdown")
                sent_tokens.add(unique_key)
            except Exception as e:
                print("Telegram Error:", e)

def main_loop():
    while True:
        for chain in ["solana", "ethereum", "bsc", "base"]:
            tokens = get_tokens(chain)
            send_tokens(chain, tokens)
        time.sleep(30)

if __name__ == "__main__":
    try:
        bot.send_message(CHANNEL_USERNAME, "✅ BatmanPump Bot is now running and monitoring new tokens on Solana, Ethereum, BSC, and Base!")
    except Exception as e:
        print("Failed to send startup message:", e)
    
    main_loop()
