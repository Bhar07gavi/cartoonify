const express = require("express")
const router = express.Router()

const { authenticateToken, deleteUser } = require("../auth")


// DELETE ACCOUNT
router.delete("/delete", authenticateToken, (req, res) => {

    try {

        const userId = req.user.id

        const { deleteUser } = require("../auth")

        deleteUser(userId)

        // destroy passport session if exists
        if (req.session) {
            req.session.destroy(() => { })
        }

        res.json({
            success: true,
            message: "Account deleted"
        })

    } catch (err) {

        console.error("Delete account error:", err)

        res.status(500).json({
            success: false,
            message: "Failed to delete account"
        })

    }

})

module.exports = router