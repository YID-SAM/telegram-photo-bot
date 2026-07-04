import os
import logging
from uuid import uuid4

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import Config
from editor import edit_image

# -----------------------------
# Logging
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# -----------------------------
# Create required folders
# -----------------------------
os.makedirs(Config.DOWNLOAD_FOLDER, exist_ok=True)
os.makedirs(Config.OUTPUT_FOLDER, exist_ok=True)
os.makedirs("logs", exist_ok=True)

# -----------------------------
# Start command
# -----------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\n\nSend me a photo and I'll edit it."
    )

# -----------------------------
# Photo handler
# -----------------------------
async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    input_path = None
    output_path = None

    try:
        unique_id = uuid4().hex

        input_path = os.path.join(
            Config.DOWNLOAD_FOLDER,
            f"{unique_id}.jpg"
        )

        output_path = os.path.join(
            Config.OUTPUT_FOLDER,
            f"{unique_id}.jpg"
        )

        logger.info(f"Input: {input_path}")
        logger.info(f"Output: {output_path}")

        # Download photo
        photo_file = await update.message.photo[-1].get_file()
        await photo_file.download_to_drive(input_path)

        logger.info("Photo downloaded successfully.")

        # Edit image
        edit_image(input_path, output_path)

        logger.info("Image edited successfully.")

        # Send image
        with open(output_path, "rb") as img:
            await update.message.reply_photo(photo=img)

        logger.info("Edited image sent.")

    except Exception:
        logger.exception("Error while processing image")
        await update.message.reply_text(
            "❌ Error processing image."
        )

    finally:

        if input_path and os.path.exists(input_path):
            os.remove(input_path)

        if output_path and os.path.exists(output_path):
            os.remove(output_path)

# -----------------------------
# Main
# -----------------------------
def main():

    app = ApplicationBuilder().token(Config.BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, photo))

    logger.info("Bot started successfully.")

    app.run_polling()


if __name__ == "__main__":
    main()