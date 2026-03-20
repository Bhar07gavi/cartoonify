/**
 * Cartoonify - Database Initialization
 * Creates SQLite database with all required tables
 */

const Database = require("better-sqlite3")
const path = require("path")
const fs = require("fs")

const DB_PATH = path.join(__dirname, "..", "..", "database", "cartoonify.db")

/* ─────────────────────────────────────────
   Ensure database directory exists
───────────────────────────────────────── */

const dbDir = path.dirname(DB_PATH)

if (!fs.existsSync(dbDir)) {
  fs.mkdirSync(dbDir, { recursive: true })
}

/* ─────────────────────────────────────────
   Initialize DB
───────────────────────────────────────── */

const db = new Database(DB_PATH)

db.pragma("journal_mode = WAL")
db.pragma("foreign_keys = ON")

/* ─────────────────────────────────────────
   Create Tables
───────────────────────────────────────── */

db.exec(`

/* Users */

CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password TEXT,
  google_id TEXT,
  profile_image TEXT,
  is_admin INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


/* Images */

CREATE TABLE IF NOT EXISTS images (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  original_image TEXT NOT NULL,
  cartoon_image TEXT NOT NULL,
  style_used TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);


/* Videos */

CREATE TABLE IF NOT EXISTS videos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  original_video TEXT NOT NULL,
  cartoon_video TEXT NOT NULL,
  style_used TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);


/* Stickers */

CREATE TABLE IF NOT EXISTS stickers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  sticker_path TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

`)

console.log("✅ Cartoonify database initialized successfully at:", DB_PATH)

module.exports = db