import os
import io
import cv2
import time
import shutil
import tempfile
import subprocess
import numpy as np
import streamlit as st
import ui.components as _comp
from PIL import Image
from urllib.request import urlopen, Request
from urllib.error import URLError
from ui.styles import inject_styles
from ui.components import navbar, left_panel_controls
from cartoon import cartoon, sketch, pencil
from auth import create_user_table, signup_user, login_user

# Optional: image comparison
try:
    from streamlit_image_comparison import image_comparison
    CMP_OK = True
except Exception:
    CMP_OK = False

# Optional ONNX runtime (for AnimeGAN)
try:
    import onnxruntime as ort
    ONNX_OK = True
except Exception:
    ONNX_OK = False

# AnimeGAN import
try:
    from animegan import AnimeGAN, ANIME_MODEL_PATH
    ANIME_OK = True
except Exception:
    ANIME_OK = False


# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="AI Toonify • Studio",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_styles()


# -----------------------------
# Session State
# -----------------------------
def init_state():
    st.session_state.setdefault("history", [])
    st.session_state.setdefault("last_out_image_bgr", None)
    st.session_state.setdefault("last_out_video_path", None)

    st.session_state.setdefault("logged_in", False)
    st.session_state.setdefault("username", "")

    st.session_state.setdefault("paid", False)
    st.session_state.setdefault("_url_video_path", None)


init_state()
create_user_table()


# -----------------------------
# Models & Paths
# -----------------------------
ANIME_MODEL_FILE = os.path.join("models", "animeganv2.onnx")


@st.cache_resource
def load_anime_model():
    if not (ONNX_OK and ANIME_OK):
        raise RuntimeError("AnimeGAN not available. Install onnxruntime and keep animegan.py.")
    model_path = ANIME_MODEL_FILE if os.path.exists(ANIME_MODEL_FILE) else ANIME_MODEL_PATH
    if not os.path.exists(model_path):
        raise RuntimeError(f"AnimeGAN model not found: {model_path}")
    return AnimeGAN(model_path=model_path)


# -----------------------------
# Helpers
# -----------------------------
def bgr_to_rgb(bgr):
    return cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)


def rgb_to_bgr(rgb):
    return cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)


def read_image_bytes(file_bytes) -> np.ndarray:
    pil = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    return np.array(pil)


def resize_max_side(img_rgb, max_side=1024):
    h, w = img_rgb.shape[:2]
    m = max(h, w)
    if m <= max_side:
        return img_rgb
    scale = max_side / float(m)
    nh, nw = int(h * scale), int(w * scale)
    return cv2.resize(img_rgb, (nw, nh), interpolation=cv2.INTER_AREA)


def push_history(item):
    hist = st.session_state.get("history", [])
    hist.insert(0, item)
    st.session_state["history"] = hist[:20]


def download_button_bytes(label, data: bytes, filename: str, mime: str):
    st.download_button(label, data=data, file_name=filename, mime=mime, use_container_width=True)


def file_bytes_from_path(path):
    with open(path, "rb") as f:
        return f.read()


def safe_temp_path(suffix):
    fd, p = tempfile.mkstemp(suffix=suffix)
    os.close(fd)
    return p


def ffmpeg_exists():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False


def ensure_mp4(input_path, out_path):
    if input_path.lower().endswith(".mp4"):
        shutil.copy(input_path, out_path)
        return out_path
    if not ffmpeg_exists():
        raise RuntimeError("ffmpeg not found. Please install ffmpeg to convert videos.")
    cmd = [
        "ffmpeg", "-y", "-i", input_path,
        "-c:v", "libx264", "-preset", "fast", "-crf", "22",
        "-c:a", "aac", out_path
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return out_path


def fetch_video_from_url(url: str) -> str:
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    data = urlopen(req, timeout=40).read()
    temp_in = safe_temp_path(".mp4")
    with open(temp_in, "wb") as f:
        f.write(data)
    return temp_in


# -----------------------------
# Filters
# -----------------------------
def _clamp01(x):
    return max(0.0, min(1.0, x))


def apply_post_filter(bgr, name="None", intensity=45, edge_strength=35):
    if name == "None":
        return bgr

    I = _clamp01(intensity / 100.0)
    E = _clamp01(edge_strength / 100.0)
    out = bgr.copy()

    if name == "Vivid":
        out = cv2.convertScaleAbs(out, alpha=1.0 + 0.45 * I, beta=int(8 * I))
        hsv = cv2.cvtColor(out, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[..., 1] *= (1.0 + 0.55 * I)
        hsv[..., 1] = np.clip(hsv[..., 1], 0, 255)
        out = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
        return out

    if name == "Warm":
        b, g, r = cv2.split(out)
        r = cv2.add(r, np.uint8(30 * I))
        b = cv2.subtract(b, np.uint8(15 * I))
        return cv2.merge([b, g, r])

    if name == "Cool":
        b, g, r = cv2.split(out)
        b = cv2.add(b, np.uint8(28 * I))
        r = cv2.subtract(r, np.uint8(12 * I))
        return cv2.merge([b, g, r])

    if name == "Sepia":
        kernel = np.array([
            [0.272, 0.534, 0.131],
            [0.349, 0.686, 0.168],
            [0.393, 0.769, 0.189]
        ], dtype=np.float32)
        sep = cv2.transform(out, kernel)
        sep = np.clip(sep, 0, 255).astype(np.uint8)
        return cv2.addWeighted(out, 1.0 - I, sep, I, 0)

    if name == "Sharpen":
        blur = cv2.GaussianBlur(out, (0, 0), sigmaX=1.2)
        sharp = cv2.addWeighted(out, 1.0 + 1.2 * I, blur, -1.2 * I, 0)
        return sharp

    if name == "Posterize":
        levels = int(10 - 7 * I)  # 10 -> 3
        levels = max(3, levels)
        step = 256 // levels
        return (out // step) * step

    if name == "Pixelate":
        h, w = out.shape[:2]
        scale = int(16 - 12 * I)  # 16 -> 4
        scale = max(4, scale)
        small = cv2.resize(out, (w // scale, h // scale), interpolation=cv2.INTER_AREA)
        return cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)

    if name == "Vignette":
        h, w = out.shape[:2]
        kx = cv2.getGaussianKernel(w, w * (0.28 + 0.10 * (1 - I)))
        ky = cv2.getGaussianKernel(h, h * (0.28 + 0.10 * (1 - I)))
        mask = (ky @ kx.T)
        mask = mask / mask.max()
        strength = 0.55 * I
        vign = out.astype(np.float32)
        vign[..., 0] *= (1 - strength) + strength * mask
        vign[..., 1] *= (1 - strength) + strength * mask
        vign[..., 2] *= (1 - strength) + strength * mask
        return np.clip(vign, 0, 255).astype(np.uint8)

    if name == "Comic Ink":
        gray = cv2.cvtColor(out, cv2.COLOR_BGR2GRAY)
        gray_blur = cv2.GaussianBlur(gray, (0, 0), 1.2)
        edges = cv2.Canny(gray_blur, int(60 + 120 * E), int(120 + 180 * E))
        edges = cv2.dilate(edges, np.ones((2, 2), np.uint8), iterations=1)
        edges_inv = cv2.bitwise_not(edges)
        base = apply_post_filter(out, "Posterize", intensity=70, edge_strength=edge_strength)
        return cv2.bitwise_and(base, base, mask=edges_inv)

    if name == "Neon Glow":
        gray = cv2.cvtColor(out, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, int(50 + 140 * E), int(120 + 200 * E))
        edges = cv2.GaussianBlur(edges, (0, 0), 2.0 + 2.5 * I)
        glow = cv2.applyColorMap(edges, cv2.COLORMAP_TURBO)
        glow = cv2.convertScaleAbs(glow, alpha=1.1, beta=0)
        return cv2.addWeighted(out, 1.0, glow, 0.65 * I, 0)

    return out


# -----------------------------
# Processing
# -----------------------------
def process_image(img_rgb, style, smooth=35, brighten=8):
    img_bgr = rgb_to_bgr(img_rgb)

    if smooth > 0:
        s = max(1, smooth // 5)
        img_bgr = cv2.bilateralFilter(img_bgr, d=0, sigmaColor=30 + s * 2, sigmaSpace=30 + s * 2)

    if brighten != 0:
        img_bgr = cv2.convertScaleAbs(img_bgr, alpha=1.05, beta=int(brighten))

    img_rgb2 = bgr_to_rgb(img_bgr)

    if style == "Cartoon":
        out_bgr = cartoon(img_rgb2)
    elif style == "Sketch":
        out_bgr = sketch(img_rgb2)
    elif style == "Pencil":
        out_bgr = pencil(img_rgb2)
    elif style == "AnimeGAN":
        model = load_anime_model()
        out_rgb = model.infer(img_rgb2)
        out_bgr = rgb_to_bgr(out_rgb)
    else:
        out_bgr = img_bgr

    return out_bgr


def process_video(in_path, style, smooth=35, brighten=8, post_filter="None", intensity=45, edge_strength=35):
    cap = cv2.VideoCapture(in_path)
    if not cap.isOpened():
        raise RuntimeError("Could not open video.")

    fps = cap.get(cv2.CAP_PROP_FPS) or 24
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 640)
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 360)

    out_path = safe_temp_path(".mp4")
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(out_path, fourcc, fps, (w, h))

    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    prog = st.progress(0, text="Processing video...")

    i = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break

        frame_rgb = bgr_to_rgb(frame)
        out_bgr = process_image(frame_rgb, style, smooth=smooth, brighten=brighten)
        out_bgr = apply_post_filter(out_bgr, post_filter, intensity, edge_strength)
        out_bgr = cv2.resize(out_bgr, (w, h), interpolation=cv2.INTER_AREA)
        writer.write(out_bgr)

        i += 1
        if total > 0 and i % 3 == 0:
            prog.progress(min(i / total, 1.0), text=f"Processing video... {i}/{total}")

    cap.release()
    writer.release()
    prog.empty()
    return out_path


# -----------------------------
# Auth Page
# -----------------------------
def auth_page():
    c1, c2, c3 = st.columns([1.4, 1.2, 1.4])
    with c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        st.markdown("""
<div class="brand">
  <div class="brand-badge">AI</div>
</div>
<div class="brand-title">AI Toonify</div>
<div class="brand-sub">Creator Studio • Transform media into art</div>

<div class="float-sprite s1">🧚‍♀️</div>
<div class="float-sprite s2">⭐</div>
<div class="float-sprite s3">✨</div>
<div class="float-sprite s4">🎨</div>
""", unsafe_allow_html=True)

        st.markdown('<div class="login-wrap">', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["Sign In", "Create Account"])

        with tab1:
            u = st.text_input("Username", key="login_user")
            p = st.text_input("Password", type="password", key="login_pass")

            if st.button("✨ Sign In"):
                ok = login_user(u, p)
                if ok:
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = u
                    st.toast("Signed in ✅")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

            st.markdown('<div class="helper">Demo: enter any username/password (2+ chars)</div>', unsafe_allow_html=True)

        with tab2:
            su = st.text_input("New Username", key="signup_user")
            sp = st.text_input("New Password", type="password", key="signup_pass")
            if st.button("🚀 Create Account"):
                ok = signup_user(su, sp)
                if ok:
                    st.success("Account created! Please sign in.")
                else:
                    st.error("Username already exists or invalid.")

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------
# Main App
# -----------------------------
def app_page():
    navbar()

    controls = left_panel_controls(ONNX_OK, ANIME_OK, ANIME_MODEL_FILE)

    # ✅ Safe unpack
    if isinstance(controls, tuple) and len(controls) == 7:
        mode, style, smooth, brighten, post_filter, intensity, edge_strength = controls
    else:
        mode, style, smooth, brighten = controls
        post_filter, intensity, edge_strength = "None", 45, 35

    st.markdown("## ✨ Studio")
    colA, colB = st.columns([1.0, 1.0], gap="large")
    
    # =========================
    # IMAGE MODE
    # =========================
    if mode == "Image":
        with colA:
            st.markdown("### 📷 Upload Image")
            up = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"], label_visibility="collapsed")

            img_rgb = None
            if up:
                img_rgb = read_image_bytes(up.read())
                img_rgb = resize_max_side(img_rgb, 1024)
                st.image(img_rgb, caption="Original", use_container_width=True)

        with colB:
            st.markdown("### 🎨 Output")

            if up:
                with st.spinner("Generating..."):
                    out_bgr = process_image(img_rgb, style, smooth=smooth, brighten=brighten)
                    out_bgr = apply_post_filter(out_bgr, post_filter, intensity, edge_strength)

                out_rgb = bgr_to_rgb(out_bgr)
                st.image(out_rgb, caption=f"Result • {style}", use_container_width=True)

                if CMP_OK:
                    st.markdown("#### Before / After")
                    image_comparison(
                        img1=Image.fromarray(img_rgb),
                        img2=Image.fromarray(out_rgb),
                        label1="Before",
                        label2="After",
                    )

                buf = io.BytesIO()
                Image.fromarray(out_rgb).save(buf, format="PNG")
                download_button_bytes("⬇️ Download PNG", buf.getvalue(), "toonify.png", "image/png")
                push_history({"type": "image", "style": style, "time": time.time(), "png": buf.getvalue()})
            else:
                st.info("Upload an image to see output.")

    # =========================
    # VIDEO MODE (Upload + URL + Camera)
    # =========================
    else:
        in_path = None
        snapshot_img_rgb = None
        input_kind = None  # "video" or "snapshot"

        with colA:
            st.markdown("### 🎬 Video Input")
            tab_upload, tab_url, tab_cam = st.tabs(["Upload File", "From URL", "Live Camera"])

            with tab_upload:
                upv = st.file_uploader("Upload video", type=["mp4", "mov", "avi", "mkv"], label_visibility="collapsed")
                if upv:
                    temp_in = safe_temp_path(os.path.splitext(upv.name)[1])
                    with open(temp_in, "wb") as f:
                        f.write(upv.read())
                    in_path = temp_in
                    input_kind = "video"
                    st.video(in_path)

            with tab_url:
                url = st.text_input("Paste direct MP4 URL", placeholder="https://.../video.mp4")
                if st.button("⬇️ Fetch Video"):
                    if not url or (not url.startswith("http")):
                        st.error("Please paste a valid URL.")
                    else:
                        try:
                            with st.spinner("Downloading video..."):
                                in_path = fetch_video_from_url(url)
                            st.session_state["_url_video_path"] = in_path
                            input_kind = "video"
                            st.success("Downloaded ✅")
                            st.video(in_path)
                        except URLError as e:
                            st.error(f"URL error: {e}")
                        except Exception as e:
                            st.error(f"Failed to fetch video: {e}")

                cached = st.session_state.get("_url_video_path")
                if (not in_path) and cached and os.path.exists(cached):
                    st.caption("Using last downloaded URL video.")
                    in_path = cached
                    input_kind = "video"
                    st.video(in_path)

            with tab_cam:
                st.caption("Streamlit camera gives snapshot. Real-time live video needs streamlit-webrtc.")
                cam_img = st.camera_input("Open Camera")
                if cam_img:
                    snapshot_img_rgb = read_image_bytes(cam_img.getvalue())
                    snapshot_img_rgb = resize_max_side(snapshot_img_rgb, 1024)
                    input_kind = "snapshot"
                    st.image(snapshot_img_rgb, caption="Camera Snapshot", use_container_width=True)

        with colB:
            st.markdown("### 🎞️ Output")

            # Camera snapshot => image flow (no payment lock)
            if input_kind == "snapshot" and snapshot_img_rgb is not None:
                with st.spinner("Generating..."):
                    out_bgr = process_image(snapshot_img_rgb, style, smooth=smooth, brighten=brighten)
                    out_bgr = apply_post_filter(out_bgr, post_filter, intensity, edge_strength)

                out_rgb = bgr_to_rgb(out_bgr)
                st.image(out_rgb, caption=f"Result • {style}", use_container_width=True)

                buf = io.BytesIO()
                Image.fromarray(out_rgb).save(buf, format="PNG")
                download_button_bytes("⬇️ Download PNG", buf.getvalue(), "camera_toonify.png", "image/png")
                push_history({"type": "image", "style": style, "time": time.time(), "png": buf.getvalue()})

            # Video upload/url
            elif input_kind == "video" and in_path:
                if not st.session_state.get("paid", False):
                    st.warning("Video processing is demo-locked. Mark Paid ✅ from sidebar.")
                else:
                    if st.button("✨ Process Video"):
                        with st.spinner("Processing video..."):
                            out_path = process_video(
                                in_path,
                                style,
                                smooth=smooth,
                                brighten=brighten,
                                post_filter=post_filter,
                                intensity=intensity,
                                edge_strength=edge_strength,
                            )
                        st.session_state["last_out_video_path"] = out_path
                        st.success("Done ✅")
                        st.video(out_path)
                        download_button_bytes("⬇️ Download MP4", file_bytes_from_path(out_path), "toonify.mp4", "video/mp4")
                        push_history({"type": "video", "style": style, "time": time.time(), "path": out_path})
            else:
                st.info("Choose Upload / URL / Camera to see output.")

    # =========================
    # History
    # =========================
    st.markdown("## 🕘 History (last 20)")
    hist = st.session_state.get("history", [])
    if not hist:
        st.caption("No history yet.")
        return

    for idx, item in enumerate(hist):
        if item["type"] == "image":
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.write(f"**Image** • Style: `{item['style']}`")
            st.image(Image.open(io.BytesIO(item["png"])), use_container_width=True)
            download_button_bytes("⬇️ Download", item["png"], f"toonify_{idx}.png", "image/png")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.write(f"**Video** • Style: `{item['style']}`")
            if os.path.exists(item["path"]):
                st.video(item["path"])
                download_button_bytes("⬇️ Download", file_bytes_from_path(item["path"]), f"toonify_{idx}.mp4", "video/mp4")
            else:
                st.caption("Video file expired (temp).")
            st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------
# Router
# -----------------------------
if not st.session_state.get("logged_in", False):
    auth_page()
else:
    app_page()