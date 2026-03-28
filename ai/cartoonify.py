import cv2
import numpy as np

def cartoonify_image(file_bytes, style="classic"):
    """
    Cartoonify using OpenCV effects only (no AI models)
    """
    
    # Decode image
    img_array = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    
    if img is None:
        raise ValueError("Invalid image")
    
    h, w = img.shape[:2]
    
    # Apply different cartoon effects based on style
    if style in ["classic", "hayao"]:
        output = cartoon_effect_bilateral(img)
        
    elif style in ["anime", "paprika"]:
        output = cartoon_effect_anime(img)
        
    elif style in ["comic"]:
        output = cartoon_effect_comic(img)
        
    elif style in ["sketch"]:
        output = sketch_effect(img)
        
    elif style in ["watercolor", "shinkai"]:
        output = watercolor_effect(img)
        
    elif style == "minimal":
        output = minimal_effect(img)
        
    else:
        # Default cartoon effect
        output = cartoon_effect_bilateral(img)
    
    # Encode and return
    success, encoded = cv2.imencode(".jpg", output)
    
    if not success:
        raise ValueError("Encoding failed")
    
    return encoded.tobytes()


def cartoon_effect_bilateral(img):
    """Classic cartoon - bilateral filter + edge detection"""
    
    # Downsample for speed
    img_small = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
    
    # Apply bilateral filter multiple times for smoothing
    for _ in range(5):
        img_small = cv2.bilateralFilter(img_small, d=9, sigmaColor=75, sigmaSpace=75)
    
    # Upsample back
    img_smooth = cv2.resize(img_small, (img.shape[1], img.shape[0]))
    
    # Edge detection
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.medianBlur(gray, 7)
    edges = cv2.adaptiveThreshold(
        gray_blur, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        blockSize=9,
        C=2
    )
    
    # Convert edges to color
    edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    
    # Combine smooth image with edges
    cartoon = cv2.bitwise_and(img_smooth, edges_colored)
    
    return cartoon


def cartoon_effect_anime(img):
    """Anime style - posterization + strong edges"""
    
    # Color quantization (posterize)
    data = np.float32(img).reshape((-1, 3))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    _, labels, centers = cv2.kmeans(data, 8, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    quantized = centers[labels.flatten()].reshape(img.shape)
    
    # Strong edge detection
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    edges = cv2.dilate(edges, None)
    edges_inv = cv2.bitwise_not(edges)
    edges_colored = cv2.cvtColor(edges_inv, cv2.COLOR_GRAY2BGR)
    
    # Combine
    result = cv2.bitwise_and(quantized, edges_colored)
    
    return result


def cartoon_effect_comic(img):
    """Comic book style - halftone + thick outlines"""
    
    # Increase saturation
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv[:, :, 1] = cv2.convertScaleAbs(hsv[:, :, 1], alpha=1.5, beta=0)
    img_saturated = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    # Posterize
    img_posterized = img_saturated // 64 * 64
    
    # Thick edges
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    edges = cv2.dilate(edges, np.ones((3, 3), np.uint8), iterations=1)
    edges_inv = cv2.bitwise_not(edges)
    edges_colored = cv2.cvtColor(edges_inv, cv2.COLOR_GRAY2BGR)
    
    result = cv2.bitwise_and(img_posterized, edges_colored)
    
    return result


def sketch_effect(img):
    """Pencil sketch effect"""
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inverted = 255 - gray
    blur = cv2.GaussianBlur(inverted, (21, 21), 0)
    inverted_blur = 255 - blur
    sketch = cv2.divide(gray, inverted_blur, scale=256.0)
    sketch = cv2.convertScaleAbs(sketch, alpha=1.2, beta=-12)
    
    return cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)


def watercolor_effect(img):
    """Watercolor painting style"""
    
    # Apply bilateral filter for smoothing while keeping edges
    result = cv2.bilateralFilter(img, 9, 75, 75)
    
    # Apply edge preserving filter
    result = cv2.edgePreservingFilter(result, flags=1, sigma_s=60, sigma_r=0.4)
    
    # Add slight blur for watercolor look
    result = cv2.GaussianBlur(result, (5, 5), 0)
    
    return result


def minimal_effect(img):
    """Minimal/flat design style - few colors"""
    
    # Heavy quantization
    Z = img.reshape((-1, 3))
    Z = np.float32(Z)
    
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, label, center = cv2.kmeans(Z, 6, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    
    center = np.uint8(center)
    res = center[label.flatten()]
    result = res.reshape((img.shape))
    
    # Smooth
    result = cv2.bilateralFilter(result, 15, 80, 80)
    
    return result


# For compatibility with old code
def apply_filter(image, filter_type):
    """Apply color filters"""
    
    if filter_type == "bw":
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    elif filter_type == "invert":
        return cv2.bitwise_not(image)
    
    elif filter_type == "vintage":
        kernel = np.array([
            [0.272, 0.534, 0.131],
            [0.349, 0.686, 0.168],
            [0.393, 0.769, 0.189]
        ])
        return cv2.transform(image, kernel)
    
    elif filter_type == "infrared":
        b, g, r = cv2.split(image)
        return cv2.merge((r, g, b))
    
    return image
