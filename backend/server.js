/**
 * Cartoonify - Express Server
 * Clean and corrected backend
 */

require("dotenv").config()

const express = require("express")
const cors = require("cors")
const morgan = require("morgan")
const session = require("express-session")
const passport = require("passport")
require("./config/passport")
const path = require("path")
const fs = require("fs")

const db = require("./database/init.db")
const { generateToken, authenticateToken, updateUser } = require("./auth")

const app = express()
const PORT = process.env.PORT || 3000


/* ─────────────────────────────────────────
   PATHS
───────────────────────────────────────── */

const BACKEND_DIR = __dirname
const ROOT = path.resolve(__dirname, "..")
const FRONTEND = path.join(ROOT, "frontend")

console.log("Backend:", BACKEND_DIR)
console.log("Root:", ROOT)
console.log("Frontend:", FRONTEND)


/* ─────────────────────────────────────────
   CREATE REQUIRED DIRECTORIES
───────────────────────────────────────── */

const REQUIRED_DIRS = [

    path.join(ROOT, "uploads"),
    path.join(ROOT, "outputs"),
    path.join(ROOT, "outputs/videos"),
    path.join(ROOT, "outputs/stickers")

]

REQUIRED_DIRS.forEach(dir => {

    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true })
        console.log("Created directory:", dir)
    }

})


/* ─────────────────────────────────────────
   MIDDLEWARE
───────────────────────────────────────── */

app.use(cors({
    origin: [
        'https://cartoonify-jade.vercel.app',
        'http://localhost:5500',
        'http://localhost:3000',
        'http://127.0.0.1:5500'
    ],
    credentials: true,
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization']
}))


app.use(morgan("dev"))

app.use(express.json({ limit: "20mb" }))
app.use(express.urlencoded({ extended: true }))

app.use(
    session({
        secret: process.env.SESSION_SECRET || "cartoonify_secret",
        resave: false,
        saveUninitialized: false
    })
)

app.use(passport.initialize())
app.use(passport.session())



   app.get("/health", (req, res) => {
    res.json({
        status: "healthy",
        timestamp: new Date().toISOString(),
        environment: process.env.NODE_ENV || "development",
        aiService: process.env.AI_SERVICE_URL || "not configured"
    })
})

/* ─────────────────────────────────────────
   STATIC FILES
───────────────────────────────────────── */

/* Frontend */
app.use(express.static(FRONTEND))

/* Uploaded images/videos */
app.use("/uploads", express.static(path.join(ROOT, "uploads")))

/* AI processed outputs */
app.use("/outputs", express.static(path.join(ROOT, "outputs")))


/* ─────────────────────────────────────────
   API ROUTES
───────────────────────────────────────── */

const imageRoutes = require("./routes/imageRoutes")
const videoRoutes = require("./routes/videoRoutes")
const galleryRoutes = require("./routes/galleryRoutes")
const adminRoutes = require("./routes/adminRoutes")
const stickerRoutes = require("./routes/stickerRoutes")
const chatRoutes = require("./routes/chatRoutes")
const authRoutes = require("./routes/authRoutes")

app.use("/api/chat", chatRoutes)
app.use("/api/images", imageRoutes)
app.use("/api/videos", videoRoutes)
app.use("/api/gallery", galleryRoutes)
app.use("/api/admin", adminRoutes)
app.use("/api/sticker", stickerRoutes)
app.use("/api/auth", authRoutes)
/* ─────────────────────────────────────────
   GOOGLE AUTH ROUTES
───────────────────────────────────────── */

const googleAuthRoutes = require("./routes/googleAuth")

app.use("/auth", googleAuthRoutes)
/* ─────────────────────────────────────────
   AUTH ROUTES
───────────────────────────────────────── */

const { registerUser, loginUser } = require("./auth")

app.post("/api/auth/register", async (req, res) => {

    try {

        const user = await registerUser(
            req.body.name,
            req.body.email,
            req.body.password
        )

        const token = generateToken(user)

        res.json({
            success: true,
            token,
            user
        })

    } catch (err) {

        res.status(400).json({
            success: false,
            message: err.message
        })

    }

})

app.post("/api/auth/update", authenticateToken, async (req, res) => {

    try {

        const { name, password } = req.body

        const user = await updateUser(req.user.id, name, password)

        res.json({
            success: true,
            user
        })

    } catch (err) {

        console.error(err)
        res.status(500).json({ success: false })

    }

})

app.post("/api/auth/login", async (req, res) => {

    try {

        const user = await loginUser(
            req.body.email,
            req.body.password
        )

        const token = generateToken(user)

        res.json({
            success: true,
            token,
            user
        })

    } catch (err) {

        res.status(401).json({
            success: false,
            message: err.message
        })

    }

})


/* ─────────────────────────────────────────
   USER PROFILE
───────────────────────────────────────── */

app.get("/api/auth/me", authenticateToken, (req, res) => {

    const user = db.prepare(`
        SELECT id, name, email, profile_image, is_admin, created_at
        FROM users
        WHERE id = ?
    `).get(req.user.id)

    res.json({
        success: true,
        user
    })

})


/* ─────────────────────────────────────────
   DASHBOARD STATS
───────────────────────────────────────── */

app.get("/api/auth/stats", authenticateToken, (req, res) => {

    try {

        const userId = req.user.id

        const totalImages = db.prepare(`
            SELECT COUNT(*) as count FROM images WHERE user_id = ?
        `).get(userId).count

        const totalVideos = db.prepare(`
            SELECT COUNT(*) as count FROM videos WHERE user_id = ?
        `).get(userId).count

        const totalStickers = db.prepare(`
            SELECT COUNT(*) as count FROM stickers WHERE user_id = ?
        `).get(userId).count

        const recentImages = db.prepare(`
            SELECT cartoon_image, style_used, created_at
            FROM images
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT 8
        `).all(userId)

        res.json({
            success: true,
            stats: {
                total_images: totalImages,
                total_videos: totalVideos,
                total_stickers: totalStickers,
                recent_images: recentImages
            }
        })

    } catch (err) {

        console.error("Stats error:", err)

        res.status(500).json({
            success: false,
            message: "Failed to load dashboard stats"
        })

    }

})


/* ─────────────────────────────────────────
   FRONTEND ROUTES
───────────────────────────────────────── */

app.get("/", (req, res) => {
    res.sendFile(path.join(FRONTEND, "index.html"))
})

app.get("/login", (req, res) => {
    res.sendFile(path.join(FRONTEND, "login.html"))
})

app.get("/dashboard", (req, res) => {
    res.sendFile(path.join(FRONTEND, "dashboard.html"))
})

app.get("/upload", (req, res) => {
    res.sendFile(path.join(FRONTEND, "upload.html"))
})

app.get("/video_editor", (req, res) => {
    res.sendFile(path.join(FRONTEND, "video_editor.html"))
})

app.get("/sticker", (req, res) => {
    res.sendFile(path.join(FRONTEND, "sticker.html"))
})

app.get("/gallery", (req, res) => {
    res.sendFile(path.join(FRONTEND, "gallery.html"))
})


/* ─────────────────────────────────────────
   API FALLBACK
───────────────────────────────────────── */

app.use("/api", (req, res) => {

    res.status(404).json({
        success: false,
        message: "API route not found"
    })

})


/* ─────────────────────────────────────────
   START SERVER
───────────────────────────────────────── */

app.listen(PORT, () => {

    console.log(`
🎨 Cartoonify Server running

Frontend:
http://localhost:${PORT}

API:
http://localhost:${PORT}/api
`)

})

module.exports = app
