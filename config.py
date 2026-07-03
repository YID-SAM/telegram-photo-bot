import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    TOKEN = os.getenv("BOT_TOKEN")

    DOWNLOAD_FOLDER = "downloads"
    OUTPUT_FOLDER = "output"

    FONT_PATH = os.path.join(
        "fonts",
        "NotoSansEthiopic-Regular.ttf"
    )

    TEXT = "እኔም እገኛለሁ"

    FONT_SIZE = 70

    GRADIENT_COLOR = (120, 30, 255)
    GRADIENT_ALPHA = 120