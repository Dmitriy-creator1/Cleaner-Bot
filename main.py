import os
from flask import Flask, request
import telebot
from telebot.types import ReplyKeyboardRemove, Update

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

# Render автоматически подставляет этот адрес или порт
RENDER_EXTERNAL_URL = os.environ.get("RENDER_EXTERNAL_URL")

@app.route('/')
def index():
    return "Бот работает через Webhook!"

# Маршрут, куда Telegram будет мгновенно присылать обновления
@app.route(f"/{TOKEN}", methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    return 'Forbidden', 403

# Обработка команд в группе и в ЛС
@bot.message_handler(commands=['clear', 'clean', 'start'])
def clear_keyboard(message):
    bot.send_message(
        message.chat.id,
        "🧹 Кнопки успешно очищены у всех участников!",
        reply_markup=ReplyKeyboardRemove()
    )

if __name__ == "__main__":
    # Устанавливаем Webhook на публичный адрес Render
    if RENDER_EXTERNAL_URL:
        webhook_url = f"{RENDER_EXTERNAL_URL}/{TOKEN}"
        bot.remove_webhook()
        bot.set_webhook(url=webhook_url)
        print(f"Вебхук успешно установлен на {webhook_url}")
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
