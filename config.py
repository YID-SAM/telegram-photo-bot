import os
from dotenv import load_dotenv


load_dotenv()


class Config:
    # Telegram Bot Token
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    # Project folders
    DOWNLOAD_FOLDER = "downloads"
    OUTPUT_FOLDER = "output"
    OVERLAY_PATH = "assets/overlay.png"
    LOG_FOLDER = "logs"

    # Font
    FONT_PATH = os.path.join(
        "fonts",
        "NotoSansEthiopic-Regular.ttf"
    )

    # Text
    TEXT = "እኔም እገኛለሁ"
    FONT_SIZE = 70

    # Gradient
    GRADIENT_COLOR = (120, 30, 255)
    GRADIENT_ALPHA = 120