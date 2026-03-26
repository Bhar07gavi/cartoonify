/**
 * Cartoonify - Video Routes
 * Handles video upload, AI processing, DB storage
 */

const express = require("express")
const multer = require("multer")
const path = require("path")
const fs = require("fs")
const axios = require("axios")
const FormData = require("form-data")
const { v4: uuidv4 } = require("uuid")

const db = require("../database/init.db")
const { authenticateToken } = require("../auth")

const router = express.Router()

/* ─────────────────────────────────────────
   DIRECTORIES
───────────────────────────────────────── */

const ROOT = path.join(__dirname, "..", "..")

const UPLOAD_DIR = path.join(ROOT, "uploads")
const OUTPUT_DIR = path.join(ROOT, "outputs", "videos")

if (!fs.existsSync(UPLOAD_DIR)) fs.mkdirSync(UPLOAD_DIR, { recursive: true })
if (!fs.existsSync(OUTPUT_DIR)) fs.mkdirSync(OUTPUT_DIR, { recursive: true })

/* ─────────────────────────────────────────
   MULTER CONFIG
───────────────────────────────────────── */

const storage = multer.diskStorage({

    destination: (req, file, cb) => {
        cb(null, UPLOAD_DIR)
    },

    filename: (req, file, cb) => {

        const ext = path.extname(file.originalname).toLowerCase()

        cb(null, "vid_" + uuidv4() + ext)

    }

})

const upload = multer({

    storage,

    limits: { fileSize: 200 * 1024 * 1024 },

    fileFilter: (req, file, cb) => {

        const allowed = [".mp4", ".avi", ".mov", ".mkv", ".webm"]

        const ext = path.extname(file.originalname).toLowerCase()

        if (!allowed.includes(ext)) {
            return cb(new Error("Only video files allowed"))
        }

        cb(null, true)

    }

})

/* ─────────────────────────────────────────
   AI SERVER
───────────────────────────────────────── */

const AI_URL = process.env.PYTHON_AI_URL || "https://cartoonify-ai.onrender.com"

/* ─────────────────────────────────────────
   POST /api/videos/upload
───────────────────────────────────────── */

router.post(
    "/upload",
    authenticateToken,
    upload.single("video"),

    async (req, res) => {

        if (!req.file) {

            return res.status(400).json({
                success: false,
                message: "No video uploaded"
            })

        }

        const style = req.body.style || "classic"

        const originalPath = req.file.path
        const originalName = req.file.filename

        try {

            /* Send video to AI */

            const formData = new FormData()

            formData.append(
                "file",
                fs.createReadStream(originalPath),
                req.file.originalname
            )

            formData.append("style", style)

            console.log("🎬 Sending video to AI server...")

            const aiResponse = await axios.post(
                `${AI_URL}/cartoonify-video`,
                formData,
                {
                    headers: formData.getHeaders(),
                    responseType: "arraybuffer",
                    timeout: 600000
                }
            )

            /* Validate AI response */

            if (!aiResponse.data || aiResponse.data.length === 0) {
                throw new Error("AI returned empty video")
            }

            /* Save processed video */

            const outputFile = "cartoon_vid_" + uuidv4() + ".mp4"
            const outputPath = path.join(OUTPUT_DIR, outputFile)

            fs.writeFileSync(outputPath, aiResponse.data)

            /* Save to database */

            const result = db.prepare(`
INSERT INTO videos
(user_id, original_video, cartoon_video, style_used)
VALUES (?, ?, ?, ?)
`).run(
                req.user.id,
                `/uploads/${originalName}`,
                `/outputs/videos/${outputFile}`,
                style
            )

            /* Fetch inserted record */

            const record = db.prepare(
                "SELECT * FROM videos WHERE id = ?"
            ).get(result.lastInsertRowid)

            /* Send response */

            res.json({

                success: true,
                message: "Video cartoonified successfully",

                data: {

                    id: record.id,
                    original: record.original_video,
                    cartoon: record.cartoon_video,
                    style: record.style_used,
                    created_at: record.created_at

                }

            })

        }

        catch (err) {

            console.error("❌ Video cartoonify error:")

            if (err.response) {
                console.error("AI Server Response:", err.response.data.toString())
            } else {
                console.error(err.message)
            }

            /* Cleanup uploaded file */

            if (fs.existsSync(originalPath)) {
                fs.unlinkSync(originalPath)
            }

            res.status(500).json({

                success: false,
                message: "Video processing failed. Check AI server."

            })

        }

    })

/* ─────────────────────────────────────────
   GET VIDEO
───────────────────────────────────────── */

router.get("/:id", authenticateToken, (req, res) => {

    const video = db.prepare(`
SELECT * FROM videos
WHERE id = ? AND user_id = ?
`).get(req.params.id, req.user.id)

    if (!video) {

        return res.status(404).json({
            success: false,
            message: "Video not found"
        })

    }

    res.json({
        success: true,
        data: video
    })

})

/* ─────────────────────────────────────────
   DELETE VIDEO
───────────────────────────────────────── */

router.delete("/:id", authenticateToken, (req, res) => {

    const video = db.prepare(`
SELECT * FROM videos
WHERE id = ? AND user_id = ?
`).get(req.params.id, req.user.id)

    if (!video) {

        return res.status(404).json({
            success: false,
            message: "Video not found"
        })

    }

    const files = [
        video.original_video,
        video.cartoon_video
    ]

    files.forEach(file => {

        const filePath = path.join(ROOT, file)

        if (fs.existsSync(filePath)) {
            fs.unlinkSync(filePath)
        }

    })

    db.prepare("DELETE FROM videos WHERE id = ?").run(video.id)

    res.json({
        success: true,
        message: "Video deleted"
    })

})

module.exports = router
