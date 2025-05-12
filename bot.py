import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests
import os

# تنظیمات
TELEGRAM_BOT_TOKEN = '7605103548:AAFpK8cI5mB71wj2CfT-qUbyh4ExbKIsE8I'
BOX_API_USERNAME = 'shmohmdi'
BOX_API_PASSWORD = 'dsHLdXye8WKvc50OIV3xr'
BOX_API_URL = 'https://boxapi.ir/api/instagram/media/get_info '

bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

def start(update: Update, context: CallbackContext):
    update.message.reply_text('سلام! لینک اینستاگرام فیلم رو بفرست تا دانلودش کنم.')

def handle_message(update: Update, context: CallbackContext):
    url = update.message.text.strip()
    update.message.reply_text("در حال دریافت اطلاعات فیلم...")

    # فرض می‌کنیم URL شامل id است
    try:
        media_id = extract_media_id(url)
    except Exception as e:
        update.message.reply_text("لینک اینستاگرام نامعتبر است.")
        return

    # ارسال درخواست به BoxAPI
    response = requests.post(
        BOX_API_URL,
        auth=(BOX_API_USERNAME, BOX_API_PASSWORD),
        json={"id": media_id}
    )

    if response.status_code != 200:
        update.message.reply_text("خطا در دریافت اطلاعات فیلم.")
        return

    data = response.json()

    if not data.get('result', {}).get('url'):
        update.message.reply_text("فیلمی پیدا نشد.")
        return

    video_url = data['result']['url']
    caption = data.get('result', {}).get('caption', 'فیلم')

    # دانلود و ارسال فیلم
    update.message.reply_text("در حال دانلود فیلم...")
    video_path = download_video(video_url)

    if video_path:
        with open(video_path, 'rb') as f:
            update.message.reply_video(video=f, caption=caption[:1024])
        os.remove(video_path)
    else:
        update.message.reply_text("خطا در دانلود فیلم.")

def extract_media_id(url):
    # ساده‌سازی: فرض می‌کنیم ID مستقیم در لینک وجود دارد مثل ?id=123456789
    if "id=" in url:
        return int(url.split("id=")[-1].split("&")[0])
    raise ValueError("No ID found")

def download_video(url):
    try:
        r = requests.get(url, stream=True)
        path = "video.mp4"
        with open(path, 'wb') as f:
            for chunk in r.iter_content(1024 * 1024):
                if chunk:
                    f.write(chunk)
        return path
    except Exception as e:
        print("Error downloading video:", e)
        return None

if __name__ == '__main__':
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    print("ربات در حال اجرا...")
    updater.start_polling()
    updater.idle()