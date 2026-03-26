const express = require("express")
const passport = require("passport")
const { generateToken } = require("../auth")

const router = express.Router()

/* Google login */
router.get(
    "/google",
    passport.authenticate("google", {
        scope: ["profile", "email"]
    })
)

/* Google callback */
router.get(
    "/google/callback",
    passport.authenticate("google", { failureRedirect: "https://cartoonify-jade.vercel.app/login.html" }),
    (req, res) => {

        try {

            const user = req.user

            const token = generateToken(user)

            // send token to frontend
            res.redirect(`https://cartoonify-jade.vercel.app/dashboard.html?token=${token}`)

        } catch (err) {

            console.error("Google auth error:", err)

            res.redirect("dashboard.html")

        }

    }
)

module.exports = router
