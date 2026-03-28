/**
 * Sticker Routes
 * Generate sticker and save to DB
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

const AI_URL = process.env.AI_SERVICE_URL || "http://localhost:8000"  // ✅ Use env variable

/* ─────────────────────────────────────────
   Multer Upload
───────────────────────────────────────── */

const storage = multer.diskStorage({

    destination: (req, file, cb) => {

        const dir = path.join(__dirname, "..", "..", "uploads")

        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir, { recursive: true })
        }

        cb(null, dir)
    },

    filename: (req, file, cb) => {

        const ext = path.extname(file.originalname)
        cb(null, "upload_" + uuidv4() + ext)

    }

})

const upload = multer({ storage })


/* ─────────────────────────────────────────
   POST /api/sticker
───────────────────────────────────────── */

router.post("/", authenticateToken, upload.single("image"), async (req, res) => {

    try {

        if (!req.file) {
            return res.status(400).json({
                success: false,
                message: "No image uploaded"
            })
        }

        // ✅ Create form data for AI server
        const formData = new FormData()

        formData.append(
            "file",
            fs.createReadStream(req.file.path),
            req.file.originalname
        )

        // ✅ Text
        if (req.body.text) {
            formData.append("text", req.body.text)
        }

        // ✅ Drag coordinates (IMPORTANT FIX)
        if (req.body.x !== undefined) {
            formData.append("x", req.body.x)
        }

        if (req.body.y !== undefined) {
            formData.append("y", req.body.y)
        }

        // 🔍 Debug (optional)
        console.log("Drag Position:", req.body.x, req.body.y)

        // ✅ Call FastAPI AI service
        const aiRes = await axios.post(
            `${AI_URL}/generate-sticker`,
            formData,
            {
                headers: formData.getHeaders(),
                responseType: "arraybuffer"
            }
        )

        /* ───────── SAVE OUTPUT ───────── */

        const outputDir = path.join(__dirname, "..", "..", "outputs", "stickers")

        if (!fs.existsSync(outputDir)) {
            fs.mkdirSync(outputDir, { recursive: true })
        }

        const filename = "sticker_" + uuidv4() + ".webp"
        const outputPath = path.join(outputDir, filename)

        fs.writeFileSync(outputPath, aiRes.data)

        /* ───────── SAVE TO DB ───────── */

        const stickerPath = `outputs/stickers/${filename}`

        db.prepare(`
            INSERT INTO stickers (user_id, sticker_path)
            VALUES (?, ?)
        `).run(req.user.id, stickerPath)

        /* ───────── CLEANUP ───────── */

        if (fs.existsSync(req.file.path)) {
            fs.unlinkSync(req.file.path)
        }

        /* ───────── RESPONSE ───────── */

        res.json({
            success: true,
            sticker: "/" + stickerPath
        })

    } catch (err) {

        console.error("Sticker error:", err)

        res.status(500).json({
            success: false,
            message: "Sticker generation failed"
        })

    }

})

module.exports = router
