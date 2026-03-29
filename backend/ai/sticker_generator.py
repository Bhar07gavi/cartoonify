import io
from PIL import Image, ImageDraw, ImageFont
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from rembg import remove

app = FastAPI()


# ================= TEXT FUNCTION =================

def add_text_to_sticker(image, text, x=None, y=None):

    if not text:
        return image

    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except:
        font = ImageFont.load_default()

    # fallback center
    if x is None or y is None:
        width, height = image.size
        bbox = draw.textbbox((0, 0), text, font=font)

        x = (width - (bbox[2]-bbox[0])) // 2
        y = (height - (bbox[3]-bbox[1])) // 2

    draw.text(
        (int(x), int(y)),
        text,
        fill="white",
        font=font,
        stroke_width=4,
        stroke_fill="black"
    )

    return image


# ================= STICKER GENERATOR =================

def generate_sticker(input_bytes, text="", x=None, y=None):

    # Load image
    img = Image.open(io.BytesIO(input_bytes)).convert("RGBA")

    # Remove background
    sticker = remove(img)

    # Resize (maintain aspect ratio)
    sticker.thumbnail((512, 512))   # ✅ correct usage

    # Create transparent 512x512 canvas
    final_img = Image.new("RGBA", (512, 512), (0, 0, 0, 0))

    # Center sticker
    paste_x = (512 - sticker.width) // 2
    paste_y = (512 - sticker.height) // 2

    final_img.paste(sticker, (paste_x, paste_y), sticker)

    # ✅ Adjust drag position relative to final canvas
    if x is not None and y is not None:
        x = int(x) + paste_x
        y = int(y) + paste_y

    # Add text
    final_img = add_text_to_sticker(final_img, text, x, y)

    # Save to memory
    output = io.BytesIO()
    final_img.save(output, format="WEBP")
    output.seek(0)

    return output


# ================= API =================

@app.post("/generate-sticker")
async def create_sticker(
    file: UploadFile = File(...),
    text: str = Form(""),
    x: str = Form(None),
    y: str = Form(None)
):

    image_bytes = await file.read()

    # safe conversion
    x = int(x) if x else None
    y = int(y) if y else None

    output = generate_sticker(
        image_bytes,
        text,
        x,
        y
    )

    return StreamingResponse(output, media_type="image/webp")