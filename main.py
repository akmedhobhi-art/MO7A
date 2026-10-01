import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك! أرسل لي رابط فيديو من (TikTok, Instagram, Reels) وسأقوم بتحميله لك بدون علامة مائية.")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    
    # التأكد أن الرسالة تحتوي على رابط
    if not url.startswith(("http://", "https://")):
        return

    msg = await update.message.reply_text("جاري تحميل الفيديو، انتظر لحظات... ⏳")

    # إعدادات yt-dlp لتحميل أفضل جودة بدون علامة مائية
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': 'downloaded_video.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        # إرسال الفيديو للمستخدم
        with open(filename, 'rb') as video_file:
            await update.message.reply_video(video=video_file, caption="تم التحميل بنجاح! ✨")

        # حذف الملف من السيرفر بعد الإرسال لتوفير المساحة
        if os.path.exists(filename):
            os.remove(filename)
        await msg.delete()

    except Exception as e:
        await msg.edit_text("حدث خطأ أثناء تحميل الفيديو، تأكد من صحة الرابط وجرب مرة أخرى.")

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    # استقبال أي نص يحتوي على رابط
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    app.run_polling()

if __name__ == "__main__":
    main()
