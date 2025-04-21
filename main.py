import os
import time
import telebot
from fetch_tokens import fetch_tokens  # Apify-based token fetcher

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "@BatmanPump")

bot = telebot.TeleBot(BOT_TOKEN)
sent_tokens = set()

def send_new_tokens():
    tokens = fetch_tokens()
    print(f"[DEBUG] Fetched {len(tokens)} tokens.")

    if not tokens:
        try:
            bot.send_message(CHANNEL_USERNAME, "🤖 No new tokens found at the moment.")
        except Exception as e:
            print("[ERROR] Failed to send empty message:", e)
        return

    for token in tokens:
        name = token.get("name", "N/A")
        symbol = token.get("symbol", "N/A")
        price = token.get("price", "0.00")
        url = token.get("url", "#")
        key = f"{symbol}:{price}"

        if key not in sent_tokens:
            msg = (
                f"🚀 *New Token Detected on PUMP.FUN*\n\n"
                f"*Name:* {name}\n"
                f"*Symbol:* {symbol}\n"
                f"*Price:* ${price}\n"
                f"[Chart]({url})"
            )
            try:
                bot.send_message(CHANNEL_USERNAME, msg, parse_mode="Markdown")
                sent_tokens.add(key)
                print(f"[SENT] {symbol} sent to Telegram.")
            except Exception as e:
                print("[ERROR] Telegram sending failed:", e)
        else:
            print(f"[SKIPPED] Already sent: {symbol}")

# Startup message
try:
    bot.send_message(CHANNEL_USERNAME, "✅ BatmanPump Bot is active and watching pump.fun!")
except Exception as e:
    print("Failed to send startup message:", e)

# Run every 30 seconds
while True:
    send_new_tokens()
    time.sleep(30)
