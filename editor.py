import cv2
import os
from PIL import Image
from config import Config


CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)


def crop_square(img):

    width, height = img.size

    gray = cv2.cvtColor(
        cv2.imread(img.filename),
        cv2.COLOR_BGR2GRAY
    )

    faces = CASCADE.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5
    )

    size = min(width, height)

    if len(faces) > 0:

        x, y, w, h = faces[0]

        face_x = x + w // 2
        face_y = y + h // 2

    else:

        face_x = width // 2
        face_y = height // 2

    left = face_x - size // 2
    top = face_y - int(size * 0.35)

    left = max(0, min(left, width - size))
    top = max(0, min(top, height - size))

    return img.crop(
        (
            left,
            top,
            left + size,
            top + size
        )
    )


def edit_image(input_path, output_path):

    photo = Image.open(input_path).convert("RGBA")

    photo = crop_square(photo)

    photo = photo.resize(
        (1080, 1080),
        Image.LANCZOS
    )

    overlay = Image.open(
        Config.OVERLAY_PATH
    ).convert("RGBA")

    overlay = overlay.resize(
        (1080, 1080),
        Image.LANCZOS
    )

    final = Image.alpha_composite(
        photo,
        overlay
    )

    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True
    )

    final.convert("RGB").save(
        output_path,
        quality=100
    )