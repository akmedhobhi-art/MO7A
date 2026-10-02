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
    "germany": ["4915234567890", "4915798765432", "4917611223344", "4915155667788", "4915999887766", "491521112233", "491572223344", "491763334455", "491514445566", "491595556677", "491526667788", "491577778899", "491768889900", "491519990011", "491591011122", "491522022334", "491573033445", "491764044556", "491515055667", "491596066778", "491527077889", "491578088990", "491769099001", "491510100112", "491592122334", "491523133445", "491574144556", "491765155667", "491516166778", "491597177889", "491528188990", "491579199001", "491760200112", "491511211223", "491592222334", "491523233445", "491574244556", "491765255667", "491516266778", "491597277889", "491528288990", "491579299001", "491760300112", "491511311223", "491592322334", "491523333445", "491574344556", "491765355667", "491516366778", "491597377889"],
    "syria": ["963931234567", "963944556677", "963988112233", "963991234568", "963955443322", "963931112233", "963942223344", "963983334455", "963994445566", "963955556677", "963936667788", "963947778899", "963988889900", "963999990011", "963951011122", "963932022334", "963943033445", "963984044556", "963995055667", "963956066778", "963937077889", "963948088990", "963989099001", "963990100112", "963952122334", "963933133445", "963944144556", "963985155667", "963996166778", "963957177889", "963938188990", "963949199001", "963980200112", "963991211223", "963952222334", "963933233445", "963944244556", "963985255667", "963996266778", "963957277889", "963938288990", "963949299001", "963980300112", "963991311223", "963952322334", "963933333445", "963944344556", "963985355667", "963996366778", "963957377889"],
    "iraq": ["9647701234567", "9647812345678", "9647509876543", "9647901122334", "9647723344556", "964771112233", "964782223344", "964753334455", "964794445566", "964775556677", "964786667788", "964757778899", "964798889900", "964779990011", "964781011122", "964752022334", "964793033445", "964774044556", "964785055667", "964756066778", "964797077889", "964778088990", "964789099001", "964750100112", "964792122334", "964773133445", "964784144556", "964755155667", "964796166778", "964777177889", "964788188990", "964759199001", "964790200112", "964771211223", "964782222334", "964753233445", "964794244556", "964775255667", "964786266778", "964757277889", "964798288990", "964779299001", "964780300112", "964751311223", "964792322334", "964773333445", "964784344556", "964755355667", "964796366778", "964777377889"],
    "vietnam": ["84912345678", "84987654321", "84903111222", "84934555666", "84975888999", "849111112233", "849822223344", "849033334455", "849344445566", "849755556677", "849166667788", "849877778899", "849088889900", "849399990011", "849710101122", "849120202334", "849830303445", "849040404556", "849350505667", "849760606778", "849170707889", "849880808990", "849090909001", "849300100112", "849721212233", "849132323344", "849843434455", "849055555667", "849366666778", "849777777889", "849188888899", "849899999001", "849000200112", "849311211223", "849722222334", "849133333345", "849844444456", "849055555567", "849366666678", "849777777889", "849188888890", "849899999901", "849000300112", "849311311223", "849722322334", "849133333445", "849844444556", "849055555667", "849366666778", "849777777889"],
    "nz": ["64211234567", "64229876543", "64275554433", "64291112233", "64218887766", "642111112233", "642222223344", "642733334455", "642944445566", "642155556677", "642266667788", "642777778899", "642988889900", "642199990011", "642210101122", "642720202334", "642930303445", "642140404556", "642250505667", "642760606778", "642970707889", "642180808990", "642290909001", "642700100112", "642921212233", "642132323344", "642243434455", "642755555667", "642966666778", "642177777889", "642288888899", "642799999001", "642900200112", "642111211223", "642222222334", "642733333345", "642944444456", "642155555567", "642266666678", "642777777889", "642988888890", "642199999901", "642200300112", "642711311223", "642922322334", "642133333445", "642244444556", "642755555667", "642966666778", "642177777889"]
}

COUNTRY_NAMES = {
    "germany": "ألمانيا 🇩🇪", "syria": "سوريا 🇸🇾", "iraq": "العراق 🇮🇶",
    "vietnam": "فيتنام 🇻🇳", "nz": "نيوزيلندا 🇳🇿"
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
        if str(user_id) not in users:
            with open("users.txt", "a", encoding="utf-8") as f:
                f.write(str(user_id) + "\n")
            if user_id != ADMIN_ID:
                notif_text = (
                    f"🚨 **مستخدم جديد دخل البوت!**\n\n"
                    f"👤 الاسم: {name}\n"
                    f"🔗 اليوزر: {username}\n"
                    f"🆔 الـ ID: `{user_id}`"
                )
                await context.bot.send_message(chat_id=ADMIN_ID, text=notif_text, parse_mode="Markdown")
    except Exception as e:
        print(f"Error saving/notifying user: {e}")

def decorate_arabic(text):
    return (
        f"🔹 1: ⦙ ".join(list(text)) + f"\n"
        f"🔹 2: ✨ " + " ̶ ".join(list(text)) + " ✨\n"
        f"🔹 3: ★ " + " • ".join(list(text)) + " ★\n"
        f"🔹 4: ༺ " + text + " ༻\n"
        f"🔹 5: ༒ " + text + " ༒\n"
        f"🔹 6: ♛ " + text + " ♛\n"
        f"🔹 7: 📿 " + text + " 📿\n"
        f"🔹 8: ⚡ " + text + " ⚡\n"
        f"🔹 9: 💎 " + text + " 💎\n"
        f"🔹 10: 🌸 " + text + " 🌸\n"
        f"🔹 11: ♫ " + text + " ♫\n"
        f"🔹 12: 🥷 " + text + " 🥷\n"
        f"🔹 13: 🧨 " + text + " 🧨\n"
        f"🔹 14: 🌀 " + text + " 🌀\n"
        f"🔹 15: 🦅 " + text + " 🦅\n"
        f"🔹 16: 🦁 " + text + " 🦁\n"
        f"🔹 17: 🔥 " + text + " 🔥\n"
        f"🔹 18: 🧊 " + text + " 🧊\n"
        f"🔹 19: 🍀 " + text + " 🍀\n"
        f"🔹 20: 🌙 " + text + " 🌙"
    )

def decorate_english(text):
    fancy = text.translate(str.maketrans("abcdefghijklmnopqrstuvwxyz", "ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙ⚥ⓛⓜⓝⓞⓟⓠⓡ🇸ⓣⓤⓥⓦⓧⓨⓩ"))
    bold_sans = text.translate(str.maketrans("abcdefghijklmnopqrstuvwxyz", "𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝗾𝘆𝘇"))
    return (
        f"✨ 1. Fancy: {fancy}\n"
        f"✨ 2. Bold: {bold_sans}\n"
        f"✨ 3. ꧁༺ {text} ༻꧂\n"
        f"✨ 4. 𝔉𝔞𝔫𝔠𝔶 𝔛: {text}\n"
        f"✨ 5. 𝓐Ɓ𝓒: {text}\n"
        f"✨ 6. 𝕬𝕭𝕮: {text}\n"
        f"✨ 7. ⒶⒷⒸ: {text}\n"
        f"✨ 8. 🇦🇧🇨: {text}\n"
        f"✨ 9. mi1: {text}\n"
        f"✨ 10. 𝚨𝚩𝚪: {text}\n"
        f"✨ 11. 𝒯𝑒𝓍𝓉: {text}\n"
        f"✨ 12. 𝐓𝐞𝐱𝐭: {text}\n"
        f"✨ 13. 𝘛𝘦𝘹𝘵: {text}\n"
        f"✨ 14. ᴛᴇxᴛ: {text}\n"
        f"✨ 15. ᵗᵉˣᵗ: {text}\n"
        f"✨ 16. Ｔｅｘｔ: {text}\n"
        f"✨ 17. Ⓣⓔⓧⓣ: {text}\n"
        f"✨ 18. 𝕿𝖊𝖝𝖙: {text}\n"
        f"✨ 19. 🄶🄾🄳: {text}\n"
        f"✨ 20. ℌ𝔢𝔩𝔩𝔬: {text}"
    )

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
        await query.message.reply_text("ارسـل الاسـم لـلـزخـرفـة ✍️️:")
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
            [InlineKeyboardButton("🇩🇪 ألمانيا", callback_data="num_germany"), InlineKeyboardButton("🇸🇾 سوريا", callback_data="num_syria")],
            [InlineKeyboardButton("🇮🇶 العراق", callback_data="num_iraq"), InlineKeyboardButton("🇻🇳 فيتنام", callback_data="num_vietnam")],
            [InlineKeyboardButton("🇳🇿 نيوزيلندا", callback_data="num_nz")],
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
    if context.user_data.get('mode') == 'pdf_images':
        photo = update.message.photo[-1]
        fp = f"img_{update.message.from_user.id}_{len(context.user_data['pdf_list'])}.jpg"
        await (await context.bot.get_file(photo.file_id)).download_to_drive(fp)
        context.user_data['pdf_list'].append(fp)
        await update.message.reply_text(f"تم استقبال الصورة! (إجمالي: {len(context.user_data['pdf_list'])}). اكتب (تم) للإنهاء.")
    else:
        await update.message.reply_text("اضغط على زر صُـنـع pdf أولاً.")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('mode') == 'pdf_images' and update.message.text.strip().lower() == "تم":
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
