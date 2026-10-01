import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

# إعداد السجلات لمتابعة الأخطاء والتشغيل
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# دالة أمر /start لإرسال رسالة الترحيب والزرين
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # إنشاء الزرين (زر التحميل وزر الزخرفة)
    keyboard = [
        [InlineKeyboardButton("📥 تحميل بدون علامة مائية", callback_data="download")],
        [InlineKeyboardButton("✨ زخرفة النصوص ✨", callback_data="decoration")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # إرسال الرسالة مع الأزرار
    await update.message.reply_text(
        "أهلاً بك في بوت MO7A لتحميل الفيديوهات! اضغط على الزر أدناه لبدء التحميل أو اختيار زخرفة:",
        reply_markup=reply_markup
    )

# دالة التعامل مع ضغطات الأزرار
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "download":
        await query.message.reply_text("أرسل لي رابط الفيديو الآن لتحميله بدون علامة مائية 📥")
    elif query.data == "decoration":
        await query.message.reply_text("أرسل لي النص الذي تريد زخرفته ✨")

def main():
    # جلب التوكن من متغيرات البيئة التي أضفتها في Railway
    TOKEN = os.getenv("BOT_TOKEN")
    
    if not TOKEN:
        print("Error: BOT_TOKEN is not set in environment variables!")
        return

    # بناء وتشغيل البوت
    application = ApplicationBuilder().token(TOKEN).build()

    # تسجيل الأوامر والمعالجات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    print("Bot is starting...")
    application.run_polling()

if __name__ == "__main__":
    main()
