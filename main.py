import os
import yt_dlp
from PIL import Image
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

# ضع هنا الآيدي الحقيقي لحسابك على تيليجرام لكي يعمل أمر الإحصائيات معك وحدك
ADMIN_ID = 6216543508  # استبدل هذا الرقم بالآيدي الخاص بك

def save_user(user_id):
    """دالة لتسجيل المستخدمين الجدد في ملف نصي بدون تكرار"""
    try:
        users = set()
        if os.path.exists("users.txt"):
            with open("users.txt", "r") as f:
                users = set(f.read().splitlines())
        
        if str(user_id) not in users:
            with open("users.txt", "a") as f:
                f.write(str(user_id) + "\n")
    except Exception as e:
        print(f"Error saving user: {e}")

def decorate_arabic(text):
    s1 = " ⦙ ".join(list(text))
    s2 = "✨ " + " ̶ ".join(list(text)) + " ✨"
    s3 = "★ " + " • ".join(list(text)) + " ★"
    s4 = " ༺ " + text + " ༻ "
    s5 = "『 " + text + " 』"
    s6 = "【 " + text + " 】"
    s7 = "ـ,.-~*'`^~*'-.,ـ " + text + " ـ,.-~*'`^~*'-.,ـ"
    s8 = "👑 " + " ༒ ".join(list(text)) + " 👑"
    return f"🔹 الشكل 1:\n{s1}\n\n🔹 الشكل 2:\n{s2}\n\n🔹 الشكل 3:\n{s3}\n\n🔹 الشكل 4:\n{s4}\n\n🔹 الشكل 5:\n{s5}\n\n🔹 الشكل 6:\n{s6}\n\n🔹 الشكل 7:\n{s7}\n\n🔹 الشكل 8:\n{s8}"

def decorate_english(text):
    fancy = text.translate(str.maketrans("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", "ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙ⚥ⓛⓜⓝⓞⓟⓠⓡ🇸ⓣⓤⓥⓦⓧⓨⓩⒶⒷⒸⒹ🇪ⓕⒼⒽⒾⒿⓀⓁⓂⓃ𝓞ⓅⓆⓇⓈⓉⓊⓋⓌ𝓍𝓎𝓏"))
    bold_sans = text.translate(str.maketrans("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", "𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡OP𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭"))
    italic = text.translate(str.maketrans("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", "𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭mbn𝘰𝘱𝘲𝘳𝘴𝘵𝘂𝘷𝘸𝘹𝘺𝘻𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘫𝘒𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡"))
    gothic = text.translate(str.maketrans("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", "𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝘘𝔙𝔚𝔛𝔜ℨ"))
    boxed = " 🔲 ".join(list(text))
    brackets = "【 " + text + " 】"
    flair = "✨ " + text + " ✨"
    return f"✨ 1. Fancy:\n{fancy}\n\n✨ 2. Bold:\n{bold_sans}\n\n✨ 3. Italic:\n{italic}\n\n✨ 4. Gothic:\n{gothic}\n\n✨ 5. Boxed:\n{boxed}\n\n✨ 6. Brackets:\n{brackets}\n\n✨ 7. Flair:\n{flair}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # تسجيل المستخدم تلقائياً فور ضغطه على /start
    user_id = update.message.from_user.id
    save_user(user_id)

    welcome_text = (
        "*أهـلاً بـك فـي بـوت ~• 𝓜𝓞7𝓐 •~ يـسـاعـدك هـذا الـبـوت عـلـي الـعـديـد مـن الأشـيـاء وكـلـهـم فـالأسـفـل “ يـقـلـبـوشـتـي 😍*\n"
        "*تـحـيـاتـي لـك ~,ًاحمد ,ًصبحي~*\n"
        "*صـانـع ومـطـور هـذا الـبـوت .* "
    )
    keyboard = [
        [InlineKeyboardButton("🔴 تحميل بدون علامه مائيه", callback_data="download_prompt")],
        [InlineKeyboardButton("🟢 زخــ🪄ـــارف", callback_data="decor_menu")],
        [InlineKeyboardButton("🔵 صُـنـع pdf 🍀", callback_data="pdf_menu")],
        [InlineKeyboardButton("🟡 تـحـديـد مـوقـع بـرقـم الـهـاتـف", callback_data="location_prompt")],
        [InlineKeyboardButton("🟣 صـنـع LINK مـلغـم", url="https://t.me/A7med_foryou_bot")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """أمر خاص بالمطور لمعرفة عدد المستخدمين"""
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("هذا الأمر مخصص للمطور فقط 🚫")
        return
    
    count = 0
    if os.path.exists("users.txt"):
        with open("users.txt", "r") as f:
            count = len(f.read().splitlines())
            
    await update.message.reply_text(f"📊 إحصائيات البوت:\n👥 عدد المستخدمين الذين دخلوا البوت: {count} شخصاً.")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "download_prompt":
        context.user_data['mode'] = 'download'
        await query.message.reply_text("أرسل رابط الفديو الذي تريد تحميله 🔗:")
        
    elif query.data == "decor_menu":
        keyboard = [
            [InlineKeyboardButton("عربـي", callback_data="decor_ar")],
            [InlineKeyboardButton("انكليزي", callback_data="decor_en")],
            [InlineKeyboardButton("🔙 رجوع", callback_data="back_main")]
        ]
        await query.message.edit_text("اختر لغة الزخرفة المطلوبة:", reply_markup=InlineKeyboardMarkup(keyboard))
        
    elif query.data == "decor_ar":
        context.user_data['mode'] = 'decor_ar'
        await query.message.reply_text("ارسـل الاسـم الـذي تريـد زخـرفـتـه ✍️:")
        
    elif query.data == "decor_en":
        context.user_data['mode'] = 'decor_en'
        await query.message.reply_text("ارسـل الاسـم الـذي تريـد زخـرفـتـه ✍️:")
        
    elif query.data == "pdf_menu":
        context.user_data['mode'] = 'pdf_images'
        context.user_data['pdf_list'] = []
        await query.message.reply_text("ارسـل الصـور الـتـي تـريـد عـمـلـهـا pdf 📂\n(أرسل الصور واحدة تلو الأخرى، وعند الانتهاء اكتب كلمة: تم)")
        
    elif query.data == "location_prompt":
        context.user_data['mode'] = 'location_phone'
        await query.message.reply_text("ارسل الرقم 📞:")
        
    elif query.data == "back_main":
        welcome_text = (
            "*أهـلاً بـك فـي بـوت ~• 𝓜𝓞7𝓐 •~ يـسـاعـدك هـذا الـبـوت عـلـي الـعـديـد مـن الأشـيـاء وكـلـهـم فـالأسـفـل “ يـقـلـبـوشـتـي 😍*\n"
            "*تـحـيـاتـي لـك ~,ًاحمد ,ًصبحي~*\n"
            "*صـانـع ومـطـور هـذا الـبـوت .* "
        )
        keyboard = [
            [InlineKeyboardButton("🔴 تحميل بدون علامه مائيه", callback_data="download_prompt")],
            [InlineKeyboardButton("🟢 زخــ🪄ـــارف", callback_data="decor_menu")],
            [InlineKeyboardButton("🔵 صُـنـع pdf 🍀", callback_data="pdf_menu")],
            [InlineKeyboardButton("🟡 تـحـديـد مـوقـع بـرقـم الـهـاتـف", callback_data="location_prompt")],
            [InlineKeyboardButton("🟣 صـنـع LINK مـلغـم", url="https://t.me/A7med_foryou_bot")]
        ]
        await query.message.edit_text(welcome_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    mode = context.user_data.get('mode')
    
    if mode == 'download' or (text and text.startswith(("http://", "https://"))):
        msg = await update.message.reply_text("جاري جلب الفيديو بدون علامة مائية، انتظر لحظات... ⏳")
        ydl_opts = {'format': 'bestvideo+bestaudio/best', 'outtmpl': 'downloaded_video.%(ext)s', 'quiet': True, 'no_warnings': True}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(text, download=True)
                filename = ydl.prepare_filename(info)
            with open(filename, 'rb') as video_file:
                await update.message.reply_video(video=video_file, caption="تم التحميل بنجاح بدون علامة مائية! ✨")
            if os.path.exists(filename):
                os.remove(filename)
            await msg.delete()
            context.user_data['mode'] = None
        except Exception as e:
            await msg.edit_text("حدث خطأ أثناء تحميل الفيديو، تأكد من صحة الرابط وجرب مرة أخرى.")
            
    elif mode == 'decor_ar':
        result = decorate_arabic(text)
        await update.message.reply_text(f"✨ إليك جميع زخارف الاسم:\n\n{result}")
        context.user_data['mode'] = None
        
    elif mode == 'decor_en':
        result = decorate_english(text)
        await update.message.reply_text(f"✨ إليك جميع زخارف الاسم:\n\n{result}")
        context.user_data['mode'] = None
        
    elif mode == 'location_phone':
        await update.message.reply_text(f"📍 بيانات الرقم ({text}):\n👤 اسم صاحب الرقم: غير متوفر في القاعدة المجانية\n🌍 الدولة / المكان: يتم التحديد عبر الأبراج وخوادم الاتصالات.\n💡 ملاحظة: هذه الخدمة تطلب صلاحيات أمنية خاصة.")
        context.user_data['mode'] = None
        
    else:
        await update.message.reply_text("من فضلك اضغط على أحد الأزرار الأساسية في القائمة عبر إرسال /start أولاً.")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mode = context.user_data.get('mode')
    if mode == 'pdf_images':
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)
        file_path = f"img_{update.message.from_user.id}_{len(context.user_data['pdf_list'])}.jpg"
        await file.download_to_drive(file_path)
        context.user_data['pdf_list'].append(file_path)
        await update.message.reply_text(f"تم استقبال الصورة بنجاح! 📸 (إجمالي الصور: {len(context.user_data['pdf_list'])}).\nأرسل صورة أخرى أو اكتب كلمة (تم) لإنشاء ملف الـ PDF.")
    else:
        await update.message.reply_text("الرجاء الضغط على زر صُـنـع pdf أولاً قبل إرسال الصور.")

async def handle_text_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    mode = context.user_data.get('mode')
    if mode == 'pdf_images' and text and text.strip().lower() == "تم":
        pdf_list = context.user_data.get('pdf_list', [])
        if not pdf_list:
            await update.message.reply_text("لم تقم بإرسال أي صور بعد!")
            return
        msg = await update.message.reply_text("جاري تحويل الصور إلى ملف PDF... ⏳")
        try:
            image_objects = [Image.open(p).convert('RGB') for p in pdf_list]
            pdf_filename = "document.pdf"
            image_objects[0].save(pdf_filename, save_all=True, append_images=image_objects[1:])
            with open(pdf_filename, 'rb') as f:
                await update.message.reply_document(document=f, caption="تم إنشاء ملف الـ PDF بنجاح! 📄✨")
            for p in pdf_list:
                if os.path.exists(p):
                    os.remove(p)
            if os.path.exists(pdf_filename):
                os.remove(pdf_filename)
            await msg.delete()
            context.user_data['mode'] = None
            context.user_data['pdf_list'] = []
        except Exception as e:
            await msg.edit_text("حدث خطأ أثناء إنشاء ملف الـ PDF.")
    else:
        await handle_message(update, context)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats_command))  # أمر الإحصائيات للمطور
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_commands))
    app.run_polling()

if __name__ == "__main__":
    main()
