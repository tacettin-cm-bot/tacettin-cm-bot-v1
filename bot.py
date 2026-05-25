from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters
import random
import logging
import json
import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = os.getenv("TOKEN")

DATA_FILE = "users_data.json"

def load_users():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_users(users):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

users = load_users()

chat_responses = [
    "😂 Kral, gene mi ölçtürmeye geldin?",
    "👀 Tacettin hazırda bekliyor, ne istiyorsun bakalım?",
    "🔥 Bu saatte ne arıyorsun kral?",
    "😈 Hadi söyle, bugün ne kadar iddialısın?",
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔥 **Tacettin Cm Bot** aktif!\n\n`/olc` yazarak ölçüm yap.", parse_mode="Markdown")

async def olc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    username = update.effective_user.username or update.effective_user.first_name

    try:
        size = int(context.args[0]) if context.args else random.randint(13, 27)
        size = max(6, min(32, size))
    except:
        size = random.randint(13, 27)

    if user_id not in users or size > users.get(user_id, {}).get("best", 0):
        users[user_id] = {"username": username, "best": size}
        save_users(users)

    text = f"🫡 **{size}cm**! Tacettin bu gece kraldır! 👑"
    
    keyboard = [[InlineKeyboardButton("🔄 Tekrar Ölç", callback_data="remeasure")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("olc", olc))
    print("✅ Tacettin Cm Bot Çalışıyor...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)
