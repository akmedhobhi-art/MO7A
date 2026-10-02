import os
import random
import asyncio
import yt_dlp
from PIL import Image
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = 6216543508

FAKE_NUMBERS = {
    "germany": ["4915234567890", "4915798765432", "4917611223344", "4915155667788", "4915999887766"],
    "lebanon": ["9613508860", "96170123456", "96171987654", "96181112233", "96176445566"],
    "vietnam": ["84912345678", "84987654321", "84903111222", "84934555666", "84975888999"],
    "syria": ["963931234567", "963944556677", "963988112233", "963991234568", "963955443322"],
    "iraq": ["9647701234567", "9647812345678", "9647509876543", "9647901122334", "9647723344556"],
    "nz": ["64211234567", "64229876543", "64275554433", "64291112233", "64218887766"]
}

COUNTRY_NAMES = {
    "germany": "ألمانيا 🇩🇪", "lebanon": "لبنان 🇱🇧", "vietnam": "فيتنام 🇻🇳",
    "syria": "سوريا 🇸🇾", "iraq": "العراق 🇮🇶", "nz": "نيوزيلندا 🇳🇿"
}

async def save_and_notify_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not user:
        return
        
    user_id = user.id
    name = user.full_name
    username = f"@{user.username}" if user.username else "لا يوجد"
    
    try:
        users = set()
        if os.path.exists("users.txt"):
            with open("users.txt", "r", encoding="utf-8") as f:
                users = set(f.read().splitlines())
        
        # إذا لم يكن المستخدم موجوداً في الملف
        if str(user_id) not in users:
            with open("users.txt", "a", encoding="utf-8") as f:
                f.write(str(user_id) + "\n")
            
            # إرسال إشعار للمطور (طالما ليس المطور هو من يدخل لأول مرة، أو حتى لو أردت رؤيته استبعد شرط المطور)
            if user_id != ADMIN_ID:
                notif_text = (
                    f"🚨 **مستخدم جديد دخل البوت!**\n\n"
                    f"👤 الاسم: {name}\n"
                    f"🔗 اليوزر: {username}\n"
                    f"🆔 الـ ID: `{user_id}`"
                )
                await context.bot.send_message(chat_id=ADMIN_ID, text=notif_text, parse_mode="Markdown")
        
        # ملاحظة: إذا أردت أن يأتيك إشعار حتى لو دخلت أنت بنفسك للتجربة، يمكنك حذف شرط (user_id != ADMIN_ID) في الأعلى.
    except Exception as e:
        print(f"Error saving/notifying user: {e}")

def decorate_arabic(text):
    s1 = " ⦙ ".join(list(text))
    s2 = "✨ " + " ̶ ".join(list(text)) + " ✨"
    s3 = "★ " + " • ".join(list(text)) + " ★"
    s4 = " ༺ " + text + " ༻ "
    return f"🔹 الشكل 1:\n{s1}\n\n🔹 الشكل 2:\n{s2}\n\n🔹 الشكل 3:\n{s3}\n\n🔹 الشكل 4:\n{s4}"

def decorate_english(text):
    fancy = text.translate(str.maketrans("abcdefghijklmnopqrstuvwxyz", "ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙ⚥ⓛⓜⓝⓞⓟⓠⓡ🇸ⓣⓤⓥⓦⓧⓨⓩ"))
    bold_sans = text.translate(str.maketrans("abcdefghijklmnopqrstuvwxyz", "𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝗾𝘆𝘇"))
    return f"✨ 1. Fancy:\n{fancy}\n\n✨ 2. Bold:\n{bold_sans}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await save_and_notify_user(update, context)
    welcome_text = "*أهـلاً بـك فـي بـوت ~• 𝓜𝓞7𝓐 •~ يـسـاعـدك هـذا الـبـوت 😍*"
    keyboard = [
        [InlineKeyboardButton("🔴 تحميل بدون علامه مائيه", callback_data="download_prompt")],
        [InlineKeyboardButton("🟢 زخــ🪄ـــارف", callback_data="decor_menu")],
        [InlineKeyboardButton("🔵 صُـنـع pdf 🍀", callback_data="pdf_menu")],
        [InlineKeyboardButton("🟡 تـحـديـد مـوقـع بـرقـم الـهـاتـف", callback_data="location_prompt")],
        [InlineKeyboardButton("📞 FAKE NUMBER ⚫️", callback_data="fake_number_menu")],
        [InlineKeyboardButton("🟣 صـنـع LINK مـلغـم", callback_data="malicious_link")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")
    elif update.callback_query:
        await update.callback_query.message.edit_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        await update.message.reply_text("هذا الأمر للمطور فقط 🚫")
        return
    count = len(open("users.txt", "r", encoding="utf-8").read().splitlines()) if os.path.exists("users.txt") else 0
    await update.message.reply_text(f"📊 عدد المستخدمين: {count}")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await save_and_notify_user(update, context)

    if query.data == "download_prompt":
        context.user_data['mode'] = 'download'
        await query.message.reply_text("أرسل رابط الفديو للتحميل 🔗:")
    elif query.data == "decor_menu":
        kb = [[InlineKeyboardButton("عربـي", callback_data="decor_ar"), InlineKeyboardButton("انكليزي", callback_data="decor_en")], [InlineKeyboardButton("🔙 رجوع", callback_data="back_main")]]
        await query.message.edit_text("اختر اللغة:", reply_markup=InlineKeyboardMarkup(kb))
    elif query.data == "decor_ar":
        context.user_data['mode'] = 'decor_ar'
        await query.message.reply_text("ارسـل الاسـم لـلـزخـرفـة ✍️:")
    elif query.data == "decor_en":
        context.user_data['mode'] = 'decor_en'
        await query.message.reply_text("ارسـل الاسـم لـلـزخـرفـة ✍️:")
    elif query.data == "pdf_menu":
        context.user_data['mode'] = 'pdf_images'
        context.user_data['pdf_list'] = []
        await query.message.reply_text("أرسل الصور واحدة تلو الأخرى، وعند الانتهاء اكتب: تم 📂")
    elif query.data == "location_prompt":
        context.user_data['mode'] = 'location_phone'
        await query.message.reply_text("ارسل الرقم 📞:")
    elif query.data == "fake_number_menu":
        kb = [
            [InlineKeyboardButton("🇩🇪 ألمانيا", callback_data="num_germany"), InlineKeyboardButton("🇱🇧 لبنان", callback_data="num_lebanon")],
            [InlineKeyboardButton("🇻🇳 فيتنام", callback_data="num_vietnam"), InlineKeyboardButton("🇸🇾 سوريا", callback_data="num_syria")],
            [InlineKeyboardButton("🇮🇶 العراق", callback_data="num_iraq"), InlineKeyboardButton("🇳🇿 نيوزيلندا", callback_data="num_nz")],
            [InlineKeyboardButton("🔙 رجوع", callback_data="back_main")]
        ]
        await query.message.edit_text("اختر الدولة المطلوبة للحصول على رقم وهمي 🌍:", reply_markup=InlineKeyboardMarkup(kb))
    elif query.data == "malicious_link":
        await query.message.reply_text("تحتاج الي التواصل مع المالك لان هذا الامر ليس مجاني ⚠️\nللتواصل: @MODY2S")
        
        user = update.effective_user
        notif_text = (
            f"🔗 **مستخدم طلب تفاصيل اللينك الملغم!**\n\n"
            f"👤 الاسم: {user.full_name}\n"
            f"🔗 اليوزر: @{user.username if user.username else 'لا يوجد'}\n"
            f"🆔 الـ ID: `{user.id}`"
        )
        await context.bot.send_message(chat_id=ADMIN_ID, text=notif_text, parse_mode="Markdown")

    elif query.data.startswith("num_"):
        ck = query.data.replace("num_", "")
        if ck in FAKE_NUMBERS:
            pn = random.choice(FAKE_NUMBERS[ck])
            kb = [
                [InlineKeyboardButton("🔄 رقم جديد", callback_data=f"num_{ck}")],
                [InlineKeyboardButton("🔙 رجوع", callback_data="fake_number_menu")]
            ]
            await query.message.edit_text(
                f"🌍 الدولة: {COUNTRY_NAMES.get(ck)}\n\n"
                f"🔢 الرقم: `{pn}`\n\n"
                f"✅ تم استخراج الرقم بنجاح!\n\n"
                f"📌 استخدم الرقم في التطبيق الذي تريده وسيصلك الكود على هذا البوت.",
                reply_markup=InlineKeyboardMarkup(kb),
                parse_mode="Markdown"
            )
            
            await asyncio.sleep(60)
            await query.message.reply_text(f"📩 كود التحقق الخاص بك:\n`57993`", parse_mode="Markdown")

    elif query.data == "back_main":
        await start(update, context)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await save_and_notify_user(update, context)
    text = update.message.text
    mode = context.user_data.get('mode')
    
    if mode == 'download' or (text and text.startswith(("http://", "https://"))):
        msg = await update.message.reply_text("جاري جلب الفيديو بدون علامة مائية... ⏳")
        try:
            ydl_opts = {'format': 'best', 'outtmpl': 'vid.%(ext)s', 'quiet': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(text, download=True)
                fn = ydl.prepare_filename(info)
            with open(fn, 'rb') as vf:
                await update.message.reply_video(video=vf, caption="تم التحميل بنجاح! ✨")
            if os.path.exists(fn): os.remove(fn)
            await msg.delete()
            context.user_data['mode'] = None
        except Exception:
            await msg.edit_text("حدث خطأ، تأكد من صحة الرابط.")
    elif mode == 'decor_ar':
        await update.message.reply_text(decorate_arabic(text))
        context.user_data['mode'] = None
    elif mode == 'decor_en':
        await update.message.reply_text(decorate_english(text))
        context.user_data['mode'] = None
    elif mode == 'location_phone':
        await update.message.reply_text(f"📍 بيانات الرقم ({text}):\n👤 غير متوفر في القاعدة المجانية\n🌍 التحديد عبر الأبراج.")
        context.user_data['mode'] = None
    else:
        await update.message.reply_text("أرسل /start لعرض القائمة الرئيسية.")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await save_and_notify_user(update, context)
    if context.user_data.get('mode'] == 'pdf_images':
        photo = update.message.photo[-1]
        fp = f"img_{update.message.from_user.id}_{len(context.user_data['pdf_list'])} .jpg"
        await (await context.bot.get_file(photo.file_id)).download_to_drive(fp)
        context.user_data['pdf_list'].append(fp)
        await update.message.reply_text(f"تم استقبال الصورة! (إجمالي: {len(context.user_data['pdf_list'])}). اكتب (تم) للإنهاء.")
    else:
        await update.message.reply_text("اضغط على زر صُـنـع pdf أولاً.")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('mode'] == 'pdf_images' and update.message.text.strip().lower() == "تم":
        plist = context.user_data.get('pdf_list', [])
        if not plist:
            await update.message.reply_text("لم ترسل أي صور!")
            return
        msg = await update.message.reply_text("جاري إنشاء الـ PDF... ⏳")
        try:
            imgs = [Image.open(p).convert('RGB') for p in plist]
            pdf_name = "doc.pdf"
            imgs[0].save(pdf_name, save_all=True, append_images=imgs[1:])
            with open(pdf_name, 'rb') as f:
                await update.message.reply_document(f, caption="تم إنشاء الـ PDF بنجاح! 📄")
            for p in plist: 
                if os.path.exists(p): os.remove(p)
            if os.path.exists(pdf_name): os.remove(pdf_name)
            await msg.delete()
            context.user_data.update({'mode': None, 'pdf_list': []})
        except Exception:
            await msg.edit_text("حدث خطأ أثناء تحويل الصور.")
    else:
        await handle_message(update, context)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling()

if __name__ == "__main__":
    main()
