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
# Create folders if they don't exist
# -----------------------------
os.makedirs(Config.DOWNLOAD_FOLDER, exist_ok=True)
os.makedirs(Config.OUTPUT_FOLDER, exist_ok=True)


# -----------------------------
# /start
# -----------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "👋 Welcome!\n\n"
        "📸 Send me a photo or image.\n\n"
    )

    await update.message.reply_text(text)


# -----------------------------
# Invalid messages
# -----------------------------
async def invalid(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "📸 Please send a photo."
    )


# -----------------------------
# Photo Handler
# -----------------------------
async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    input_path = None
    output_path = None

    # Show processing message
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

        logger.info(f"Input: {input_path}")
        logger.info(f"Output: {output_path}")

        # Download photo
        photo_file = await update.message.photo[-1].get_file()
        await photo_file.download_to_drive(input_path)

        logger.info("Photo downloaded.")

        # Edit image
        edit_image(input_path, output_path)

        logger.info("Image edited.")

        # Send edited image
        with open(output_path, "rb") as image:

            await update.message.reply_photo(
                photo=image,
                caption="✅ Your profile picture is ready!"
            )

        # Remove processing message
        await processing.delete()

        logger.info("Image sent.")

    except Exception:

        logger.exception("Error processing image")

        # Remove processing message if it still exists
        try:
            await processing.delete()
        except:
            pass

        await update.message.reply_text(
            "❌ Sorry, I couldn't process that image.\nPlease try another photo."
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

    if not Config.TOKEN:
        raise ValueError(
            "BOT_TOKEN is missing. Check your Railway Environment Variables."
        )

    app = ApplicationBuilder().token(Config.TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))

    # Photo messages
    app.add_handler(
        MessageHandler(
            filters.PHOTO,
            photo
        )
    )

    # Everything except photos and commands
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