import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# جلب التوكن من متغيرات البيئة في ريندر
TOKEN = os.getenv("BOT_TOKEN")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if not ("instagram.com" in url or "facebook.com" in url):
        await update.message.reply_text("أرسل رابط Instagram أو Facebook.")
        return

    await update.message.reply_text("⏳ جاري تحميل الفيديو...")

    filename = f"video_{update.message.from_user.id}.mp4"

    options = {
        "format": "best[ext=mp4]/best",
        "outtmpl": filename,
        "noplaylist": True,
        "quiet": True,
        "merge_output_format": "mp4"
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])

        if os.path.exists(filename):
            with open(filename, "rb") as video:
                await update.message.reply_video(
                    video=video,
                    caption="✅ تم تحميل الفيديو"
                )

            os.remove(filename)
        else:
            await update.message.reply_text("❌ لم يتم العثور على الفيديو.")

    except Exception:
        if os.path.exists(filename):
            os.remove(filename)

        await update.message.reply_text(
            "❌ تعذر تحميل الفيديو. تأكد أن الرابط عام ويعمل."
        )

def main():
    # التحقق من وجود التوكن قبل تشغيل البوت
    if not TOKEN:
        raise ValueError("❌ لم يتم العثور على BOT_TOKEN في متغيرات البيئة (Environment Variables).")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            download_video
        )
    )

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
