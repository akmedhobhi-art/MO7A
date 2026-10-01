import os
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("تحميل بدون علامه مائيه", callback_data="download_prompt")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "أهلاً بك في بوت MO7A لتحميل الفيديوهات! اضغط على الزر أدناه لبدء التحميل:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "download_prompt":
        context.user_data['waiting_for_url'] = True
        await query.message.reply_text("أرسل الرابط الذي تريد تحميله الآن 🔗:")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text.startswith(("http://", "https://")):
        msg = await update.message.reply_text("جاري تحميل الفيديو، انتظر لحظات... ⏳")

        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': 'downloaded_video.%(ext)s',
            'quiet': True,
            'no_warnings': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(text, download=True)
                filename = ydl.prepare_filename(info)

            with open(filename, 'rb') as video_file:
                await update.message.reply_video(video=video_file, caption="تم التحميل بنجاح! ✨")

            if os.path.exists(filename):
                os.remove(filename)
            await msg.delete()

        except Exception as e:
            await msg.edit_text("حدث خطأ أثناء تحميل الفيديو، تأكد من صحة الرابط وجرب مرة أخرى.")
    else:
        await update.message.reply_text("من فضلك اضغط على زر التحميل أولاً أو أرسل رابطاً صحيحاً.")

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()
