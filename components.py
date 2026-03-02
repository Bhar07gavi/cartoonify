import streamlit as st


def navbar():
    username = st.session_state.get("username", "")
    paid = st.session_state.get("paid", False)

    st.markdown(
        f"""
<div class="navbar">
  <div class="nav-left">
    <div class="nav-logo">AI</div>
    <div>
      <p class="nav-title">AI Toonify</p>
      <p class="nav-sub">Creator Studio • Transform media into art</p>
    </div>
  </div>
  <div class="nav-right">
    <div class="pill">User: {username if username else "Guest"}</div>
    <div class="pill">Plan: {"Premium" if paid else "Free"}</div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def left_panel_controls(ONNX_OK=False, ANIME_OK=False, ANIME_MODEL_FILE=""):
    st.sidebar.markdown("### 🎛️ Studio Controls")

    # --- Mode
    st.sidebar.markdown('<div class="panel">', unsafe_allow_html=True)
    st.sidebar.write("**Mode**")
    mode = st.sidebar.radio(
        "Choose mode",
        ["Image", "Video"],
        label_visibility="collapsed",
        horizontal=True,
    )
    st.sidebar.markdown("</div>", unsafe_allow_html=True)

    # --- Style
    st.sidebar.markdown('<div class="panel">', unsafe_allow_html=True)
    st.sidebar.write("**Style**")
    style = st.sidebar.selectbox(
        "Style",
        ["Cartoon", "Sketch", "Pencil", "AnimeGAN"],
        index=0,
        label_visibility="collapsed",
    )
    st.sidebar.markdown("</div>", unsafe_allow_html=True)

    # --- Filters (NEW)
    st.sidebar.markdown('<div class="panel">', unsafe_allow_html=True)
    st.sidebar.write("**Filters**")

    post_filter = st.sidebar.selectbox(
        "Post Filter",
        [
            "None",
            "Vivid",
            "Warm",
            "Cool",
            "Sepia",
            "Neon Glow",
            "Comic Ink",
            "Posterize",
            "Pixelate",
            "Vignette",
            "Sharpen",
        ],
        index=0,
    )

    intensity = st.sidebar.slider("Filter Intensity", 0, 100, 45)
    edge_strength = st.sidebar.slider("Edge Strength", 0, 100, 35)

    st.sidebar.markdown("</div>", unsafe_allow_html=True)

    # --- Tune
    st.sidebar.markdown('<div class="panel">', unsafe_allow_html=True)
    st.sidebar.write("**Tune**")
    smooth = st.sidebar.slider("Smoothness", 0, 100, 35)
    brighten = st.sidebar.slider("Brightness", -30, 30, 8)
    st.sidebar.markdown("</div>", unsafe_allow_html=True)

    # --- Session
    st.sidebar.markdown('<div class="panel">', unsafe_allow_html=True)
    st.sidebar.write("**Session**")
    if st.sidebar.button("Clear History"):
        st.session_state["history"] = []
        st.session_state["last_out_image_bgr"] = None
        st.session_state["last_out_video_path"] = None
        st.toast("History cleared ✅")
    st.sidebar.markdown("</div>", unsafe_allow_html=True)

    # --- Payment
    st.sidebar.markdown('<div class="panel">', unsafe_allow_html=True)
    st.sidebar.write("**Payment (Demo)**")
    col1, col2 = st.sidebar.columns(2)
    if col1.button("Mark Paid ✅"):
        st.session_state["paid"] = True
    if col2.button("Reset ❌"):
        st.session_state["paid"] = False
    st.sidebar.caption("This is demo state only.")
    st.sidebar.markdown("</div>", unsafe_allow_html=True)

    # ✅ RETURN 7 VALUES
    return mode, style, smooth, brighten, post_filter, intensity, edge_strength