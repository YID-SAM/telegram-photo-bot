from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from config import Config
from handlers import start, photo
from logger import logger


app = ApplicationBuilder().token(Config.TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.PHOTO, photo))

logger.info("Bot started successfully")

app.run_polling()