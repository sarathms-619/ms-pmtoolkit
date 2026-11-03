# PM Toolkit

A free library of project management templates for project, delivery and program managers. Every template is filled with sample data and explained in plain English, so people who aren't PMs can follow it too.

The site has two ways in:

- **Documents by project:** Category → Project type → Documents → **When · How · Who · What** to create and update each one
- **Metrics playbook:** Category → Metric → **Impact** when it's off → **Resolution** steps

It also has an "All templates" library with filters, and a glossary. Jargon on every page is underlined; hover over it or tap it to see a definition.

| What | Count |
|---|---|
| Templates (Word, Excel with live formulas and charts, PowerPoint) | 25 |
| Project categories / types | 7 / 18 |
| Metric categories / metrics | 9 / 27 |
| Glossary terms | 51 |

All templates share one fictional project (Project Lighthouse at Halcyon Outfitters), so the numbers agree across documents. For example, the CPI of 0.90 in the EVM tracker is the same figure that appears in the status report, the dashboard and the SteerCo deck.

## Structure

```
generator/         Python: the content and the template generators (the source of truth)
  data.py                 sample project data used by every template
  gen_docx.py / gen_xlsx.py / gen_pptx.py   build the files
  catalog_documents.py    each document: plain-English explanation + when/how/who/what
  catalog_projects.py     categories > project types > which documents, priority, tailored timing
  catalog_metrics.py      metric categories > metrics > impact > resolution
  glossary.py             plain-English definitions
frontend/          Static site for Netlify (no build step)
  index.html, app.js, styles.css, config.js, _redirects
  catalog.json            generated
  files/                  generated templates
backend/           Cloudflare Worker: API, R2 file storage, D1 download counts
scripts/dev-server.mjs    local preview with the same routing as Netlify
netlify.toml
```

## Change content or regenerate

```bash
pip install python-docx openpyxl xlsxwriter python-pptx
```

```bash
python3 generator/build_files.py && python3 generator/build_catalog.py
```

`build_catalog.py` stops with an error if a project type or metric refers to a document that doesn't exist.

To put your name on the templates, change `BRAND` in `generator/data.py`.

## Preview locally

```bash
node scripts/dev-server.mjs 8080
```

Then open http://localhost:8080.

## Deploy

### 1. Cloudflare backend (optional but recommended)

The site works on Netlify alone. The Worker adds download counts and moves file hosting to R2.

```bash
cd backend && npm install && npx wrangler login
```

```bash
npx wrangler r2 bucket create pm-toolkit-files
```

```bash
npx wrangler d1 create pm-toolkit-db
```

Paste the `database_id` from that command into `backend/wrangler.toml`. Then set `ALLOWED_ORIGINS` to your Netlify URL and your portfolio domain.

```bash
npm run db:init && npm run upload && npm run deploy
```

### 2. Netlify frontend

1. Push this repo to GitHub and import it in Netlify. `netlify.toml` already sets the base folder.
2. If you deployed the Worker, set `apiBase` in `frontend/config.js` to the Worker URL.
3. Optional: add a custom subdomain such as `toolkit.yourportfolio.com`.

### 3. Link from your portfolio

Link to the Netlify URL, or deep-link straight to a page:

- `/projects/client-services/fixed-bid`
- `/metrics/cost/cpi`
- `/documents/raid-log`

## API

| Route | Returns |
|---|---|
| `GET /api/health` | `{ ok: true }` |
| `GET /api/catalog` | Full catalogue (R2 copy if uploaded, else bundled) |
| `GET /api/download/:file` | The template; counts the download (stores no IP or personal data) |
| `GET /api/stats` | `{ total, byFile }` |

Only files listed in the catalogue can be downloaded.
