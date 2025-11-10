import telebot
import os
from dotenv import load_dotenv


load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, f"✅ Your Chat ID is: {chat_id}")
    print("Your chat ID is:", chat_id)

print("Bot is waiting... send /start to your bot in Telegram.")
bot.polling()
