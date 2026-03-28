/**
 * Cartoonify - Image Routes
 * Upload image → send to Python AI → save result
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

// ----------------------------------------------------
// Directories
// ----------------------------------------------------

const ROOT = path.join(__dirname, "..", "..")
const UPLOAD_DIR = path.join(ROOT, "uploads")
const OUTPUT_DIR = path.join(ROOT, "outputs")

if (!fs.existsSync(UPLOAD_DIR)) fs.mkdirSync(UPLOAD_DIR, { recursive: true })
if (!fs.existsSync(OUTPUT_DIR)) fs.mkdirSync(OUTPUT_DIR, { recursive: true })

// ----------------------------------------------------
// Multer Upload Config
// ----------------------------------------------------

const storage = multer.diskStorage({

    destination: (req, file, cb) => {
        cb(null, UPLOAD_DIR)
    },

    filename: (req, file, cb) => {

        const ext = path.extname(file.originalname).toLowerCase()
        cb(null, "img_" + uuidv4() + ext)

    }

})

const upload = multer({

    storage,

    limits: { fileSize: 20 * 1024 * 1024 },

    fileFilter: (req, file, cb) => {

        const allowed = [".jpg", ".jpeg", ".png", ".webp"]

        const ext = path.extname(file.originalname).toLowerCase()

        if (!allowed.includes(ext)) {
            return cb(new Error("Only JPG, PNG, WEBP images allowed"))
        }

        cb(null, true)

    }

})

// ----------------------------------------------------
// AI Server URL
// ----------------------------------------------------

const AI_URL = process.env.AI_SERVICE_URL || "http://localhost:8000"

// ----------------------------------------------------
// Upload + Cartoonify Image
// ----------------------------------------------------

router.post(
    "/upload",
    authenticateToken,
    upload.single("image"),
    async (req, res) => {

        if (!req.file) {

            return res.status(400).json({
                success: false,
                message: "No image uploaded"
            })

        }

        // --------------------------------------------
        // Parameters from frontend
        // --------------------------------------------

        // Parameters from frontend
        const style = req.body.style || "classic"
        const filter = req.body.filter || ""
        const overlay = req.body.overlay || ""

        const brightness = req.body.brightness || 50
        const contrast = req.body.contrast || 50
        const saturation = req.body.saturation || 50

        // Just pass the style directly - no mapping needed
const aiStyle = style || "classic"

        console.log("STYLE FROM FRONTEND:", style)

        const originalPath = req.file.path
        const originalName = req.file.filename

        try {

            const formData = new FormData()

            // image file
            formData.append(
                "file",
                fs.createReadStream(originalPath),
                req.file.originalname
            )

            // style + controls
            formData.append("style", aiStyle)
            formData.append("filter", filter)
            formData.append("overlay", overlay)

            formData.append("brightness", brightness)
            formData.append("contrast", contrast)
            formData.append("saturation", saturation)

            console.log("🎨 Sending image to AI server with style:", aiStyle)

            const aiResponse = await axios.post(
    `${AI_URL}/cartoonify-image`,
    formData,
    {
        headers: formData.getHeaders(),
        responseType: "arraybuffer",
        timeout: 600000  // ← 10 minutes (600 seconds)
    }
)

            // ------------------------------------------------
            // Save cartoon image
            // ------------------------------------------------

            const outputFile = "cartoon_" + uuidv4() + ".jpg"
            const outputPath = path.join(OUTPUT_DIR, outputFile)

            fs.writeFileSync(outputPath, aiResponse.data)

            // ------------------------------------------------
            // Save to database
            // ------------------------------------------------

            const result = db.prepare(`
                INSERT INTO images
                (user_id, original_image, cartoon_image, style_used)
                VALUES (?, ?, ?, ?)
            `).run(
                req.user.id,
                "uploads/" + originalName,
                "outputs/" + outputFile,
                style
            )

            const record = db.prepare(
                "SELECT * FROM images WHERE id = ?"
            ).get(result.lastInsertRowid)

            res.json({

                success: true,

                message: "Image cartoonified successfully",

                data: {

                    id: record.id,
                    original: "/" + record.original_image,
                    cartoon: "/" + record.cartoon_image,
                    style: style,
                    created_at: record.created_at

                }

            })

        }

       catch (err) {
    console.error("=" * 50)
    console.error("❌ FULL ERROR:", err)
    console.error("❌ Error Message:", err.message)
    console.error("❌ Error Code:", err.code)
    console.error("❌ AI URL Being Called:", `${AI_URL}/cartoonify-image`)
    
    if (err.response) {
        console.error("❌ AI Response Status:", err.response.status)
        console.error("❌ AI Response Data:", err.response.data)
    }
    
    if (err.request && !err.response) {
        console.error("❌ No response received from AI service")
        console.error("❌ Request details:", err.request)
    }
    console.error("=" * 50)

    if (fs.existsSync(originalPath)) {
        fs.unlinkSync(originalPath)
    }

    res.status(500).json({
        success: false,
        message: `Failed to process image: ${err.message}`
    })
}
    }
)

// ----------------------------------------------------
// Get Image By ID
// ----------------------------------------------------

router.get("/:id", authenticateToken, (req, res) => {

    const image = db.prepare(`
        SELECT * FROM images
        WHERE id = ? AND user_id = ?
    `).get(req.params.id, req.user.id)

    if (!image) {

        return res.status(404).json({
            success: false,
            message: "Image not found"
        })

    }

    res.json({
        success: true,
        data: image
    })

})

// ----------------------------------------------------
// Delete Image
// ----------------------------------------------------

router.delete("/:id", authenticateToken, (req, res) => {

    const image = db.prepare(`
        SELECT * FROM images
        WHERE id = ? AND user_id = ?
    `).get(req.params.id, req.user.id)

    if (!image) {

        return res.status(404).json({
            success: false,
            message: "Image not found"
        })

    }

    const files = [
        image.original_image,
        image.cartoon_image
    ]

    files.forEach(file => {

        const fp = path.join(ROOT, file)

        if (fs.existsSync(fp)) {
            fs.unlinkSync(fp)
        }

    })

    db.prepare(
        "DELETE FROM images WHERE id = ?"
    ).run(image.id)

    res.json({
        success: true,
        message: "Image deleted"
    })

})

module.exports = router
