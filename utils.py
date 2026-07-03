import os
from uuid import uuid4
from config import Config


def generate_paths():
    uid = uuid4().hex

    input_path = os.path.join(
        Config.DOWNLOAD_FOLDER,
        f"{uid}.jpg"
    )

    output_path = os.path.join(
        Config.OUTPUT_FOLDER,
        f"{uid}.jpg"
    )

    return input_path, output_path