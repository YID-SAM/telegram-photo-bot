from PIL import Image, ImageDraw, ImageFont
from config import Config


def edit_image(input_path, output_path):

    img = Image.open(input_path).convert("RGBA")
    width, height = img.size

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Gradient overlay
    for y in range(height):
        alpha = int(Config.GRADIENT_ALPHA * (y / height))
        color = (*Config.GRADIENT_COLOR, alpha)

        draw.line([(0, y), (width, y)], fill=color)

    img = Image.alpha_composite(img, overlay)

    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype(Config.FONT_PATH, Config.FONT_SIZE)

    text = Config.TEXT

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]

    x = (width - text_width) // 2
    y = height - 150

    # shadow
    draw.text((x+2, y+2), text, font=font, fill="black")

    # main text
    draw.text((x, y), text, font=font, fill="white")

    img.convert("RGB").save(output_path)