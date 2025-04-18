import os
import time
import telebot
from fetch_tokens import fetch_tokens  # Import the token fetch function

# Load environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "@BatmanPump")

bot = telebot.TeleBot(BOT_TOKEN)
sent_tokens = set()

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
                msg = (
                    f"*🚀 New Token Detected on {chain.upper()}*\n\n"
                    f"*Name:* {name}\n"
                    f"*Symbol:* {symbol}\n"
                    f"*Price:* ${price}\n"
                    f"[Chart]({url})"
                )
                try:
                    bot.send_message(CHANNEL_USERNAME, msg, parse_mode="Markdown")
                    sent_tokens.add(key)
                except Exception as e:
                    print("Telegram Error:", e)

# Send a startup message
try:
    bot.send_message(CHANNEL_USERNAME, "✅ BatmanPump Bot is now running and monitoring new tokens on Solana, Ethereum, BSC, and Base!")
except Exception as e:
    print("Failed to send startup message:", e)

# Run every 30 seconds
while True:
    send_new_tokens()
    time.sleep(30)
