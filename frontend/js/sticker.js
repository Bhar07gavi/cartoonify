/**
 * Cartoonify - Sticker Generator JS
 */

let generatedSticker = null


/* ─────────────────────────────────────────
   GENERATE STICKER
───────────────────────────────────────── */

async function generateSticker() {

    const fileInput = document.getElementById("imageInput")
    const text = document.getElementById("stickerText").value
    const position = document.getElementById("textPosition").value

    if (!fileInput.files.length) {

        alert("Please upload an image")
        return

    }

    const file = fileInput.files[0]

    const formData = new FormData()

    formData.append("image", file)
    formData.append("text", text)
    formData.append("position", position)


    try {

        const res = await fetch("/api/sticker", {
            method: "POST",
            headers: getAuthHeaders(),
            body: formData
        })

        const data = await res.json()

        if (!data.success) {

            alert("Sticker generation failed")
            return

        }

        generatedSticker = data.sticker


        /* Show sticker */

        const img = document.getElementById("result")

        img.src = data.sticker + "?t=" + Date.now()

        document.getElementById("resultPlaceholder").classList.add("d-none")

        document.getElementById("resultContainer").classList.remove("d-none")


    } catch (err) {

        console.error(err)
        alert("Sticker generation failed")

    }

}



/* ─────────────────────────────────────────
   DOWNLOAD STICKER
───────────────────────────────────────── */

function downloadSticker() {

    if (!generatedSticker) return

    const link = document.createElement("a")

    link.href = generatedSticker

    link.download = "sticker.webp"

    document.body.appendChild(link)

    link.click()

    document.body.removeChild(link)

}



/* ─────────────────────────────────────────
   SHARE WHATSAPP
───────────────────────────────────────── */

function shareWhatsApp() {

    if (!generatedSticker) return

    const url = window.location.origin + generatedSticker

    const shareUrl = `https://wa.me/?text=${encodeURIComponent("Check my sticker: " + url)}`

    window.open(shareUrl, "_blank")

}



/* ─────────────────────────────────────────
   IMAGE PREVIEW
───────────────────────────────────────── */

document
    .getElementById("imageInput")
    .addEventListener("change", function () {

        const file = this.files[0]

        if (!file) return

        const reader = new FileReader()

        reader.onload = function (e) {

            const img = document.getElementById("previewImg")

            img.src = e.target.result

            img.style.display = "block"

        }

        reader.readAsDataURL(file)

    })