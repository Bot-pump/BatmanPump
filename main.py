import os
import time
import requests
import telebot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")
DEX_PROXY_URL = os.getenv("DEX_PROXY_URL")

bot = telebot.TeleBot(BOT_TOKEN)
sent_tokens = set()

def get_tokens():
    try:
        url = f"{DEX_PROXY_URL}/tokens"
        response = requests.get(url)
        data = response.json()
        return data.get("tokens", [])
    except Exception as e:
        print("Error fetching tokens:", e)
        return []

def send_new_tokens():
    tokens = get_tokens()
    for token in tokens:
        name = token.get("name", "Unknown")
        symbol = token.get("symbol", "Unknown")
        price = token.get("price", "0.00")
        url = token.get("url", "#")
        chain = token.get("chain", "Unknown").upper()

        unique_key = f"{symbol}:{price}"
        if unique_key not in sent_tokens:
            msg = f"*New Token Detected on {chain}*

*Name:* {name}
*Symbol:* {symbol}
*Price:* ${price}
[Chart]({url})"
            try:
                bot.send_message(CHANNEL_USERNAME, msg, parse_mode="Markdown")
                sent_tokens.add(unique_key)
                print(f"[SENT] {name} - {symbol} on {chain}")
            except Exception as e:
                print("Telegram Error:", e)

if __name__ == "__main__":
    print("✅ BatmanPump Bot is now running and monitoring new tokens on Solana, Ethereum, BSC, and Base!")
    bot.send_message(CHANNEL_USERNAME, "✅ BatmanPump Bot is now running and monitoring new tokens on Solana, Ethereum, BSC, and Base!")
    while True:
        send_new_tokens()
        time.sleep(30)
