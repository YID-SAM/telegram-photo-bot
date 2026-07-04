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

# --------------------------------------------------
# Logging
# --------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# --------------------------------------------------
# Create required folders
# --------------------------------------------------
os.makedirs(Config.DOWNLOAD_FOLDER, exist_ok=True)
os.makedirs(Config.OUTPUT_FOLDER, exist_ok=True)
os.makedirs(Config.LOG_FOLDER, exist_ok=True)


# --------------------------------------------------
# /start command
# --------------------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "👋 Welcome!\n\n"
        "📸 Send me a photo.\n\n"
        "✨ I'll automatically:\n"
        "• Crop it into a square\n"
        "• Apply the official challenge frame\n"
        "• Return a profile-picture-ready image."
    )

    await update.message.reply_text(text)


# --------------------------------------------------
# Invalid message handler
# --------------------------------------------------
async def invalid(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "📸 Please send a photo."
    )


# --------------------------------------------------
# Photo handler
# --------------------------------------------------
async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    input_path = None
    output_path = None

    processing = await update.message.reply_text(
        "⏳ Processing your photo..."
    )

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

        logger.info(f"Input file: {input_path}")
        logger.info(f"Output file: {output_path}")

        # Download user's photo
        photo_file = await update.message.photo[-1].get_file()
        await photo_file.download_to_drive(input_path)

        logger.info("Photo downloaded successfully.")

        # Edit image
        edit_image(input_path, output_path)

        logger.info("Image edited successfully.")

        # Send edited image
        with open(output_path, "rb") as image:

            await update.message.reply_photo(
                photo=image,
                caption="✅ Your profile picture is ready!"
            )

        # Remove processing message
        await processing.delete()

        logger.info("Edited image sent.")

    except Exception as e:

        logger.exception("Error processing image")

        try:
            await processing.delete()
        except Exception:
            pass

        await update.message.reply_text(
            "❌ Sorry, I couldn't process your image.\nPlease try another photo."
        )

    finally:

        if input_path and os.path.exists(input_path):
            os.remove(input_path)

        if output_path and os.path.exists(output_path):
            os.remove(output_path)


# --------------------------------------------------
# Main
# --------------------------------------------------
def main():

    if not Config.BOT_TOKEN:
        raise ValueError(
            "BOT_TOKEN is missing. Check Railway Variables."
        )

    app = ApplicationBuilder().token(
        Config.BOT_TOKEN
    ).build()

    # Commands
    app.add_handler(
        CommandHandler("start", start)
    )

    # Photo messages
    app.add_handler(
        MessageHandler(
            filters.PHOTO,
            photo
        )
    )

    # Invalid messages
    app.add_handler(
        MessageHandler(
            ~filters.PHOTO & ~filters.COMMAND,
            invalid
        )
    )

    logger.info("Bot started successfully.")

    app.run_polling()


if __name__ == "__main__":
    main()