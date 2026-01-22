import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import yt_dlp

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    link = update.message.text

    if "x.com" in link or "twitter.com" in link:
        await update.message.reply_text("Downloading... ⏳")

        ydl_opts = {
            "format": "mp4",
            "outtmpl": "video.%(ext)s"
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link, download=True)
                file = ydl.prepare_filename(info)

            await update.message.reply_video(open(file, "rb"))
            os.remove(file)

        except:
            await update.message.reply_text("❌ Failed")

    else:
        await update.message.reply_text("Send X video link")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
app.run_polling()
