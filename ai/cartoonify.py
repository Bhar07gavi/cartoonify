import os
import cv2
import numpy as np
import onnxruntime as ort

BASE_DIR = os.path.dirname(__file__)
MODEL_DIR = os.path.join(BASE_DIR, "models")

MODEL_PATHS = {
    "hayao": os.path.join(MODEL_DIR, "hayao.onnx"),
    "paprika": os.path.join(MODEL_DIR, "paprika.onnx"),
    "shinkai": os.path.join(MODEL_DIR, "shinkai.onnx"),
}

# UI style → model
STYLE_MODEL_MAP = {
    "classic": "hayao",
    "anime": "hayao",
    "comic": "paprika",
    "watercolor": "shinkai",
    "minimal": "shinkai",

    # allow direct model names
    "hayao": "hayao",
    "paprika": "paprika",
    "shinkai": "shinkai"
}

print("\n---- Cartoonify Ready (Lazy Loading) ----\n")

# ✅ Don't load models at startup - load on demand
sessions = {}
model_sizes = {}

def load_model_if_needed(model_name):
    """Load model only when first requested"""
    
    if model_name in sessions:
        print(f"✅ Using cached model: {model_name}")
        return sessions[model_name]
    
    path = MODEL_PATHS.get(model_name)
    
    if not path or not os.path.exists(path):
        raise ValueError(f"Model not found: {model_name}")
    
    print(f"📥 Loading model: {model_name} from {path}")
    
    # Load model
    session = ort.InferenceSession(
        path, 
        providers=["CPUExecutionProvider"]
    )
    
    input_shape = session.get_inputs()[0].shape
    model_sizes[model_name] = 512 if 512 in input_shape else 256
    sessions[model_name] = session
    
    print(f"✅ Loaded: {model_name}, Input shape: {input_shape}")
    
    return session


def cartoonify_image(file_bytes, style="classic"):

    ui_style = style.lower()

    # decode image
    img_array = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    if img is None:
        raise ValueError("Invalid image")

    original_img = img.copy()

    # --------------------------------
    # SKETCH STYLE (skip AI model)
    # --------------------------------
    if ui_style == "sketch":

        gray = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)

        # invert image
        inverted = 255 - gray

        # blur the inverted image
        blur = cv2.GaussianBlur(inverted, (21,21), 0)

        # invert blurred
        inverted_blur = 255 - blur

        # color dodge blend
        sketch = cv2.divide(gray, inverted_blur, scale=256.0)

        # enhance pencil lines
        sketch = cv2.convertScaleAbs(sketch, alpha=1.2, beta=-12)

        output = cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)

        success, encoded = cv2.imencode(".jpg", output)

        if not success:
            raise ValueError("Encoding failed")

        return encoded.tobytes()

    # --------------------------------
    # AI MODEL CARTOON STYLES
    # --------------------------------

    model_name = STYLE_MODEL_MAP.get(ui_style, "hayao")

    print("UI Style:", ui_style, "→ Model:", model_name)

    # ✅ Load model only now (lazy loading)
    session = load_model_if_needed(model_name)
    
    h, w = img.shape[:2]
    original_size = (w, h)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    model_size = model_sizes[model_name]
    img = cv2.resize(img, (model_size, model_size))

    # normalize
    img = img.astype(np.float32) / 127.5 - 1.0
    input_img = np.expand_dims(img, axis=0)

    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name

    result = session.run([output_name], {input_name: input_img})

    output = result[0][0]

    output = (output + 1) * 127.5
    output = np.clip(output, 0, 255).astype(np.uint8)

    output = cv2.cvtColor(output, cv2.COLOR_RGB2BGR)
    output = cv2.resize(output, original_size)

    # --------------------------------
    # STYLE EFFECTS
    # --------------------------------

    if ui_style == "minimal":

        output = cv2.bilateralFilter(output, 15, 80, 80)

        Z = output.reshape((-1, 3))
        Z = np.float32(Z)

        K = 8

        _, label, center = cv2.kmeans(
            Z,
            K,
            None,
            (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0),
            10,
            cv2.KMEANS_RANDOM_CENTERS
        )

        center = np.uint8(center)
        res = center[label.flatten()]
        output = res.reshape((output.shape))

    elif ui_style == "comic":

        output = cv2.convertScaleAbs(output, alpha=1.25, beta=15)

    elif ui_style == "watercolor":

        output = cv2.edgePreservingFilter(output, flags=1, sigma_s=60, sigma_r=0.4)

    # --------------------------------
    # ENCODE RESULT
    # --------------------------------

    success, encoded = cv2.imencode(".jpg", output)

    if not success:
        raise ValueError("Encoding failed")

    return encoded.tobytes()


# --------------------------------
# EXTRA FILTERS
# --------------------------------

def apply_filter(image, filter_type):

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
