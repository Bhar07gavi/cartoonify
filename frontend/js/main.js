/**
 * Cartoonify - Main JS Utilities
 * Toast notifications, API helpers, slider,
 * sticker generator, preview, download, WhatsApp share
 */

const API_BASE = "";


/* ─────────────────────────────────────────
   Toast Notification System
───────────────────────────────────────── */

(function createToastContainer() {

    if (!document.getElementById("toastContainer")) {
        const div = document.createElement("div")
        div.id = "toastContainer"
        document.body.appendChild(div)
    }

})()

function showToast(message, type = "info", duration = 4000) {

    const container = document.getElementById("toastContainer")

    const icons = {
        success: "✅",
        error: "❌",
        warning: "⚠️",
        info: "ℹ️"
    }

    const toast = document.createElement("div")
    toast.className = `toast-item ${type}`

    toast.innerHTML = `
        <span class="toast-icon">${icons[type] || icons.info}</span>
        <span class="toast-msg">${message}</span>
    `

    container.appendChild(toast)

    setTimeout(() => {

        toast.style.transition = "opacity 0.3s, transform 0.3s"
        toast.style.opacity = "0"
        toast.style.transform = "translateX(120%)"

        setTimeout(() => toast.remove(), 350)

    }, duration)

}


/* ─────────────────────────────────────────
   Authentication Headers
───────────────────────────────────────── */

function getAuthHeaders() {

    const token = localStorage.getItem("cartoonify_token")

    return token
        ? { Authorization: `Bearer ${token}` }
        : {}

}


/* ─────────────────────────────────────────
   API Helpers
───────────────────────────────────────── */

async function apiGet(url) {

    const res = await fetch(API_BASE + url, {
        headers: getAuthHeaders()
    })

    if (res.status === 401 || res.status === 403) {

        localStorage.removeItem("cartoonify_token")
        window.location.href = "/login.html"
        return

    }

    return res.json()

}

async function apiPost(url, body) {

    const res = await fetch(API_BASE + url, {

        method: "POST",

        headers: {
            ...getAuthHeaders(),
            "Content-Type": "application/json"
        },

        body: JSON.stringify(body)

    })

    return res.json()

}


/* ─────────────────────────────────────────
   Image Upload Preview
───────────────────────────────────────── */

document.addEventListener("DOMContentLoaded", () => {

    const input = document.getElementById("imageInput")

    if (!input) return

    input.addEventListener("change", function () {

        const file = this.files[0]
        if (!file) return

        const reader = new FileReader()

        reader.onload = function (e) {

            const img = document.getElementById("previewImg")

            if (img) {
                img.src = e.target.result
                img.style.display = "block"
            }

        }

        reader.readAsDataURL(file)

    })

})


/* ─────────────────────────────────────────
   Image Comparison Slider
───────────────────────────────────────── */

function initComparisonSlider(wrapId = "sliderWrap", sliderId = "compSlider") {

    const wrap = document.getElementById(wrapId)
    const slider = document.getElementById(sliderId)

    const before = wrap ? wrap.querySelector(".comp-before") : null
    const after = wrap ? wrap.querySelector(".comp-after") : null

    if (!wrap || !slider || !before || !after) return

    const setHeight = () => {
        wrap.style.height = wrap.offsetWidth * 0.65 + "px"
    }

    setHeight()
    window.addEventListener("resize", setHeight)

    let dragging = false

    function updateSlider(x) {

        const rect = wrap.getBoundingClientRect()

        let pct = Math.max(
            0,
            Math.min(100, ((x - rect.left) / rect.width) * 100)
        )

        slider.style.left = pct + "%"

        before.style.clipPath = `inset(0 ${100 - pct}% 0 0)`
        after.style.clipPath = `inset(0 0 0 ${pct}%)`

    }

    wrap.addEventListener("mousedown", e => {
        dragging = true
        updateSlider(e.clientX)
    })

    document.addEventListener("mousemove", e => {
        if (dragging) updateSlider(e.clientX)
    })

    document.addEventListener("mouseup", () => {
        dragging = false
    })

}


/* ─────────────────────────────────────────
   Generate Sticker
───────────────────────────────────────── */

async function generateSticker() {

    const input = document.getElementById("imageInput")

    if (!input || !input.files.length) {
        showToast("Select image first", "warning")
        return
    }

    const file = input.files[0]

    const text = document.getElementById("stickerText")?.value || ""
    const position = document.getElementById("textPosition")?.value || "top"

    const formData = new FormData()

    formData.append("image", file)
    formData.append("text", text)
    formData.append("position", position)

    const token = localStorage.getItem("cartoonify_token")

    showToast("Generating sticker...", "info")

    try {

        const res = await fetch("https://cartoonify-backend-ordt.onrender.com/api/sticker", {
            method: "POST",
            headers: {
                Authorization: "Bearer " + token
            },
            body: formData
        })

        if (!res.ok) {
            showToast("Sticker generation failed", "error")
            return
        }

        const data = await res.json()

        if (!data.success) {
            showToast("Sticker failed", "error")
            return
        }

        const img = document.getElementById("result")

        if (img) img.src = data.sticker

        document.getElementById("resultPlaceholder")?.classList.add("d-none")
        document.getElementById("resultContainer")?.classList.remove("d-none")

        showToast("Sticker created!", "success")

    }
    catch (err) {

        console.error(err)
        showToast("Server error generating sticker", "error")

    }

}


/* ─────────────────────────────────────────
   Copy Sticker
───────────────────────────────────────── */

async function copySticker(url) {

    try {

        const blob = await fetch(url).then(r => r.blob())

        await navigator.clipboard.write([
            new ClipboardItem({
                "image/webp": blob
            })
        ])

        showToast("Sticker copied! Paste in WhatsApp", "success")

    }
    catch {

        showToast("Clipboard not supported", "error")

    }

}


/* ─────────────────────────────────────────
   Download Sticker
───────────────────────────────────────── */

function downloadSticker(url = null) {

    let imgUrl = url

    if (!imgUrl) {

        const img = document.getElementById("result")

        if (!img || !img.src) {

            showToast("No sticker available", "warning")
            return

        }

        imgUrl = img.src

    }

    const a = document.createElement("a")

    a.href = imgUrl
    a.download = "cartoonify_sticker.webp"

    document.body.appendChild(a)
    a.click()
    a.remove()

    showToast("Sticker downloaded!", "success")

}


/* ─────────────────────────────────────────
   WhatsApp Share
───────────────────────────────────────── */

function shareWhatsApp() {

    showToast("Download or copy sticker then paste in WhatsApp", "info")

    window.open("https://web.whatsapp.com", "_blank")

}
