import os
import asyncio
from telegram import Update
from telegram.ext import ContextTypes

from editor import edit_image
from utils import generate_paths
from logger import logger


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📷 Send me a photo and I'll transform it."
    )


async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    input_path, output_path = generate_paths()

    try:
        # Download image
        photo_file = await update.message.photo[-1].get_file()
        await photo_file.download_to_drive(input_path)

        logger.info(f"Downloaded: {input_path}")

        # Edit image
        await asyncio.to_thread(edit_image, input_path, output_path)

        logger.info(f"Edited: {output_path}")

        # IMPORTANT FIX: read file as bytes BEFORE sending
        with open(output_path, "rb") as f:
            image_bytes = f.read()

        await update.message.reply_photo(photo=image_bytes)

        logger.info("Image sent successfully")

    except Exception as e:
        logger.exception(e)
        await update.message.reply_text("❌ Error processing image")

    finally:
        if os.path.exists(input_path):
            os.remove(input_path)

        if os.path.exists(output_path):
            os.remove(output_path)

        logger.info("Cleaned temporary files")