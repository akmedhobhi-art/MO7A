import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# إعداد السجلات
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("• عربي ☪️ •", callback_data='ar'),
            InlineKeyboardButton("• english ✴️ •", callback_data='en'),
            InlineKeyboardButton("رق☘️عه", callback_data='ruqah')
        ],
        [
            InlineKeyboardButton("• الرموز ⚛️ •", callback_data='symbols')
        ],
        [
            InlineKeyboardButton("تحميل بدون علامه مائيه 😎", callback_data='download_no_wm')
        ],
        [
            InlineKeyboardButton("FAKE NUMBER 😍", callback_data='fake_number')
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "(أحمد) • أهلا بك في بوت الزخرفة •\n"
        "- اختر •من الاسفل ، ☪️\n"
        "--------------------\n"
        "WELCOME TO THE DECORATION BOT\n"
        "CHOOSE WHAT YOU WANT FROM THE BOTTOM 🏺"
    )
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

def main():
    if not TOKEN:
        print("Error: BOT_TOKEN variable is not set!")
        return

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
