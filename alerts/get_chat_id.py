import telebot

TOKEN = "8520468474:AAFeXhNO9gAVHxzWryzLu6MzJael-y6ynME"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, f"✅ Your Chat ID is: {chat_id}")
    print("Your chat ID is:", chat_id)

print("Bot is waiting... send /start to your bot in Telegram.")
bot.polling()
