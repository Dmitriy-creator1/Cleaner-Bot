import os
import threading
from flask import Flask
import telebot
from telebot.types import ReplyKeyboardRemove

# Токен будет браться автоматически из настроек Render
TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Веб-сервер для поддержки работы на бесплатном тарифе Render
app = Flask(__name__)

@app.route('/')
def index():
    return "Бот работает!"

# Реакция на команды /clear, /clean или /start
@bot.message_handler(commands=['clear', 'clean', 'start'])
def clear_keyboard(message):
    # Бот сам берет ID чата (message.chat.id) и удаляет клавиатуру
    bot.send_message(
        message.chat.id,
        "🧹 Кнопки успешно удалены!",
        reply_markup=ReplyKeyboardRemove()
    )

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    # Запускаем бота в фоновом потоке
    threading.Thread(target=run_bot, daemon=True).start()
    # Запускаем веб-сервер на порту, который выдаст Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
