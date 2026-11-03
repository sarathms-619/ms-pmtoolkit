// PM Toolkit API (Cloudflare Worker)
//
// GET /api/health            -> { ok: true }
// GET /api/catalog           -> the full catalogue (R2 copy if uploaded, else the bundled one)
// GET /api/download/:file    -> streams a template from R2 and counts the download in D1
// GET /api/stats             -> { total, byFile: { "raid-log.xlsx": 12, ... } }

import bundledCatalog from "./catalog.json";

const MIME = {
  docx: "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  xlsx: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  pptx: "application/vnd.openxmlformats-officedocument.presentationml.presentation",
};

// Only files listed in the catalogue can be downloaded.
const ALLOWED_FILES = new Set(bundledCatalog.documents.map((d) => d.file));

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const cors = corsHeaders(request, env);

    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: cors });
    if (request.method !== "GET" && request.method !== "HEAD") {
      return json({ error: "Method not allowed" }, 405, cors);
    }

    try {
      if (url.pathname === "/api/health") return json({ ok: true }, 200, cors);
      if (url.pathname === "/api/catalog") return catalog(env, cors);
      if (url.pathname === "/api/stats") return stats(env, cors);
      const m = url.pathname.match(/^\/api\/download\/([a-z0-9-]+\.(docx|xlsx|pptx))$/);
      if (m) return download(m[1], m[2], request, env, ctx, cors);
      return json({ error: "Not found" }, 404, cors);
    } catch (err) {
      console.error(err);
      return json({ error: "Something went wrong on our side. Try again in a minute." }, 500, cors);
    }
  },
};

async function catalog(env, cors) {
  let body = null;
  if (env.FILES) {
    const obj = await env.FILES.get("catalog.json");
    if (obj) body = await obj.text();
  }
  body = body || JSON.stringify(bundledCatalog);
  return new Response(body, {
    headers: { ...cors, "content-type": "application/json; charset=utf-8", "cache-control": "public, max-age=300" },
  });
}

async function download(file, ext, request, env, ctx, cors) {
  if (!ALLOWED_FILES.has(file)) return json({ error: "That template does not exist." }, 404, cors);
  const obj = await env.FILES.get(`files/${file}`);
  if (!obj) return json({ error: "Template not uploaded yet." }, 404, cors);

  if (env.DB && request.method === "GET") {
    const country = request.cf?.country || null;
    const ref = request.headers.get("referer");
    const referrer = ref ? safeHost(ref) : null; // store only the host, never full URLs
    ctx.waitUntil(
      env.DB.prepare("INSERT INTO downloads (file, country, referrer) VALUES (?, ?, ?)")
        .bind(file, country, referrer).run().catch((e) => console.error("count failed", e))
    );
  }

  return new Response(request.method === "HEAD" ? null : obj.body, {
    headers: {
      ...cors,
      "content-type": MIME[ext],
      "content-disposition": `attachment; filename="${file}"`,
      "content-length": String(obj.size),
      "cache-control": "public, max-age=3600",
      etag: obj.httpEtag,
    },
  });
}

async function stats(env, cors) {
  if (!env.DB) return json({ total: 0, byFile: {} }, 200, cors);
  const { results } = await env.DB.prepare("SELECT file, COUNT(*) AS n FROM downloads GROUP BY file").all();
  const byFile = {};
  let total = 0;
  for (const r of results) { byFile[r.file] = r.n; total += r.n; }
  return new Response(JSON.stringify({ total, byFile }), {
    headers: { ...cors, "content-type": "application/json", "cache-control": "public, max-age=120" },
  });
}

function corsHeaders(request, env) {
  const origin = request.headers.get("origin");
  const allowed = (env.ALLOWED_ORIGINS || "").split(",").map((s) => s.trim()).filter(Boolean);
  const ok = origin && (allowed.includes("*") || allowed.includes(origin));
  return {
    "access-control-allow-origin": ok ? origin : allowed[0] || "*",
    "access-control-allow-methods": "GET, HEAD, OPTIONS",
    "access-control-allow-headers": "content-type",
    "access-control-expose-headers": "content-disposition",
    vary: "origin",
  };
}

function json(obj, status, cors) {
  return new Response(JSON.stringify(obj), { status, headers: { ...cors, "content-type": "application/json" } });
}

function safeHost(u) {
  try { return new URL(u).host; } catch { return null; }
}
