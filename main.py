import os
import time
import telebot
from fetch_tokens import fetch_tokens  # Import token fetcher for gmgn.ai

# Telegram bot and channel configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "@BatmanPump")

bot = telebot.TeleBot(BOT_TOKEN)
sent_tokens = set()

def send_new_tokens():
    tokens = fetch_tokens()
    print(f"[DEBUG] Fetched {len(tokens)} tokens from gmgn.ai")

    if not tokens:
        try:
            bot.send_message(CHANNEL_USERNAME, "🤖 No new tokens found on gmgn.ai.")
        except Exception as e:
            print("[ERROR] Failed to send fallback message:", e)
        return

    for token in tokens:
        name = token.get("name", "N/A")
        symbol = token.get("symbol", "N/A")
        price = token.get("price", "0.00")
        url = token.get("url", "#")
        key = f"{symbol}:{price}"

        if key not in sent_tokens:
            msg = (
                f"🚀 *New Token Detected on gmgn.ai*\\n\\n"
                f"*Name:* {name}\\n"
                f"*Symbol:* {symbol}\\n"
                f"*Price:* ${price}\\n"
                f"[Chart]({url})"
            )
            try:
                bot.send_message(CHANNEL_USERNAME, msg, parse_mode="Markdown")
                sent_tokens.add(key)
                print(f"[SENT] Token {symbol} sent.")
            except Exception as e:
                print("[ERROR] Telegram send failed:", e)
        else:
            print(f"[SKIPPED] Token {symbol} already sent.")

# Send startup message
try:
    bot.send_message(CHANNEL_USERNAME, "✅ BatmanPump is now watching gmgn.ai!")
except Exception as e:
    print("[ERROR] Failed to send startup message:", e)

# Run the process every 30 seconds
while True:
    send_new_tokens()
    time.sleep(30)
