/**
 * Cartoonify - Dashboard Stats Routes
 * Returns statistics for logged-in user
 */

const express = require("express")
const router = express.Router()

const db = require("../database/init.db")
const { authenticateToken } = require("../auth")


/* ─────────────────────────────────────────
   GET /api/auth/stats
───────────────────────────────────────── */
router.get("/", authenticateToken, (req, res) => {

    const userId = req.user.id

    try {

        const totalImages = db.prepare(`
SELECT COUNT(*) as count
FROM images
WHERE user_id=?
`).get(userId).count

        const totalVideos = db.prepare(`
SELECT COUNT(*) as count
FROM videos
WHERE user_id=?
`).get(userId).count

        const totalStickers = db.prepare(`
SELECT COUNT(*) as count
FROM stickers
WHERE user_id=?
`).get(userId).count


        const recentImages = db.prepare(`
SELECT id, cartoon_image, style_used, created_at
FROM images
WHERE user_id=?
ORDER BY created_at DESC
LIMIT 8
`).all(userId)


        res.json({

            success: true,

            stats: {
                total_images: totalImages,
                total_videos: totalVideos,
                total_stickers: totalStickers
            },

            recent_images: recentImages.map(img => ({
                id: img.id,
                cartoon: img.cartoon_image.startsWith("/")
                    ? img.cartoon_image
                    : "/" + img.cartoon_image,
                style_used: img.style_used,
                created_at: img.created_at
            }))

        })

    } catch (err) {

        console.error("Stats error:", err)

        res.status(500).json({
            success: false,
            message: "Failed to load dashboard stats"
        })

    }

})



module.exports = router