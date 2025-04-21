import os
import time
import telebot
from fetch_tokens import fetch_tokens

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "@BatmanPump")

bot = telebot.TeleBot(BOT_TOKEN)

def send_all_tokens():
    tokens = fetch_tokens()
    print(f"[DEBUG] Fetched {len(tokens)} tokens (sending all regardless of duplicates).")

    if not tokens:
        try:
            bot.send_message(CHANNEL_USERNAME, "🤖 No tokens received from data source.")
        except Exception as e:
            print("[ERROR] Fallback message failed:", e)
        return

    for token in tokens:
        name = token.get("name", "Unknown")
        symbol = token.get("symbol", "Unknown")
        price = token.get("price", "0.00")
        url = token.get("url", "#")

        msg = (
            f"🚀 *Token from gmgn/pump.fun*

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
            print(f"[SENT] {symbol}")
        except Exception as e:
            print(f"[ERROR] Failed to send {symbol}:", e)

# Startup message
try:
    bot.send_message(CHANNEL_USERNAME, "✅ BatmanPump Unfiltered Mode: All tokens will be sent.")
except Exception as e:
    print("Failed to send startup message:", e)

while True:
    send_all_tokens()
    time.sleep(30)
