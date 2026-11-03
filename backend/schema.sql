-- One row per download. No IP addresses or personal data are stored.
CREATE TABLE IF NOT EXISTS downloads (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  file       TEXT NOT NULL,
  country    TEXT,
  referrer   TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_downloads_file ON downloads(file);
