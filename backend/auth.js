const jwt = require("jsonwebtoken")
const bcrypt = require("bcryptjs")
const db = require("./database/init.db")

const fs = require("fs")
const path = require("path")

const JWT_SECRET = process.env.JWT_SECRET || "cartoonify_secret"


// ------------------------------------------------
// Generate JWT Token
// ------------------------------------------------

function generateToken(user) {

    return jwt.sign(
        {
            id: user.id,
            email: user.email,
            is_admin: user.is_admin
        },
        JWT_SECRET,
        { expiresIn: "30d" }
    )

}


// ------------------------------------------------
// Auth Middleware
// ------------------------------------------------

function authenticateToken(req, res, next) {

    const authHeader = req.headers["authorization"]
    const token = authHeader && authHeader.split(" ")[1]

    if (!token) {

        return res.status(401).json({
            success: false,
            message: "Token required"
        })

    }

    try {

        const decoded = jwt.verify(token, JWT_SECRET)
        req.user = decoded
        next()

    } catch (err) {

        return res.status(403).json({
            success: false,
            message: "Invalid token"
        })

    }

}


// ------------------------------------------------
// Register User
// ------------------------------------------------

async function registerUser(name, email, password) {

    const existing = db.prepare(
        "SELECT id FROM users WHERE email=?"
    ).get(email)

    if (existing) {
        throw new Error("Email already registered")
    }

    const hashed = await bcrypt.hash(password, 10)

    const result = db.prepare(`
INSERT INTO users(name,email,password)
VALUES(?,?,?)
`).run(name, email, hashed)

    return db.prepare(
        "SELECT id,name,email,created_at FROM users WHERE id=?"
    ).get(result.lastInsertRowid)

}


// ------------------------------------------------
// Login User
// ------------------------------------------------

async function loginUser(email, password) {

    const user = db.prepare(
        "SELECT * FROM users WHERE email=?"
    ).get(email)

    if (!user) {
        throw new Error("Invalid credentials")
    }

    const valid = await bcrypt.compare(password, user.password)

    if (!valid) {
        throw new Error("Invalid credentials")
    }

    return user

}


// ------------------------------------------------
// Update Profile
// ------------------------------------------------

async function updateUser(userId, name, password) {

    if (name) {

        db.prepare(`
UPDATE users
SET name=?
WHERE id=?
`).run(name, userId)

    }

    if (password) {

        const hashed = await bcrypt.hash(password, 10)

        db.prepare(`
UPDATE users
SET password=?
WHERE id=?
`).run(hashed, userId)

    }

    return db.prepare(
        "SELECT id,name,email,created_at FROM users WHERE id=?"
    ).get(userId)

}

function requireAdmin(req, res, next) {

    if (!req.user || !req.user.is_admin) {

        return res.status(403).json({
            success: false,
            message: "Admin access required"
        })

    }

    next()

}
// ------------------------------------------------
// Delete User Account
// ------------------------------------------------
function deleteUser(userId) {

    try {

        /* delete image files */

        const images = db.prepare(`
SELECT original_image, cartoon_image
FROM images
WHERE user_id=?
`).all(userId)

        for (const img of images) {

            const orig = path.join(__dirname, "../uploads", img.original_image)
            const cartoon = path.join(__dirname, "../uploads", img.cartoon_image)

            if (fs.existsSync(orig)) fs.unlinkSync(orig)
            if (fs.existsSync(cartoon)) fs.unlinkSync(cartoon)

        }


        /* delete video files */

        const videos = db.prepare(`
SELECT original_video, cartoon_video
FROM videos
WHERE user_id=?
`).all(userId)

        for (const v of videos) {

            const orig = path.join(__dirname, "../uploads", v.original_video)
            const cartoon = path.join(__dirname, "../uploads", v.cartoon_video)

            if (fs.existsSync(orig)) fs.unlinkSync(orig)
            if (fs.existsSync(cartoon)) fs.unlinkSync(cartoon)

        }


        /* delete sticker files */

        const stickers = db.prepare(`
SELECT sticker_path
FROM stickers
WHERE user_id=?
`).all(userId)

        for (const s of stickers) {

            const file = path.join(__dirname, "../uploads", s.sticker_path)

            if (fs.existsSync(file)) fs.unlinkSync(file)

        }


        /* delete database records */

        db.prepare(`DELETE FROM images WHERE user_id=?`).run(userId)
        db.prepare(`DELETE FROM videos WHERE user_id=?`).run(userId)
        db.prepare(`DELETE FROM stickers WHERE user_id=?`).run(userId)
        db.prepare(`DELETE FROM users WHERE id=?`).run(userId)

        return { success: true }

    } catch (err) {

        console.error("Delete user error:", err)

        return { success: false }

    }

}



// ------------------------------------------------
// Export
// ------------------------------------------------

module.exports = {
    requireAdmin,
    generateToken,
    authenticateToken,
    registerUser,
    loginUser,
    updateUser,
    deleteUser

}