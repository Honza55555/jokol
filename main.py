import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = os.getenv("BASE_URL")  # např. https://mojebotaplikace.onrender.com

app = Flask(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ahoj")

@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), ApplicationBuilder().token(TOKEN).build().bot)
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.process_update(update)
    return "OK"

@app.route("/", methods=["GET"])
def index():
    return "Bot běží."

if __name__ == "__main__":
    import telegram
    bot = telegram.Bot(token=TOKEN)
    bot.set_webhook(f"{BASE_URL}/webhook/{TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
