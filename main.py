import os
import time
import telebot
from fetch_tokens import get_tokens

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "@BatmanPump")

bot = telebot.TeleBot(BOT_TOKEN)
sent_tokens = set()

CHAINS = {
    "solana": "SOLANA",
    "bsc": "BSC",
    "eth": "ETHEREUM",
    "base": "BASE"
}

def send_new_tokens():
    for chain, display in CHAINS.items():
        tokens = get_tokens(chain)
        for token in tokens:
            name = token.get("name", "N/A")
            symbol = token.get("symbol", "N/A")
            price = token.get("price", "0.00")
            url = token.get("url", "#")

            unique_key = f"{chain}:{symbol}:{price}"
            if unique_key not in sent_tokens:
                msg = f"🚀 *New Token Detected on {display}*

*Name:* {name}
*Symbol:* {symbol}
*Price:* ${price}
[Chart]({url})"
                try:
                    bot.send_message(CHANNEL_USERNAME, msg, parse_mode="Markdown")
                    sent_tokens.add(unique_key)
                    print(f"[{display}] Sent Token - {name}, Symbol: {symbol}, Price: {price}")
                except Exception as e:
                    print("Telegram Error:", e)

bot.send_message(CHANNEL_USERNAME, "✅ BatmanPump Bot is now running and monitoring new tokens on Solana, Ethereum, BSC, and Base!", parse_mode="Markdown")

while True:
    send_new_tokens()
    time.sleep(30)