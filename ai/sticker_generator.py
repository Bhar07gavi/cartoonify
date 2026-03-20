import io
from PIL import Image, ImageDraw, ImageFont
from rembg import remove


def add_text_to_sticker(image, text, position="top"):
    """
    Adds meme-style text to sticker
    """

    if not text:
        return image

    draw = ImageDraw.Draw(image)

    width, height = image.size

    # Try loading font
    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except:
        font = ImageFont.load_default()

    # Calculate text size
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Position
    if position == "top":
        x = (width - text_width) // 2
        y = 20
    else:
        x = (width - text_width) // 2
        y = height - text_height - 20

    # Outline (meme style)
    draw.text(
        (x, y),
        text,
        fill="white",
        font=font,
        stroke_width=4,
        stroke_fill="black"
    )

    return image


def generate_sticker(input_bytes, text="", position="top"):
    """
    Main sticker generator
    """

    # Load image
    img = Image.open(io.BytesIO(input_bytes)).convert("RGBA")

    # Remove background
    sticker = remove(img)

    # Resize for WhatsApp sticker size
    sticker = sticker.resize((512, 512))

    # Add text
    sticker = add_text_to_sticker(sticker, text, position)

    # Save to memory
    output = io.BytesIO()

    sticker.save(output, format="WEBP")

    output.seek(0)

    return output