import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# إعداد السجلات
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 1. أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك! البوت يعمل بنجاح وتحت سيطرتك الكاملة 🚀")

# 2. الرد على الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if "مرحبا" in text or "أهلا" in text:
        await update.message.reply_text("أهلاً بك! كيف يمكنني مساعدتك؟")
    else:
        await update.message.reply_text(f"وصلتني رسالتك: {update.message.text}")

if __name__ == '__main__':
    # تم وضع التوكن الخاص بك هنا جاهزاً
    TOKEN = "8972769903:AAFr4BRrg9QohhN6Ph1y7RyqP2453PS7gxs"
    
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("البوت يعمل...")
    app.run_polling()
