import os
import time
import telebot
from fetch_tokens import fetch_tokens  # Import Apify-based token fetcher

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "@BatmanPump")

bot = telebot.TeleBot(BOT_TOKEN)
sent_tokens = set()

def send_new_tokens():
    tokens = fetch_tokens()
    for token in tokens:
        name = token["name"]
        symbol = token["symbol"]
        price = token["price"]
        url = token["url"]
        key = f"{symbol}:{price}"

        if key not in sent_tokens:
            msg = (
                f"*🚀 New Token Detected on PUMP.FUN*

"
                f"*Name:* {name}
"
                f"*Symbol:* {symbol}
"
                f"*Price:* ${price}
"
                f"[Chart]({url})"
            )
            try:
                bot.send_message(CHANNEL_USERNAME, msg, parse_mode="Markdown")
                sent_tokens.add(key)
                print(f"[SENT] {symbol} sent to Telegram.")
            except Exception as e:
                print("[ERROR] Telegram sending failed:", e)

# Startup message
try:
    bot.send_message(CHANNEL_USERNAME, "✅ BatmanPump Bot is now monitoring graduated tokens on pump.fun!")
except Exception as e:
    print("Failed to send startup message:", e)

# Loop every 30 seconds
while True:
    send_new_tokens()
    time.sleep(30)
