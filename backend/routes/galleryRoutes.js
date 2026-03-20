/**
 * Cartoonify - Gallery Routes
 * Return images, videos, stickers for logged-in user
 */

const express = require("express")
const db = require("../database/init.db")
const { authenticateToken } = require("../auth")

const router = express.Router()


/* ─────────────────────────────────────────
   IMAGES
───────────────────────────────────────── */

router.get("/images", authenticateToken, (req, res) => {

    try {

        const page = parseInt(req.query.page) || 1
        const limit = parseInt(req.query.limit) || 12
        const offset = (page - 1) * limit

        const images = db.prepare(`
            SELECT *
            FROM images
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
        `).all(req.user.id, limit, offset)

        const total = db.prepare(`
            SELECT COUNT(*) as count
            FROM images
            WHERE user_id = ?
        `).get(req.user.id).count

        res.json({
            success: true,
            data: images.map(img => ({
                id: img.id,
                original: img.original_image.startsWith("/")
                    ? img.original_image
                    : "/" + img.original_image,
                cartoon: img.cartoon_image.startsWith("/")
                    ? img.cartoon_image
                    : "/" + img.cartoon_image,
                style_used: img.style_used,
                created_at: img.created_at
            })),
            pagination: { page, limit, total }
        })

    } catch (err) {

        console.error("Image gallery error:", err)

        res.status(500).json({
            success: false,
            message: "Failed to load images"
        })

    }

})


/* ─────────────────────────────────────────
   VIDEOS
───────────────────────────────────────── */

router.get("/videos", authenticateToken, (req, res) => {

    try {

        const page = parseInt(req.query.page) || 1
        const limit = parseInt(req.query.limit) || 8
        const offset = (page - 1) * limit

        const videos = db.prepare(`
            SELECT *
            FROM videos
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
        `).all(req.user.id, limit, offset)

        const total = db.prepare(`
            SELECT COUNT(*) as count
            FROM videos
            WHERE user_id = ?
        `).get(req.user.id).count

        res.json({
            success: true,
            data: videos.map(v => ({
                id: v.id,
                original: v.original_video.startsWith("/")
                    ? v.original_video
                    : "/" + v.original_video,
                cartoon: v.cartoon_video.startsWith("/")
                    ? v.cartoon_video
                    : "/" + v.cartoon_video,
                style_used: v.style_used,
                created_at: v.created_at
            })),
            pagination: { page, limit, total }
        })

    } catch (err) {

        console.error("Video gallery error:", err)

        res.status(500).json({
            success: false,
            message: "Failed to load videos"
        })

    }

})

router.get("/recent", authenticateToken, (req, res) => {

    try {

        const images = db.prepare(`
SELECT cartoon_image, style_used, created_at
FROM images
WHERE user_id = ?
ORDER BY created_at DESC
LIMIT 8
`).all(req.user.id)

        res.json({
            success: true,
            images
        })

    } catch (err) {

        console.error(err)

        res.json({
            success: false,
            images: []
        })

    }

})
/* ─────────────────────────────────────────
   STICKERS
───────────────────────────────────────── */

router.get("/stickers", authenticateToken, (req, res) => {

    try {

        const stickers = db.prepare(`
            SELECT
                id,
                sticker_path AS sticker,
                created_at
            FROM stickers
            WHERE user_id = ?
            ORDER BY created_at DESC
        `).all(req.user.id)

        res.json({
            success: true,
            data: stickers.map(s => ({
                id: s.id,
                sticker: s.sticker.startsWith("/")
                    ? s.sticker
                    : "/" + s.sticker,
                created_at: s.created_at
            }))
        })

    } catch (err) {

        console.error("Sticker fetch error:", err)

        res.status(500).json({
            success: false,
            message: "Failed to load stickers"
        })

    }

})


module.exports = router