import io
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def add_text_to_sticker(image, text, x=None, y=None):
    """Add text overlay to sticker"""
    
    if not text:
        return image

    draw = ImageDraw.Draw(image)

    # Try different fonts
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
    except:
        try:
            font = ImageFont.truetype("arial.ttf", 60)
        except:
            font = ImageFont.load_default()

    # Center text if position not specified
    if x is None or y is None:
        width, height = image.size
        bbox = draw.textbbox((0, 0), text, font=font)
        x = (width - (bbox[2] - bbox[0])) // 2
        y = (height - (bbox[3] - bbox[1])) // 2

    # Draw text with outline
    draw.text(
        (int(x), int(y)),
        text,
        fill="white",
        font=font,
        stroke_width=4,
        stroke_fill="black"
    )

    return image


def remove_background_simple(img_array):
    """
    Simple background removal using GrabCut algorithm
    Works well for images with clear subject
    No AI needed - pure OpenCV
    """
    
    # Create mask
    mask = np.zeros(img_array.shape[:2], np.uint8)
    
    # Background and foreground models (required by GrabCut)
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)
    
    # Define a rectangle around the subject
    # Assume subject is in center 80% of image
    h, w = img_array.shape[:2]
    margin_w = int(w * 0.1)
    margin_h = int(h * 0.1)
    rect = (margin_w, margin_h, w - margin_w, h - margin_h)
    
    try:
        # Apply GrabCut algorithm
        cv2.grabCut(img_array, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
        
        # Create final mask (0 and 2 = background, 1 and 3 = foreground)
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        
        # Apply mask
        result = img_array * mask2[:, :, np.newaxis]
        
        # Create alpha channel
        alpha = mask2 * 255
        
        # Combine with alpha
        b, g, r = cv2.split(result)
        rgba = cv2.merge((r, g, b, alpha))
        
        return rgba
        
    except:
        # Fallback: simple color-based background removal
        # Convert to HSV
        hsv = cv2.cvtColor(img_array, cv2.COLOR_BGR2HSV)
        
        # Create mask for white/light backgrounds
        lower_white = np.array([0, 0, 200])
        upper_white = np.array([180, 30, 255])
        mask = cv2.inRange(hsv, lower_white, upper_white)
        
        # Invert mask (we want to keep the subject, not the background)
        mask = cv2.bitwise_not(mask)
        
        # Apply morphological operations to clean up
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        
        # Create RGBA
        b, g, r = cv2.split(img_array)
        rgba = cv2.merge((r, g, b, mask))
        
        return rgba


def generate_sticker(input_bytes, text="", x=None, y=None):
    """
    Generate sticker using OpenCV only (no AI models)
    - GrabCut for background removal
    - Text overlay
    - Returns WebP format
    """
    
    # Decode image
    img_array = np.frombuffer(input_bytes, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    
    if img is None:
        raise ValueError("Invalid image")
    
    # Remove background
    img_rgba = remove_background_simple(img)
    
    # Convert to PIL
    img_pil = Image.fromarray(img_rgba, mode='RGBA')
    
    # Resize to thumbnail (maintain aspect ratio)
    img_pil.thumbnail((512, 512), Image.Resampling.LANCZOS)
    
    # Create 512x512 transparent canvas
    final_img = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    
    # Center the sticker
    paste_x = (512 - img_pil.width) // 2
    paste_y = (512 - img_pil.height) // 2
    
    final_img.paste(img_pil, (paste_x, paste_y), img_pil)
    
    # Adjust text position relative to final canvas
    if x is not None and y is not None:
        x = int(x) + paste_x
        y = int(y) + paste_y
    
    # Add text
    final_img = add_text_to_sticker(final_img, text, x, y)
    
    # Save to memory as WebP
    output = io.BytesIO()
    final_img.save(output, format="WEBP", quality=90)
    output.seek(0)
    
    return output


# Optional: Make it runnable standalone for testing
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'rb') as f:
            img_bytes = f.read()
        
        result = generate_sticker(img_bytes, "TEST", None, None)
        
        with open("test_sticker.webp", 'wb') as f:
            f.write(result.read())
        
        print("✅ Test sticker saved as test_sticker.webp")
