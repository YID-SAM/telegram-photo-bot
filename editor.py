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

    # Resize to 1080x1080
    photo = photo.resize((1080, 1080), Image.LANCZOS)

    # Load overlay
    overlay = Image.open(Config.OVERLAY_PATH).convert("RGBA")

    # Resize overlay
    overlay = overlay.resize((1080, 1080), Image.LANCZOS)

    # Create transparent canvas
    overlay_canvas = Image.new("RGBA", (1080, 1080), (0, 0, 0, 0))

    # ==========================
    # Move overlay DOWN
    # Increase this value if needed
    # ==========================
    OVERLAY_OFFSET_Y = 40

    overlay_canvas.paste(
        overlay,
        (0, OVERLAY_OFFSET_Y),
        overlay
    )

    # Merge overlay with photo
    final = Image.alpha_composite(
        photo,
        overlay_canvas
    )

    # Save
    final.convert("RGB").save(
        output_path,
        "JPEG",
        quality=100
    )