/**
 * Cartoonify - Gallery JS
 * Fetches and renders user image, video, and sticker gallery
 */

let imagePage = 1
let videoPage = 1

let imageTotal = 0
let videoTotal = 0
let stickerTotal = 0

/* ─────────────────────────
   UTILITY FUNCTIONS
───────────────────────── */

function escHtml(text) {
  if (!text) return ""
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;")
}

function timeAgo(dateString) {

  const date = new Date(dateString)
  const seconds = Math.floor((new Date() - date) / 1000)

  const intervals = [
    { label: "year", seconds: 31536000 },
    { label: "month", seconds: 2592000 },
    { label: "day", seconds: 86400 },
    { label: "hour", seconds: 3600 },
    { label: "minute", seconds: 60 }
  ]

  for (const i of intervals) {

    const count = Math.floor(seconds / i.seconds)

    if (count >= 1)
      return count + " " + i.label + (count > 1 ? "s" : "") + " ago"
  }

  return "just now"
}

/* ─────────────────────────────────────────
   LOAD IMAGES
───────────────────────────────────────── */

async function loadImages(append = false) {

  if (!append) imagePage = 1

  const grid = document.getElementById("imagesGrid")

  try {

    const data = await apiGet(`/api/gallery/images?page=${imagePage}&limit=12`)

    if (!data || !data.success) return

    imageTotal = data.pagination.total
    document.getElementById("imageCount").textContent = imageTotal

    if (!append) grid.innerHTML = ""

    if (data.data.length === 0 && !append) {

      grid.innerHTML = `
      <div class="col-12 text-center py-5 text-muted">
      <i class="bi bi-images fs-1 d-block mb-2"></i>
      <p>No images yet.
      <a href="upload.html" class="link-purple">
      Create your first cartoon!
      </a></p>
      </div>`

      return
    }

    data.data.forEach(img => {

      const col = document.createElement("div")
      col.className = "col-6 col-md-4 col-lg-3"
      col.innerHTML = buildImageCard(img)

      grid.appendChild(col)

    })

    imagePage++

  }

  catch (err) {

    console.error("Gallery images error:", err)

  }

}


/* ─────────────────────────────────────────
   IMAGE CARD
───────────────────────────────────────── */

function buildImageCard(img) {

  const original = img.original || img.original_image
  const cartoon = img.cartoon || img.cartoon_image

  return `
<div class="gallery-image-card">

<div class="gallery-thumb-row">

<div class="gallery-thumb g-label-wrap">
<img src="${original}" alt="Original"/>
<span class="g-label">Before</span>
</div>

<div class="gallery-thumb g-label-wrap">
<img src="${cartoon}" alt="Cartoon"/>
<span class="g-label">After</span>
</div>

</div>

<div class="gallery-info">

<div class="d-flex justify-content-between align-items-center mb-2">

<span class="style-badge">${escHtml(img.style_used)}</span>

<small class="text-muted">
${timeAgo(img.created_at)}
</small>

</div>

<div class="d-flex gap-1">

<button class="btn btn-ghost flex-fill"
onclick="openImageModal('${original}','${cartoon}','${escHtml(img.style_used)}')">

<i class="bi bi-arrows-angle-expand"></i>
View

</button>

<a href="${cartoon}"
download
class="btn btn-glow-sm flex-fill">

<i class="bi bi-download"></i>
Download

</a>

</div>

</div>

</div>
`
}


/* ─────────────────────────────────────────
   IMAGE MODAL
───────────────────────────────────────── */

function openImageModal(original, cartoon, style) {

  const modal = new bootstrap.Modal(
    document.getElementById("imageModal")
  )

  document.getElementById("modalBefore").src = original
  document.getElementById("modalAfter").src = cartoon
  document.getElementById("modalStyle").textContent = style
  document.getElementById("modalDownload").href = cartoon

  modal.show()

  setTimeout(() => {
    initComparisonSlider("modalSliderWrap", "modalSlider")
  }, 300)

}


/* ─────────────────────────────────────────
   LOAD VIDEOS
───────────────────────────────────────── */

async function loadVideos() {

  const grid = document.getElementById("videosGrid")

  try {

    const data = await apiGet(`/api/gallery/videos?page=${videoPage}&limit=8`)

    if (!data || !data.success) return

    videoTotal = data.pagination.total
    document.getElementById("videoCount").textContent = videoTotal

    grid.innerHTML = ""

    if (data.data.length === 0) {

      grid.innerHTML = `
<div class="col-12 text-center py-5 text-muted">

<i class="bi bi-camera-video fs-1 d-block mb-2"></i>

<p>No videos yet.
<a href="video_editor.html" class="link-purple">
Create your first cartoon video!
</a></p>

</div>`

      return

    }

    data.data.forEach(vid => {

      const col = document.createElement("div")
      col.className = "col-6 col-md-4 col-lg-3"
      col.innerHTML = buildVideoCard(vid)

      grid.appendChild(col)

    })

  }

  catch (err) {

    console.error("Gallery videos error:", err)

  }

}


/* ─────────────────────────────────────────
   VIDEO CARD
───────────────────────────────────────── */

function buildVideoCard(vid) {

  let cartoon = vid.cartoon || vid.cartoon_video

  if (!cartoon) return ""

  if (!cartoon.startsWith("/")) {
    cartoon = "/" + cartoon
  }

  cartoon = window.location.origin + cartoon

  return `
<div class="gallery-video-card">

<div class="gallery-video-thumb">

<video
src="${cartoon}"
muted
loop
controls
preload="metadata"
onmouseenter="this.play()"
onmouseleave="this.pause()">
</video>

</div>

<div class="gallery-info">

<div class="d-flex justify-content-between align-items-center mb-2">

<span class="style-badge">${escHtml(vid.style_used)}</span>

<small class="text-muted">
${timeAgo(vid.created_at)}
</small>

</div>

<a href="${cartoon}"
download
class="btn btn-glow-sm w-100">

<i class="bi bi-download"></i>
Download Video

</a>

</div>

</div>
`
}


/* ─────────────────────────────────────────
   LOAD STICKERS
───────────────────────────────────────── */

async function loadStickers() {

  const grid = document.getElementById("stickersGrid")

  try {

    const data = await apiGet("/api/gallery/stickers")

    if (!data || !data.success) {
      showStickerError()
      return
    }

    const stickers = data.data || []

    stickerTotal = stickers.length
    document.getElementById("stickerCount").textContent = stickerTotal

    grid.innerHTML = ""

    if (stickers.length === 0) {

      grid.innerHTML = `
<div class="col-12 text-center py-5 text-muted">

<i class="bi bi-emoji-smile fs-1 d-block mb-2"></i>

<p>No stickers generated yet.
<a href="sticker.html" class="link-purple">
Create your first sticker!
</a></p>

</div>`

      return
    }

    stickers.forEach(sticker => {

      const col = document.createElement("div")
      col.className = "col-6 col-md-4 col-lg-3"
      col.innerHTML = buildStickerCard(sticker)

      grid.appendChild(col)

    })

  }

  catch (err) {

    console.error("Sticker gallery error:", err)
    showStickerError()

  }

}


/* ─────────────────────────────────────────
   STICKER CARD
───────────────────────────────────────── */

function buildStickerCard(sticker) {

  const img = sticker.sticker || sticker.sticker_path

  return `
<div class="gallery-sticker-card text-center">

<img src="${img}"
class="img-fluid mb-2"
style="max-height:180px; object-fit:contain;">

<a href="${img}"
download
class="btn btn-glow-sm w-100">

<i class="bi bi-download"></i>
Download

</a>

</div>
`
}


/* ─────────────────────────────────────────
   ERROR MESSAGE
───────────────────────────────────────── */

function showStickerError() {

  const grid = document.getElementById("stickersGrid")

  grid.innerHTML = `
<div class="col-12 text-center py-5 text-danger">

<i class="bi bi-exclamation-triangle fs-1 d-block mb-2"></i>

<p>Failed to load stickers</p>

</div>`
}


/* ─────────────────────────────────────────
   AUTO REFRESH AFTER VIDEO PROCESS
───────────────────────────────────────── */

if (localStorage.getItem("galleryRefresh")) {

  loadVideos()
  localStorage.removeItem("galleryRefresh")

}


/* ─────────────────────────────────────────
   INIT
───────────────────────────────────────── */

document.addEventListener("DOMContentLoaded", () => {

  loadImages()
  loadVideos()
  loadStickers()

})