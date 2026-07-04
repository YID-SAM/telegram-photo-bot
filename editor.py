from PIL import Image
from config import Config


def crop_square(img):
    width, height = img.size

    size = min(width, height)

    left = (width - size) // 2
    top = (height - size) // 2
    right = left + size
    bottom = top + size

    return img.crop((left, top, right, bottom))


def edit_image(input_path, output_path):

    # Open user's image
    photo = Image.open(input_path).convert("RGBA")

    # Crop to square
    photo = crop_square(photo)

    # Resize to 1080 × 1080
    photo = photo.resize((1080, 1080), Image.LANCZOS)

    # Open overlay
    overlay = Image.open(Config.OVERLAY_PATH).convert("RGBA")

    # Resize overlay to exactly match the photo
    overlay = overlay.resize((1080, 1080), Image.LANCZOS)

    # Merge overlay directly on top of the photo
    final = Image.alpha_composite(photo, overlay)

    # Save
    final.convert("RGB").save(
        output_path,
        "JPEG",
        quality=100
    )