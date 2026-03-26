const passport = require("passport")
const GoogleStrategy = require("passport-google-oauth20").Strategy
const db = require("../database/init.db")

passport.use(
    new GoogleStrategy(
        {
            clientID: process.env.GOOGLE_CLIENT_ID,
            clientSecret: process.env.GOOGLE_CLIENT_SECRET,
            callbackURL: "https://cartoonify-backend-ordt.onrender.com/api/auth/google"
        },
        (accessToken, refreshToken, profile, done) => {

            try {

                const email = profile.emails[0].value
                const name = profile.displayName
                const googleId = profile.id
                const image = profile.photos[0]?.value || ""

                let user = db.prepare("SELECT * FROM users WHERE email=?").get(email)

                if (!user) {

                    const result = db.prepare(`
                        INSERT INTO users (name,email,google_id,profile_image)
                        VALUES (?,?,?,?)
                    `).run(name, email, googleId, image)

                    user = db.prepare("SELECT * FROM users WHERE id=?")
                        .get(result.lastInsertRowid)

                }

                return done(null, user)

            } catch (err) {

                return done(err, null)

            }

        }
    )
)

passport.serializeUser((user, done) => done(null, user.id))

passport.deserializeUser((id, done) => {

    const user = db.prepare("SELECT * FROM users WHERE id=?").get(id)

    done(null, user)

})
