import os
import logging
import traceback
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
# Create folders
# -----------------------------
os.makedirs(Config.DOWNLOAD_FOLDER, exist_ok=True)
os.makedirs(Config.OUTPUT_FOLDER, exist_ok=True)


# -----------------------------
# /start
# -----------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\n\nSend me a photo."
    )


# -----------------------------
# Photo handler
# -----------------------------
async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    input_path = None
    output_path = None

    try:

        logger.info("Received photo")

        unique_id = uuid4().hex

        input_path = os.path.join(
            Config.DOWNLOAD_FOLDER,
            f"{unique_id}.jpg"
        )

        output_path = os.path.join(
            Config.OUTPUT_FOLDER,
            f"{unique_id}.jpg"
        )

        logger.info(f"Input file: {input_path}")
        logger.info(f"Output file: {output_path}")

        # Download image
        photo_file = await update.message.photo[-1].get_file()

        logger.info("Downloading image...")

        await photo_file.download_to_drive(input_path)

        logger.info("Image downloaded successfully.")

        # Edit image
        logger.info("Calling edit_image()...")

        edit_image(input_path, output_path)

        logger.info("Image edited successfully.")

        # Send image
        with open(output_path, "rb") as image:
            await update.message.reply_photo(photo=image)

        logger.info("Edited image sent.")

    except Exception as e:

        logger.error(traceback.format_exc())

        # TEMPORARY
        # Send the real error back to Telegram
        await update.message.reply_text(
            f"ERROR:\n{str(e)}"
        )

    finally:

        try:
            if input_path and os.path.exists(input_path):
                os.remove(input_path)

            if output_path and os.path.exists(output_path):
                os.remove(output_path)

        except Exception:
            logger.exception("Cleanup failed")


# -----------------------------
# Main
# -----------------------------
def main():

    if not Config.BOT_TOKEN:
        raise ValueError(
            "BOT_TOKEN environment variable is missing."
        )

    app = ApplicationBuilder().token(Config.BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, photo))

    logger.info("Bot started successfully.")

    app.run_polling()


if __name__ == "__main__":
    main()