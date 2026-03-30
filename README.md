

# 🎨 Cartoonify – AI-Powered Cartoon Creator

A full-stack AI SaaS platform for transforming photos and videos into stunning cartoon styles using OpenCV, FastAPI, and Node.js.

## Features

- 🖼️ **Image Cartoonification** – 10 unique AI cartoon styles
- 🎬 **Video Cartoonification** – Frame-by-frame processing with MoviePy
- 📸 **Live Camera Filters** – Real-time cartoon effects via WebRTC
- 🧸 **Sticker Generator** – Background removal + PNG export
- 🎨 **10 Cartoon Styles**: Classic, Anime, Comic, Sketch, Oil Painting, Pixar, Pop Art, Watercolor, Sticker, Minimal
- 👤 **Google OAuth + Email Auth** with JWT sessions
- 🗂️ **Personal Gallery** with before/after comparison slider
- 👑 **Admin Panel** with user management

## Project Structure

```
cartoonify/
├── frontend/          ← HTML pages + CSS + JS
│   ├── css/style.css
│   ├── js/
│   ├── index.html     ← Landing page
│   ├── login.html
│   ├── dashboard.html
│   ├── upload.html    ← Image editor
│   ├── gallery.html
│   ├── video_editor.html
│   ├── live_camera.html
│   ├── admin.html
│   └── editor.html
├── backend/           ← Node.js Express server
│   ├── server.js
│   ├── auth.js
│   ├── routes/
│   └── database/
├── ai/                ← Python FastAPI AI server
│   ├── api.py
│   ├── cartoonify.py
│   ├── video_cartoon.py
│   ├── sticker_generator.py
│   └── styles.py
├── uploads/           ← Uploaded original files
├── outputs/           ← Processed cartoon outputs
│   ├── videos/
│   └── stickers/
├── database/          ← SQLite database
└── requirements.txt
```

## Prerequisites

- **Node.js** v18+ and npm
- **Python** 3.9+ with pip
- **ffmpeg** (required by MoviePy for video processing)

## Setup Instructions

### 1. Clone / Open the Project

```bash
cd d:\projects\toonify-node
```

### 2. Install Node.js Dependencies

```bash
npm install
```

### 3. Set Up Python Environment

```bash
# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Linux/Mac

# Install Python dependencies
pip install -r requirements.txt
```

> **Note**: `rembg` (used for sticker background removal) downloads a model (~170MB) on first use.

### 4. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your credentials:

```bash
copy .env.example .env
```

**Required for Google OAuth:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project → Enable Google+ API
3. Create OAuth 2.0 credentials (Web Application type)
4. Add `http://localhost:3000/auth/google/callback` as Authorized Redirect URI
5. Copy the Client ID and Secret to `.env`

### 5. Initialize the Database

```bash
npm run init-db
```

### 6. Start Both Servers

**Terminal 1 – Python AI Server:**
```bash
cd ai
python -m uvicorn api:app --host 0.0.0.0 --port 8001 --reload
```

**Terminal 2 – Node.js Backend:**
```bash
npm start
# or for development with auto-reload:
npm run dev
```

### 7. Open the App

Visit: **http://localhost:3000**

## API Endpoints

### Auth
| Method | URL | Description |
|--------|-----|-------------|
| POST | `/api/auth/register` | Register with email/password |
| POST | `/api/auth/login` | Login with email/password |
| GET  | `/api/auth/me` | Get current user profile |
| GET  | `/api/auth/stats` | Get user creation stats |
| GET  | `/auth/google` | Start Google OAuth flow |

### Images
| Method | URL | Description |
|--------|-----|-------------|
| POST | `/api/images/upload` | Upload + cartoonify image |
| GET  | `/api/images/:id` | Get image by ID |
| DELETE | `/api/images/:id` | Delete image |

### Gallery
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/gallery/images` | Get user's images |
| GET | `/api/gallery/videos` | Get user's videos |

### Admin (admin only)
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/admin/stats` | Platform statistics |
| GET | `/api/admin/users` | All users list |
| DELETE | `/api/admin/users/:id` | Delete user |
| PATCH | `/api/admin/users/:id/promote` | Toggle admin role |

### Python AI Server (port 8001)
| Method | URL | Description |
|--------|-----|-------------|
| POST | `/cartoonify-image` | Cartoonify image |
| POST | `/cartoonify-video` | Cartoonify video |
| POST | `/generate-sticker` | Generate sticker PNG |
| GET  | `/docs` | Swagger API docs |

## Cartoon Styles

| Key | Name | Description |
|-----|------|-------------|
| `classic` | Classic Cartoon | Standard bilateral filter cartoon |
| `anime` | Anime Style | Enhanced edges + high saturation |
| `comic` | Comic Book | Bold outlines + high contrast |
| `sketch` | Sketch Style | Pencil sketch effect |
| `oil` | Oil Painting | Heavy bilateral + texture |
| `pixar` | Pixar Style | Soft rounded cartoon look |
| `popart` | Pop Art | Posterized + vibrant colors |
| `watercolor` | Watercolor | Soft edges + pastel tones |
| `sticker` | Sticker Mode | Opaque cartoon for stickers |
| `minimal` | Minimal Cartoon | Subtle, clean cartoon |

## Make First Admin User

After registering your first account, run this in the project root:

```bash
node -e "const db = require('./backend/database/init.db'); db.prepare('UPDATE users SET is_admin = 1 WHERE email = ?').run('your@email.com'); console.log('Done!');"
```

## Technologies

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, CSS3, Bootstrap 5.3, jQuery 3.7 |
| Backend | Node.js 18+, Express 4 |
| AI Server | Python 3.9+, FastAPI, Uvicorn |
| AI Processing | OpenCV, NumPy, Pillow, MediaPipe |
| Video | MoviePy, ffmpeg |
| Background Removal | rembg |
| Database | SQLite (via better-sqlite3) |
| Auth | Passport.js, Google OAuth 2.0, JWT |
| Media | Multer (file uploads) |
>>>>>>> 01af42b (Initial clean commit - cartoonify project)
