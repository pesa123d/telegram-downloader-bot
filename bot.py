from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
import yt_dlp
import os

TOKEN = os.getenv("7591723699:AAEMp8YORb7Gk6HERj7bdn7Xzls_9CsrAWQ")

def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("📘 فيسبوك", callback_data='facebook')],
        [InlineKeyboardButton("📸 إنستغرام", callback_data='instagram')],
        [InlineKeyboardButton("📺 يوتيوب", callback_data='youtube')],
        [InlineKeyboardButton("🎵 تيك توك", callback_data='tiktok')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("🔹 اختر المنصة:", reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    context.user_data['platform'] = query.data
    query.edit_message_text(text=f"✅ أرسل الآن رابط {query.data.capitalize()}:")

def download_media(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    platform = context.user_data.get('platform')

    if not platform:
        update.message.reply_text("⚠️ اختر المنصة أولاً باستخدام /start")
        return

    update.message.reply_text("🔄 جارِ التحميل، انتظر...")

    try:
        ydl_opts = {'outtmpl': 'video.%(ext)s'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info)
            update.message.reply_video(video=open(file_name, 'rb'))
            os.remove(file_name)

    except Exception as e:
        update.message.reply_text(f"❌ خطأ أثناء التحميل: {e}")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, download_media))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
