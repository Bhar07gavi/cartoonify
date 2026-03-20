const express = require("express");
const router = express.Router();

const fetch = (...args) =>
    import("node-fetch").then(({ default: fetch }) => fetch(...args));

const config = require("../config/chatConfig");

router.post("/", async (req, res) => {
    try {

        const { message } = req.body;

        if (!message) {
            return res.json({ reply: "Please type a message." });
        }

        const msg = message.toLowerCase().trim();

        /* -----------------------------
           1️⃣ QUICK COMMANDS
        ------------------------------*/

        if (config.quickCommands[msg]) {
            return res.json({
                reply: config.quickCommands[msg]
            });
        }

        /* -----------------------------
           2️⃣ RULE BASED RESPONSES
        ------------------------------*/

        if (msg.includes("upload")) {
            return res.json({
                reply:
                    "To cartoonify an image:\n\n1️⃣ Upload your image\n2️⃣ Choose a style (Classic, Anime, Comic, Sketch, Watercolor, Minimal)\n3️⃣ Click **Cartoonify!**\n\nYour result will appear on the right."
            });
        }

        if (msg.includes("sticker")) {
            return res.json({
                reply:
                    "To create stickers:\n\n1️⃣ Open **Sticker Generator**\n2️⃣ Upload your image\n3️⃣ Generate sticker\n4️⃣ Download and share on WhatsApp."
            });
        }

        if (msg.includes("video")) {
            return res.json({
                reply:
                    "Use **Video Editor** to convert short videos into animated cartoon styles."
            });
        }

        if (msg.includes("portrait")) {
            return res.json({
                reply:
                    "For portraits try **Anime** or **Classic** style. They highlight facial expressions and details."
            });
        }

        if (msg.includes("black") || msg.includes("white") || msg.includes("bw")) {
            return res.json({
                reply:
                    "For black & white images try **Sketch** or **Comic** style. They preserve outlines and contrast."
            });
        }

        if (msg.includes("style")) {
            return res.json({
                reply:
                    "Available styles:\n\n🎨 Classic\n🎨 Anime\n🎨 Comic\n🎨 Sketch\n🎨 Watercolor\n🎨 Minimal"
            });
        }

        if (msg.includes("download")) {
            return res.json({
                reply:
                    "After your cartoon image appears in the result panel, you can download it directly from there."
            });
        }

        if (msg.includes("gallery")) {
            return res.json({
                reply:
                    "Your previous creations are stored in **My Gallery** where you can view and download them anytime."
            });
        }

        /* -----------------------------
           3️⃣ GEMINI AI RESPONSE
        ------------------------------*/

        const response = await fetch(
            `https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key=${process.env.GEMINI_API_KEY}`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    contents: [
                        {
                            parts: [
                                {
                                    text: `${config.systemPrompt}

User question: ${message}`
                                }
                            ]
                        }
                    ],
                    generationConfig: {
                        maxOutputTokens: 600,
                        temperature: 0.7
                    }
                })
            }
        );

        const data = await response.json();

        const reply =
            data?.candidates?.[0]?.content?.parts
                ?.map((p) => p.text)
                .join("") ||
            "Sorry, I couldn't generate a response.";

        res.json({ reply });

    } catch (err) {

        console.error("Gemini error:", err);

        res.json({
            reply:
                "AI assistant is temporarily unavailable. Please try again."
        });

    }
});

module.exports = router;