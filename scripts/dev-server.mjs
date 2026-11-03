// Local preview of the frontend with the same single-page fallback as Netlify.
// Usage: node scripts/dev-server.mjs [port]      (PMT_API=http://localhost:8787 to use the local Worker)
import http from "node:http";
import { readFile, stat } from "node:fs/promises";
import { extname, join, normalize } from "node:path";
import { fileURLToPath } from "node:url";

const root = fileURLToPath(new URL("../frontend/", import.meta.url));
const port = Number(process.argv[2] || 8080);
const types = { ".html": "text/html; charset=utf-8", ".js": "text/javascript", ".css": "text/css", ".json": "application/json",
  ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation" };

http.createServer(async (req, res) => {
  const path = decodeURIComponent(new URL(req.url, "http://x").pathname);
  if (path === "/config.js" && process.env.PMT_API) {
    res.writeHead(200, { "content-type": "text/javascript" });
    return res.end(`window.PMT_CONFIG = { apiBase: ${JSON.stringify(process.env.PMT_API)}, siteName: "PM Toolkit" };`);
  }
  let file = normalize(join(root, path));
  if (!file.startsWith(root)) { res.writeHead(403); return res.end(); }
  try { if ((await stat(file)).isDirectory()) file = join(file, "index.html"); }
  catch { file = join(root, "index.html"); }
  try {
    const body = await readFile(file);
    res.writeHead(200, { "content-type": types[extname(file)] || "application/octet-stream" });
    res.end(body);
  } catch { res.writeHead(404); res.end("Not found"); }
}).listen(port, () => console.log(`Preview on http://localhost:${port}`));
