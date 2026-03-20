/**
 * Cartoonify - Admin Routes
 * Admin-only endpoints
 */

const express = require("express")
const path = require("path")
const fs = require("fs")

const db = require("../database/init.db")
const { authenticateToken, requireAdmin } = require("../auth")

console.log("AUTH CHECK:", authenticateToken, requireAdmin)
const router = express.Router()


/* ─────────────────────────────
   ADMIN DASHBOARD
───────────────────────────── */

router.get(
    "/dashboard",
    authenticateToken,
    requireAdmin,
    (req, res) => {

        res.json({
            success: true,
            message: "Admin dashboard access granted"
        })

    }
)


/* ─────────────────────────────
   ADMIN STATS
───────────────────────────── */

router.get(
    "/stats",
    authenticateToken,
    requireAdmin,
    (req, res) => {

        const totalUsers =
            db.prepare("SELECT COUNT(*) as count FROM users").get().count

        const totalImages =
            db.prepare("SELECT COUNT(*) as count FROM images").get().count

        const totalVideos =
            db.prepare("SELECT COUNT(*) as count FROM videos").get().count

        res.json({
            success: true,
            stats: {
                total_users: totalUsers,
                total_images: totalImages,
                total_videos: totalVideos
            }
        })

    }
)


/* ─────────────────────────────
   LIST USERS
───────────────────────────── */

router.get(
    "/users",
    authenticateToken,
    requireAdmin,
    (req, res) => {

        const users = db.prepare(`
            SELECT id,name,email,is_admin,created_at
            FROM users
            ORDER BY created_at DESC
        `).all()

        res.json({
            success: true,
            data: users
        })

    }
)


/* ─────────────────────────────
   DELETE USER
───────────────────────────── */

router.delete(
    "/users/:id",
    authenticateToken,
    requireAdmin,
    (req, res) => {

        const userId = parseInt(req.params.id)

        if (userId === req.user.id) {

            return res.status(400).json({
                success: false,
                message: "Cannot delete your own account"
            })

        }

        const user = db.prepare(
            "SELECT * FROM users WHERE id=?"
        ).get(userId)

        if (!user) {

            return res.status(404).json({
                success: false,
                message: "User not found"
            })

        }

        db.prepare("DELETE FROM users WHERE id=?").run(userId)

        res.json({
            success: true,
            message: "User deleted"
        })

    }
)


module.exports = router