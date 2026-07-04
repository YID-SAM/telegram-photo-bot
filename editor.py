import os
from PIL import Image, ImageDraw, ImageFont
from config import Config


def edit_image(input_path, output_path):
    """Edit an image by adding a gradient overlay and centered text."""

    # Check input file exists
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input image not found: {input_path}")

    # Check font exists
    if not os.path.exists(Config.FONT_PATH):
        raise FileNotFoundError(f"Font file not found: {Config.FONT_PATH}")

    # Open image
    img = Image.open(input_path).convert("RGBA")
    width, height = img.size

    # Create transparent overlay
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)

    # Draw vertical gradient
    for y in range(height):
        alpha = int(Config.GRADIENT_ALPHA * (y / height))
        color = (
            Config.GRADIENT_COLOR[0],
            Config.GRADIENT_COLOR[1],
            Config.GRADIENT_COLOR[2],
            alpha
        )

        overlay_draw.line([(0, y), (width, y)], fill=color)

    # Merge overlay
    img = Image.alpha_composite(img, overlay)

    draw = ImageDraw.Draw(img)

    # Load font
    font = ImageFont.truetype(
        Config.FONT_PATH,
        Config.FONT_SIZE
    )

    text = Config.TEXT

    # Calculate text position
    bbox = draw.textbbox((0, 0), text, font=font)

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (width - text_width) // 2
    y = height - text_height - 80

    # Draw shadow
    draw.text(
        (x + 3, y + 3),
        text,
        font=font,
        fill=(0, 0, 0)
    )

    # Draw text
    draw.text(
        (x, y),
        text,
        font=font,
        fill=(255, 255, 255)
    )

    # Make sure output folder exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save image
    img.convert("RGB").save(output_path, "JPEG", quality=95)