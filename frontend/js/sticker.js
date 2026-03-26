let generatedSticker = null
let videoStream = null

/* ================= CAMERA ================= */

async function startCamera() {

    const video = document.getElementById("video")

    try {
        videoStream = await navigator.mediaDevices.getUserMedia({ video: true })
        video.srcObject = videoStream
    } catch {
        alert("Camera not allowed")
    }
}

function stopCamera() {
    if (videoStream) {
        videoStream.getTracks().forEach(track => track.stop())
        videoStream = null
    }
}

/* ================= CAPTURE STICKER ================= */

async function captureSticker() {

    const video = document.getElementById("video")
    const canvas = document.getElementById("canvas")

    if (!video || !video.videoWidth) {
        alert("Camera not ready")
        return
    }

    const text = document.getElementById("stickerText").value
    const position = document.getElementById("textPosition").value

    canvas.width = video.videoWidth
    canvas.height = video.videoHeight

    const ctx = canvas.getContext("2d")
    ctx.drawImage(video, 0, 0)

    canvas.toBlob(async (blob) => {

        const formData = new FormData()

        formData.append("image", blob, "camera.png")
        formData.append("text", text)
        formData.append("position", position)

        // ✅ ONLY if custom
        if (position === "custom") {

        const previewImg = document.getElementById("previewImg")

        const scaleX = 512 / previewImg.clientWidth
        const scaleY = 512 / previewImg.clientHeight

        const x = dragText.offsetLeft * scaleX
        const y = dragText.offsetTop * scaleY

        formData.append("x", Math.round(x))
        formData.append("y", Math.round(y))
    }

        try {
            const res = await fetch("https://cartoonify-backend-ordt.onrender.com/api/sticker", {
                method: "POST",
                headers: getAuthHeaders(),
                body: formData
            })

            const data = await res.json()

            if (!data.success) {
                alert("Sticker generation failed")
                return
            }

            showResult(data.sticker)
            stopCamera()

        } catch {
            alert("Camera sticker failed")
        }

    }, "image/png")
}
/* ================= UPLOAD STICKER ================= */

async function generateSticker() {

    const fileInput = document.getElementById("imageInput")

    
    if (!fileInput.files || fileInput.files.length === 0) {
        alert("Upload image first")
        return
    }

    const file = fileInput.files[0]
    const text = document.getElementById("stickerText").value
    const position = document.getElementById("textPosition").value

    const formData = new FormData()

    formData.append("image", file)
    formData.append("text", text)
    formData.append("position", position)

    // ✅ ONLY if custom
    if (position === "custom") {

        const dragText = document.getElementById("dragText")
        const previewImg = document.getElementById("previewImg")

        const scaleX = 512 / previewImg.clientWidth
        const scaleY = 512 / previewImg.clientHeight

        const rectImg = previewImg.getBoundingClientRect()
const rectText = dragText.getBoundingClientRect()

const x = (rectText.left - rectImg.left) * scaleX
const y = (rectText.top - rectImg.top) * scaleY

        formData.append("x", Math.round(x))
        formData.append("y", Math.round(y))
    }

    try {

        const res = await fetch("https://cartoonify-backend-ordt.onrender.com/api/sticker", {
            method: "POST",
            headers: getAuthHeaders(),
            body: formData
        })

        const data = await res.json()

        if (!data.success) {
            alert("Sticker failed")
            return
        }

        showResult(data.sticker)

    } catch {
        alert("Sticker error")
    }
}

/* ================= RESULT ================= */

function showResult(url) {

    generatedSticker = url

    document.getElementById("result").src = url + "?t=" + Date.now()

    document.getElementById("resultPlaceholder").classList.add("d-none")
    document.getElementById("resultContainer").classList.remove("d-none")

    document.getElementById("result").scrollIntoView({ behavior: "smooth" })
}

/* ================= DOWNLOAD ================= */

function downloadSticker() {

    if (!generatedSticker) return

    const link = document.createElement("a")
    link.href = generatedSticker
    link.download = "sticker.webp"
    link.click()
}

/* ================= WHATSAPP ================= */

function shareWhatsApp() {

    if (!generatedSticker) return

    const url = window.location.origin + generatedSticker

    window.open(`https://wa.me/?text=${encodeURIComponent(url)}`)
}
