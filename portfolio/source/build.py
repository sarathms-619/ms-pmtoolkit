"""Builds site/index.html from index.original.html.

Every change is a named, checked replacement, so the original stays untouched
and each edit fails loudly if the source changes underneath it.
Run:  python3 build.py
"""
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "essays"))
from essays_ab import ESSAYS_AB  # noqa: E402
from essays_hi import ESSAYS_HI  # noqa: E402

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "index.original.html")
OUT = os.path.join(ROOT, "..", "site", "index.html")

TOOLKIT_URL = "https://ms-pmtoolkit.netlify.app"   # change if your Netlify site name differs
RESUME_PATH = "resume/sarathms_resume_2026.pdf"

s = open(SRC, encoding="utf-8").read()


def rep(old, new, count=1, label=""):
    global s
    n = s.count(old)
    if n != count:
        sys.exit(f"[{label}] expected {count} match(es), found {n}: {old[:80]!r}")
    s = s.replace(old, new)


def insert_before(anchor, text, after_pos=0, label=""):
    """Insert text before the first occurrence of anchor at or after after_pos."""
    global s
    i = s.find(anchor, after_pos)
    if i < 0:
        sys.exit(f"[{label}] anchor not found: {anchor[:60]!r}")
    s = s[:i] + text + s[i:]
    return i


# ─────────────────────────────────────────────────────────── 1. RESUME
rep('<a class="nav-cta" href="sarathms_resume_2026.pdf" target="_blank">Resume ↗</a>',
    f'<a class="nav-cta" href="{RESUME_PATH}" target="_blank" rel="noopener">Resume ↗</a>', label="nav resume")
rep('<a class="btn-resume-hero" href="sarathms_resume_2026.pdf" target="_blank" onclick="resumeDownload(event)">Download Resume ↓</a>',
    f'<a class="btn-resume-hero" href="{RESUME_PATH}" download="Sarath_MS_Delivery_Operations.pdf">Download Resume ↓</a>', label="hero resume")
# The old fetch-and-blob handler is no longer used by any link; keep a harmless stub.
start = s.index("function resumeDownload(e) {")
end = s.index("// ═══════════════════════════════════════\n// TESTIMONIAL CAROUSEL", start)
s = s[:start] + "function resumeDownload() { /* links now download directly */ }\n\n" + s[end:]

# ─────────────────────────────────────────────────────────── 2. NAV
rep("""      <li><button onclick="showPage('work')" id="nav-work">Work</button></li>
""", """      <li><button onclick="showPage('work')" id="nav-work">Work</button></li>
      <li><button onclick="showPage('toolkit')" id="nav-toolkit">Toolkit</button></li>
""", label="nav toolkit")
rep("""<button class="nav-vcard-btn" onclick="document.getElementById('vcardOverlay').style.display='flex'" title="Get in touch">📇</button>""",
    """<button class="nav-contact" onclick="document.getElementById('vcardOverlay').style.display='flex'">Contact</button>""",
    label="contact button")

MOBILE_NAV = """
<!-- ── MOBILE TAB BAR (phones only) ── -->
<nav class="mtab" aria-label="Sections">
  <button onclick="showPage('home')" data-page="home" class="active">Overview</button>
  <button onclick="showPage('about')" data-page="about">About</button>
  <button onclick="showPage('thinking')" data-page="thinking">Thinking</button>
  <button onclick="showPage('work')" data-page="work">Work</button>
  <button onclick="showPage('toolkit')" data-page="toolkit">Toolkit</button>
</nav>
"""
rep("<footer>\n", MOBILE_NAV + "<footer>\n", label="mobile nav")
rep("""  const activeBtn = document.getElementById('nav-' + name);
  if (activeBtn) activeBtn.classList.add('active');
""", """  const activeBtn = document.getElementById('nav-' + name);
  if (activeBtn) activeBtn.classList.add('active');
  document.querySelectorAll('.mtab button').forEach(b => b.classList.toggle('active', b.dataset.page === name));
""", label="mobile nav active state")

# ─────────────────────────────────────────────────────────── 3. FOOTER
rep("""    <div class="footer-mark">Built without a developer background.</div>
  </div>
</footer>""", """    <div class="footer-links">
      <a href="#" onclick="showPage('toolkit');return false;">PM Toolkit</a>
      <a href="#" onclick="showPage('thinking');return false;">Delivery Dilemmas</a>
      <a href="https://www.linkedin.com/in/sarath-m-158228a7" target="_blank" rel="noopener">LinkedIn</a>
      <a href="RESUME" target="_blank" rel="noopener">Resume</a>
    </div>
  </div>
</footer>""".replace("RESUME", RESUME_PATH), label="footer")

# ─────────────────────────────────────────────────────────── 4. TOOLKIT PAGE
TOOLKIT_TYPES = [
    ("software-digital/agile-product-build", "Software & Digital", "Agile product build", "12 documents · 3-12 months"),
    ("enterprise-it/erp-implementation", "Enterprise IT", "ERP implementation", "22 documents · 9-24 months"),
    ("client-services/fixed-bid", "Client Services", "Fixed-bid client engagement", "12 documents · 1-6 months"),
    ("infrastructure-cloud/cloud-migration", "Infrastructure & Cloud", "Cloud migration", "11 documents · 6-18 months"),
    ("data-ai/ai-ml-pilot", "Data & AI", "AI / ML pilot", "7 documents · 6-16 weeks"),
    ("program-portfolio/multi-project-program", "Programs & Portfolio", "Multi-project program", "10 documents · 1-3 years"),
]
TOOLKIT_DOCS = [
    ("raid-log", "XLSX", "RAID Log", "Risks, assumptions, issues, dependencies and decisions, with an automatic heat map."),
    ("budget-evm-tracker", "XLSX", "Budget & EVM Tracker", "Planned vs earned vs actual, CPI, SPI and forecast at completion, with an S-curve."),
    ("weekly-status-report", "DOCX", "Weekly Status Report", "One page: RAG by dimension, a summary for busy readers, risks and asks."),
    ("steering-committee-deck", "PPTX", "Steering Committee Deck", "Seven slides built around one decision, with an editable EVM chart."),
    ("project-health-dashboard", "XLSX", "Project Health Dashboard", "KPI tiles, RAG by dimension and three charts on one screen."),
    ("project-charter", "DOCX", "Project Charter", "The official go-ahead: objectives, scope, milestones, budget, governance."),
]
types_html = "\n".join(
    f'''          <a class="tk-type" href="{TOOLKIT_URL}/projects/{path}" target="_blank" rel="noopener">
            <span class="tk-type-cat">{cat}</span>
            <span class="tk-type-name">{name}</span>
            <span class="tk-type-meta">{meta}</span>
          </a>''' for path, cat, name, meta in TOOLKIT_TYPES)
docs_html = "\n".join(
    f'''          <a class="tk-doc" href="{TOOLKIT_URL}/documents/{slug}" target="_blank" rel="noopener">
            <span class="tk-fmt tk-fmt--{fmt.lower()}">{fmt}</span>
            <span class="tk-doc-body"><span class="tk-doc-name">{name}</span><span class="tk-doc-desc">{desc}</span></span>
            <span class="tk-doc-arrow">↗</span>
          </a>''' for slug, fmt, name, desc in TOOLKIT_DOCS)

TOOLKIT_PAGE = f"""
<!-- ══════════════════════════════════════════════
     TOOLKIT
══════════════════════════════════════════════ -->
<div id="page-toolkit" class="page">
  <div class="tk-hero">
    <div class="wrap">
      <div class="eyebrow">Toolkit</div>
      <h1 class="tk-title">Every document a project needs. <em>And when to use it.</em></h1>
      <p class="tk-sub">A free library of 25 project templates, filled with one worked example so every number lines up across documents. Pick the kind of project you're running and see which documents it needs, when to create and update each one, how, and who owns it. Written in plain English, so it works for people who aren't project managers too.</p>
      <div class="tk-cta-row">
        <a class="btn-primary" href="{TOOLKIT_URL}" target="_blank" rel="noopener">Open the toolkit ↗</a>
        <a class="btn-ghost" href="{TOOLKIT_URL}/library" target="_blank" rel="noopener">Browse all templates</a>
      </div>
    </div>
  </div>

  <div class="tk-band">
    <div class="wrap tk-figures">
      <div><b>25</b><span>Templates</span></div>
      <div><b>18</b><span>Project types mapped</span></div>
      <div><b>27</b><span>Metrics explained</span></div>
      <div><b>51</b><span>Terms in plain English</span></div>
    </div>
  </div>

  <div class="wrap">
    <div class="tk-tracks">
      <a class="tk-track" href="{TOOLKIT_URL}/projects" target="_blank" rel="noopener">
        <span class="tk-track-label">Track 1</span>
        <span class="tk-track-title">Documents by project</span>
        <span class="tk-track-desc">Start from the kind of project you're running. Get only the documents it needs, in the order you'll need them.</span>
        <span class="tk-path"><i>Category</i><i>Project type</i><i>Documents</i><i class="on">When · How · Who · What</i></span>
      </a>
      <a class="tk-track" href="{TOOLKIT_URL}/metrics" target="_blank" rel="noopener">
        <span class="tk-track-label">Track 2</span>
        <span class="tk-track-title">Metrics playbook</span>
        <span class="tk-track-desc">For each number on a status report: what it means, what happens when it's off target, and what to do about it.</span>
        <span class="tk-path"><i>Category</i><i>Metric</i><i>Impact</i><i class="on">Resolution</i></span>
      </a>
    </div>

    <section class="tk-section">
      <div class="tk-section-head"><h2>Start with your project.</h2><a href="{TOOLKIT_URL}/projects" target="_blank" rel="noopener">All 18 project types ↗</a></div>
      <div class="tk-types">
{types_html}
      </div>
    </section>

    <section class="tk-section">
      <div class="tk-section-head"><h2>Most-used templates.</h2><a href="{TOOLKIT_URL}/library" target="_blank" rel="noopener">All 25 templates ↗</a></div>
      <div class="tk-docs">
{docs_html}
      </div>
    </section>

    <section class="tk-why">
      <div class="eyebrow">Why I built it</div>
      <p>Most template packs give you an empty form and leave the judgement to you. The judgement is the hard part: which documents a project actually needs, when they earn their keep, and what to do when the numbers turn amber. This toolkit is the version I wish someone had handed me fourteen years ago, with the reasoning left in.</p>
    </section>
  </div>
</div><!-- /page-toolkit -->
"""
insert_before("<!-- ══════════════════════════════════════════════\n     WORK", TOOLKIT_PAGE, label="toolkit page")

# Home teaser band, between "Notes from the field" and "Selected work".
HOME_TEASER = f"""
  <!-- TOOLKIT TEASER -->
  <div class="tk-teaser">
    <div class="wrap">
      <a class="tk-teaser-inner" href="#" onclick="showPage('toolkit');return false;">
        <span class="tk-teaser-tag">New · Free</span>
        <span class="tk-teaser-text"><b>The PM Toolkit.</b> 25 templates, mapped to 18 project types, with a metrics playbook. Explained so anyone can use them.</span>
        <span class="tk-teaser-go">Explore →</span>
      </a>
    </div>
  </div>
"""
insert_before("  <!-- WORK PREVIEW -->", HOME_TEASER, label="home teaser")

# ─────────────────────────────────────────────────────────── 5. NEW ESSAYS
CAT_TAG = {"A": "A · Scope", "B": "B · Resource", "H": "H · PM Position", "I": "I · AI Layer"}
P_STYLE_OPEN = '<p style="font-family:var(--serif);font-size:22px;font-style:italic;color:var(--ink);line-height:1.65;margin-bottom:28px;">'
PULL = '<div style="border-left:2px solid var(--green);padding-left:22px;margin:32px 0;"><p style="font-family:var(--serif);font-size:19px;font-style:italic;color:var(--ink2);line-height:1.7;margin:0;">{}</p></div>'


def para(t):
    return f"<p>{html.escape(t, quote=False)}</p>"


def render(e):
    out = [P_STYLE_OPEN + html.escape(e["hook"], quote=False) + "</p>"]
    out.append("<h3>The Situation</h3>"); out += [para(p) for p in e["situation"]]
    out.append("<h3>The Ideal World</h3>"); out += [para(p) for p in e["ideal"]]
    out.append("<h3>Why That Doesn't Work</h3>"); out += [para(p) for p in e["why"]]
    out.append("<h3>My Thought Process</h3>"); out += [para(p) for p in e["thought"]]
    out.append("<h3>Possible Options</h3>")
    for i, (name, works, fails, cost) in enumerate(e["options"]):
        out.append(f'<div class="dd-option"><div class="dd-option-name">Option {"ABC"[i]} · {html.escape(name)}</div>'
                   f'<dl><dt>Works when</dt><dd>{html.escape(works)}</dd><dt>Fails when</dt><dd>{html.escape(fails)}</dd>'
                   f'<dt>The cost</dt><dd>{html.escape(cost)}</dd></dl></div>')
    out.append("<h3>What I'd Do</h3>"); out += [para(p) for p in e["do"]]
    out.append(PULL.format(html.escape(e["pull"], quote=False)))
    out.append("<h3>What Changed My Thinking</h3>"); out += [para(p) for p in e["changed"]]
    out.append("<h3>Principles Behind the Decision</h3>")
    out.append('<ul class="dd-principles">' + "".join(
        f"<li><strong>{html.escape(n)}.</strong> {html.escape(t)}</li>" for n, t in e["principles"]) + "</ul>")
    return "\n".join(out)


new_essays = ESSAYS_AB + ESSAYS_HI
# Index of the first new essay = current length of ESSAYS.
a = s.index("const ESSAYS = [")
b = s.index("const SPECIAL_ESSAYS")
close = s.rfind("];", a, b)
existing = s[a:close].count("\n  {\n    tag:")
base_idx = existing
js_items = []
for e in new_essays:
    obj = {"tag": f"Delivery Dilemmas · Debrief {e['num']} · Category {e['cat']}", "title": e["title"], "time": e["time"], "body": render(e)}
    js_items.append("  " + json.dumps(obj, ensure_ascii=False))
s = s[:close].rstrip() + ",\n" + ",\n".join(js_items) + "\n" + s[close:]

# Category cards: append rows to A, B, H, I.
for cat in ["A", "B", "H", "I"]:
    pos = s.index(f'<div class="tl-cat-letter">{cat}</div>')
    rows = ""
    for k, e in enumerate(new_essays):
        if e["cat"] != cat:
            continue
        rows += f"""
              <div class="tl-cat-essay" onclick="openEssay({base_idx + k})">
                <span class="tl-cat-essay-num">{e['num']}</span>
                <span class="tl-cat-essay-title">{html.escape(e['title'], quote=False)}</span>
                <span class="tl-cat-essay-live tl-cat-essay-new">New</span>
              </div>"""
    insert_before("\n            </div>\n          </div>", rows, after_pos=pos, label=f"cat {cat} rows")

# Essay table rows (newest first, at the top of the table).
table_rows = ""
for k, e in enumerate(new_essays):
    mins = e["time"].split()[0]
    table_rows += f"""
          <div class="tl-essay-row" data-filter="dilemma cat-{e['cat'].lower()}" onclick="openEssay({base_idx + k})">
            <div class="tl-essay-row-num">{e['num']}</div>
            <div class="tl-essay-row-body">
              <div class="tl-essay-row-title">{html.escape(e['title'], quote=False)}</div>
              <div class="tl-essay-row-meta"><span class="tl-tag tl-tag--green">{CAT_TAG[e['cat']]}</span><span class="tl-tag tl-tag--live">New</span><span class="tl-tag">{mins} min</span></div>
            </div>
            <div class="tl-essay-row-arrow">→</div>
          </div>
"""
rep('<div class="tl-essay-table reveal reveal-delay-2" id="essayTable">\n',
    '<div class="tl-essay-table reveal reveal-delay-2" id="essayTable">\n' + table_rows, label="essay table")

# Counts and copy.
rep("a 65-debrief series", "a 72-debrief series", label="hero copy")
rep('data-target="65">0</span></span><span class="tl-stat-label">Dilemmas planned',
    'data-target="72">0</span></span><span class="tl-stat-label">Dilemmas planned', label="planned")
rep('data-target="54">0</span></span><span class="tl-stat-label">Live now',
    'data-target="66">0</span></span><span class="tl-stat-label">Live now', label="live")
rep('data-target="10">0</span></span><span class="tl-stat-label">Categories',
    'data-target="11">0</span></span><span class="tl-stat-label">Categories', label="cats")
rep("10 categories. 65 debriefs planned. The top three from each category are live — click any to read.",
    "11 categories. 72 debriefs planned, 66 live. Click any title to read.", label="cat desc")
rep('<div class="tl-cat-sub">8 debriefs · Allocation, utilisation, capacity conflicts</div>',
    '<div class="tl-cat-sub">9 debriefs · Allocation, utilisation, capacity conflicts</div>', label="B count")
rep('<div class="tl-cat-sub">4 debriefs · The category nobody else writes</div>',
    '<div class="tl-cat-sub">9 debriefs · The category nobody else writes</div>', label="H count")
rep('<div class="tl-cat-sub">3 debriefs · Only possible from real operational experience</div>',
    '<div class="tl-cat-sub">7 debriefs · Only possible from real operational experience</div>', label="I count")
# Filters: add the two missing categories.
rep('<button class="tl-filter" data-filter="cat-e">E · Agency</button>',
    '<button class="tl-filter" data-filter="cat-e">E · Agency</button>\n          <button class="tl-filter" data-filter="cat-f">F · Decisions</button>',
    label="filter F")

# ─────────────────────────────────────────────────────────── 6. ASK AI FIXES
rep("const WORKER_URL = 'https://sarath-digital-twin.rey619-ms.workers.dev';",
    """// Same-site path proxied by Netlify (see _redirects): avoids networks that block workers.dev.
  const WORKER_URL = location.protocol.startsWith('http')
    ? '/api/twin'
    : 'https://sarath-digital-twin.rey619-ms.workers.dev';""", label="twin url")
rep("""      const res = await fetch(WORKER_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, history: chatHistory.slice(-8) })
      });
      const data = await res.json();""", """      const ctrl = new AbortController();
      const timer = setTimeout(() => ctrl.abort(), 30000);
      const res = await fetch(WORKER_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        // History excludes the message being sent; the Worker adds it.
        body: JSON.stringify({ message: text, history: chatHistory.slice(0, -1).slice(-8) }),
        signal: ctrl.signal
      });
      clearTimeout(timer);
      if (!res.ok) throw new Error('HTTP ' + res.status);
      const data = await res.json();""", label="twin fetch")
rep("""      typing.remove();
      appendMsg(box, 'Connection issue — try again in a moment.', 'ai');""",
    """      typing.remove();
      chatHistory.pop(); // don't keep a question that never got an answer
      appendMsg(box, "I couldn't reach the server just now. Try again in a moment, or email Sarath at rey619.ms@gmail.com.", 'ai');""",
    label="twin error")

# ─────────────────────────────────────────────────────────── 7. CSS
CSS = """
/* ═══════════════════════════════════════════════════
   ADDITIONS: contact, mobile tab bar, toolkit page, essay options, polish
═══════════════════════════════════════════════════ */
.nav-contact {
  background: none; border: 1px solid var(--line-hi); border-radius: 8px; cursor: pointer;
  font-family: var(--mono); font-size: 12px; letter-spacing: 1.5px; text-transform: uppercase;
  color: var(--slate); padding: 8px 12px; margin-right: 12px; transition: border-color .2s, color .2s;
}
.nav-links { margin: 0 auto; }
.nav-contact:hover { border-color: var(--green); color: var(--green); }
.nav-links button:focus-visible, .nav-contact:focus-visible, .mtab button:focus-visible,
.tk-type:focus-visible, .tk-doc:focus-visible, .tk-track:focus-visible { outline: 2px solid var(--green); outline-offset: 2px; }

/* employers: four across, no orphan */
.employers-row { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 32px; }
@media (max-width: 768px) { .employers-row { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 28px 20px; } }

/* testimonials: cards keep their natural height */
.testimonial-track { align-items: flex-start; }

/* footer links */
.footer-links { display: flex; gap: 18px; flex-wrap: wrap; }
.footer-links a { font-family: var(--mono); font-size: 12px; color: var(--slate2); text-decoration: none; }
.footer-links a:hover { color: var(--green); }

/* mobile tab bar */
.mtab { display: none; }
@media (max-width: 768px) {
  .mtab {
    display: flex; position: fixed; left: 0; right: 0; bottom: 0; z-index: 600;
    background: rgba(248,247,244,0.96); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
    border-top: 1px solid var(--line-hi);
    padding: 6px max(8px, env(safe-area-inset-right)) calc(6px + env(safe-area-inset-bottom)) max(8px, env(safe-area-inset-left));
  }
  .mtab button {
    flex: 1; background: none; border: 0; cursor: pointer; padding: 9px 2px; border-radius: 8px;
    font-family: var(--mono); font-size: 10.5px; letter-spacing: .6px; text-transform: uppercase; color: var(--slate2);
  }
  .mtab button.active { color: var(--green); background: var(--green-bg); }
  body { padding-bottom: calc(64px + env(safe-area-inset-bottom)); }
  .twin-trigger { bottom: calc(78px + env(safe-area-inset-bottom)) !important; }
  .nav-contact { padding: 7px 10px; font-size: 11px; margin-right: 8px; }
}

/* essay options + principles */
.reader-body .dd-option { max-width: 680px; border: 1px solid var(--line-hi); border-radius: 10px; padding: 18px 22px; margin: 0 0 14px; background: var(--paper2); }
.reader-body .dd-option-name { font-family: var(--serif); font-size: 18px; font-weight: 600; color: var(--ink); margin-bottom: 8px; }
.reader-body .dd-option dl { display: grid; grid-template-columns: 110px 1fr; gap: 6px 14px; margin: 0; }
.reader-body .dd-option dt { font-family: var(--mono); font-size: 11px; letter-spacing: 1.2px; text-transform: uppercase; color: var(--green); padding-top: 4px; }
.reader-body .dd-option dd { margin: 0; font-size: 16px; line-height: 1.7; color: var(--ink2); }
@media (max-width: 560px) { .reader-body .dd-option dl { grid-template-columns: 1fr; gap: 2px; } .reader-body .dd-option dd { margin-bottom: 8px; } }
.reader-body .dd-principles { max-width: 680px; padding-left: 0; list-style: none; display: grid; gap: 16px; margin-bottom: 26px; }
.reader-body .dd-principles li { font-size: 17px; line-height: 1.85; color: var(--ink2); padding-left: 18px; border-left: 2px solid var(--line-hi); }
.reader-body .dd-principles strong { color: var(--ink); font-weight: 600; }
.tl-cat-essay-new { background: var(--green); color: #fff !important; }

/* toolkit teaser on home */
.tk-teaser { padding: 8px 0 40px; }
.tk-teaser-inner {
  display: flex; align-items: center; gap: 18px; flex-wrap: wrap; text-decoration: none; color: var(--ink);
  border: 1px solid var(--line-hi); border-radius: 12px; padding: 18px 22px; background: linear-gradient(90deg, var(--green-bg2), transparent 70%);
  transition: border-color .2s, transform .2s var(--ease-out-expo);
}
.tk-teaser-inner:hover { border-color: var(--green); transform: translateY(-1px); }
.tk-teaser-tag { font-family: var(--mono); font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase; color: #fff; background: var(--green); padding: 4px 9px; border-radius: 6px; }
.tk-teaser-text { flex: 1 1 320px; font-size: 16px; color: var(--slate); }
.tk-teaser-text b { color: var(--ink); font-family: var(--serif); font-weight: 600; }
.tk-teaser-go { font-family: var(--mono); font-size: 12px; letter-spacing: 1.5px; text-transform: uppercase; color: var(--green); }

/* toolkit page */
.tk-hero { padding: 96px 0 56px; }
.tk-title { font-family: var(--serif); font-size: clamp(36px, 5.2vw, 60px); font-weight: 600; line-height: 1.08; letter-spacing: -1.5px; color: var(--ink); max-width: 15ch; margin: 18px 0 22px; text-wrap: balance; }
.tk-title em { font-style: italic; font-weight: 400; color: var(--green); }
.tk-sub { font-size: 18px; color: var(--slate); max-width: 62ch; line-height: 1.75; }
.tk-cta-row { display: flex; gap: 12px; flex-wrap: wrap; margin-top: 30px; }
.tk-band { background: var(--ink); color: #fff; }
.tk-figures { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); padding-top: 34px; padding-bottom: 34px; }
.tk-figures div { display: grid; gap: 4px; padding: 0 20px; border-left: 1px solid rgba(255,255,255,0.12); }
.tk-figures div:first-child { border-left: 0; padding-left: 0; }
.tk-figures b { font-family: var(--serif); font-size: 34px; font-weight: 600; line-height: 1; font-variant-numeric: tabular-nums; }
.tk-figures span { font-family: var(--mono); font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase; color: rgba(255,255,255,0.55); }
@media (max-width: 640px) {
  .tk-figures { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 22px 0; }
  .tk-figures div:nth-child(3) { border-left: 0; padding-left: 0; }
}
.tk-tracks { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px; margin-top: 56px; }
@media (max-width: 820px) { .tk-tracks { grid-template-columns: 1fr; } }
.tk-track { display: grid; align-content: start; gap: 10px; padding: 28px; border: 1px solid var(--line-hi); border-radius: 14px; background: #fff; text-decoration: none; color: var(--ink); transition: border-color .2s, transform .25s var(--ease-out-expo), box-shadow .25s; }
.tk-track:hover { border-color: var(--green); transform: translateY(-2px); box-shadow: 0 10px 30px rgba(15,31,61,0.07); }
.tk-track-label { font-family: var(--mono); font-size: 11px; letter-spacing: 2px; text-transform: uppercase; color: var(--green); }
.tk-track-title { font-family: var(--serif); font-size: 28px; font-weight: 600; letter-spacing: -0.6px; }
.tk-track-desc { color: var(--slate); font-size: 16px; }
.tk-path { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 6px; }
.tk-path i { font-style: normal; font-family: var(--mono); font-size: 11px; letter-spacing: .5px; padding: 5px 9px; border-radius: 999px; background: var(--paper2); color: var(--slate); }
.tk-path i:not(:last-child)::after { content: " ›"; color: var(--slate2); }
.tk-path i.on { background: var(--green); color: #fff; }
.tk-section { padding-top: 64px; display: grid; gap: 22px; }
.tk-section-head { display: flex; justify-content: space-between; align-items: baseline; gap: 14px; flex-wrap: wrap; }
.tk-section-head h2 { font-family: var(--serif); font-size: clamp(28px, 3.4vw, 38px); font-weight: 600; letter-spacing: -1px; color: var(--ink); }
.tk-section-head a { font-family: var(--mono); font-size: 12px; letter-spacing: 1.5px; text-transform: uppercase; color: var(--green); text-decoration: none; }
.tk-types { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; }
@media (max-width: 900px) { .tk-types { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (max-width: 560px) { .tk-types { grid-template-columns: 1fr; } }
.tk-type { display: grid; gap: 6px; padding: 20px 22px; border: 1px solid var(--line-hi); border-radius: 12px; text-decoration: none; color: var(--ink); background: var(--paper); transition: border-color .2s, background .2s; }
.tk-type:hover { border-color: var(--green); background: #fff; }
.tk-type-cat { font-family: var(--mono); font-size: 11px; letter-spacing: 1.4px; text-transform: uppercase; color: var(--slate2); }
.tk-type-name { font-family: var(--serif); font-size: 20px; font-weight: 600; letter-spacing: -0.3px; }
.tk-type-meta { font-size: 14px; color: var(--slate); }
.tk-docs { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); border-top: 1px solid var(--line-hi); }
@media (max-width: 760px) { .tk-docs { grid-template-columns: 1fr; } }
.tk-doc { display: grid; grid-template-columns: auto 1fr auto; gap: 16px; align-items: start; padding: 20px 4px; border-bottom: 1px solid var(--line-hi); text-decoration: none; color: var(--ink); }
.tk-doc:nth-child(odd) { padding-right: 28px; }
.tk-doc:hover .tk-doc-name { color: var(--green); }
.tk-fmt { font-family: var(--mono); font-size: 11px; font-weight: 500; padding: 3px 7px; border-radius: 5px; border: 1px solid currentColor; margin-top: 3px; }
.tk-fmt--xlsx { color: #217346; } .tk-fmt--docx { color: #2B5797; } .tk-fmt--pptx { color: #B7472A; }
.tk-doc-body { display: grid; gap: 4px; min-width: 0; }
.tk-doc-name { font-family: var(--serif); font-size: 19px; font-weight: 600; transition: color .2s; }
.tk-doc-desc { font-size: 15px; color: var(--slate); line-height: 1.6; }
.tk-doc-arrow { color: var(--slate2); font-size: 14px; margin-top: 4px; }
.tk-why { margin: 72px 0 24px; padding: 32px 0 0; border-top: 1px solid var(--line); display: grid; gap: 14px; }
.tk-why p { font-family: var(--serif); font-size: clamp(19px, 2.2vw, 23px); font-style: italic; line-height: 1.6; color: var(--ink2); max-width: 760px; }
@media (max-width: 768px) { .tk-hero { padding: 72px 0 40px; } .tk-doc:nth-child(odd) { padding-right: 4px; } }
"""
rep("\n</style>\n</head>", CSS + "\n</style>\n</head>", label="css")


# ─────────────────────────────────────────────────────────── 8. CAREER UPDATES (Nov 2026)
rep("""          Open to opportunities
          <span class="snapshot-open-chevron">▾</span>""",
    """          Available immediately · Open to opportunities
          <span class="snapshot-open-chevron">▾</span>""", label="availability")
rep("""          <span class="snapshot-tag">Resource Management</span>
          <span class="snapshot-tag">Delivery Operations</span>
          <span class="snapshot-tag">Project Management</span>
          <span class="snapshot-tag">Bengaluru · Remote</span>""",
    """          <span class="snapshot-tag">Delivery Manager</span>
          <span class="snapshot-tag">Program Manager</span>
          <span class="snapshot-tag">PMO Lead</span>
          <span class="snapshot-tag">Head of Operations</span>
          <span class="snapshot-tag">Resource Management Lead</span>
          <span class="snapshot-tag">Bengaluru · Onsite / Hybrid / Remote</span>
          <span class="snapshot-tag">Relocation · Let's talk</span>""", label="role tags")
rep('<div class="employer-tenure">2+ yrs · Bengaluru</div>',
    '<div class="employer-tenure">2 yrs 6 mos · Bengaluru</div>', label="nb tenure")
rep('<div class="tl-dates">Apr 2024 – Present</div>\n            <div class="tl-tenure">1 yr+</div>',
    '<div class="tl-dates">Apr 2024 – Oct 2026</div>\n            <div class="tl-tenure">2 yrs 6 mos</div>', label="nb dates")
rep("Program Manager for a 50+ person design and UX consultancy — spearheading delivery operations",
    "Program Manager for a 50+ person design and UX consultancy — led delivery operations", label="nb tense 1")
rep("Directly managing CXO, VP, and Director-level client relationships. Mentoring junior PMs",
    "Directly managed CXO, VP, and Director-level client relationships. Mentored junior PMs", label="nb tense 2")

# Compact round chat button on phones (icon only), so it stops covering page content.
rep("""  <span class="twin-trigger-dot"></span>
  <div class="twin-trigger-text">""", """  <span class="twin-trigger-dot"></span>
  <svg class="twin-trigger-icon" viewBox="0 0 24 24" width="24" height="24" aria-hidden="true"><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3h11A2.5 2.5 0 0 1 20 5.5v8a2.5 2.5 0 0 1-2.5 2.5H10l-4.2 3.6c-.5.4-1.3.1-1.3-.6V16.9A2.5 2.5 0 0 1 4 14.6z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M8.5 9.5h7M8.5 12.5h4.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
  <div class="twin-trigger-text">""", label="trigger icon")

# ─────────────────────────────────────────────────────────── 9. ASK AI LANDING
a = s.index('<div class="twin-greeting">')
b = s.index('<div class="twin-input-area">', a)
b = s.rfind("</div>", a, s.rfind("</div>", a, b))  # end of twin-greeting (keep twin-messages close)
def nudges(items, personal=False):
    cls = "twin-nudge twin-nudge--personal" if personal else "twin-nudge"
    return "\n".join(f'          <button class="{cls}" onclick="twinNudge(this)">{t}</button>' for t in items)
LANDING = f"""<div class="twin-greeting">
      <div class="twin-greeting-msg">
        Hey, I'm Sarath's AI. I know his 14 years, his 20+ tools, his writing, and his very strong opinions on Test cricket. <span class="twin-avail">Available immediately</span> Pick a lane below, or just ask.
      </div>

      <div class="twin-nudge-section twin-landing">
        <div class="twin-tabs" role="tablist" aria-label="Topics">
          <button class="twin-tab active" role="tab" aria-selected="true" data-tab="work">Work</button>
          <button class="twin-tab" role="tab" aria-selected="false" data-tab="choices">Choices</button>
          <button class="twin-tab" role="tab" aria-selected="false" data-tab="whatif">What If</button>
          <button class="twin-tab" role="tab" aria-selected="false" data-tab="food">Food for thought</button>
        </div>
        <div class="twin-panel" data-panel="work">
          <p class="twin-panel-hint">The short version, the long version, and whether he's free.</p>
          <div class="twin-nudges">
{nudges(["14 years — give me the short version", "Is he available?", "What roles is he open to?", "What did he do at BCG?", "Has he built a PMO from scratch?", "Why do PMs need to build tools?", "What's the PM Toolkit?", "What do people say about him?"])}
          </div>
        </div>
        <div class="twin-panel" data-panel="choices" hidden>
          <p class="twin-panel-hint">This or that. The AI picks a side and defends it.</p>
          <div class="twin-nudges">
{nudges(["Prime Marshall or prime ABD? 🏏", "Test cricket or T20?", "Lelouch or Light — who runs a better PMO?", "Edward Elric or Sung Jinwoo on a delivery team?", "Idli or dosa?", "Gon or Killua?"], True)}
          </div>
        </div>
        <div class="twin-panel" data-panel="whatif" hidden>
          <p class="twin-panel-hint">Anime meets project management. Pick one or get surprised.</p>
          <div class="twin-nudges">
{nudges(["Surprise me with a What If 🤯", "What if Edward Elric priced a change request?", "What if L audited your RAID log?", "What if Lelouch ran a program?", "What if Levi Ackerman was a delivery manager?", "What if Goku and Vegeta were Hashiras?"], True)}
          </div>
        </div>
        <div class="twin-panel" data-panel="food" hidden>
          <p class="twin-panel-hint">Actual food, and food for thought.</p>
          <div class="twin-nudges">
{nudges(["Best food in Jayanagar & JP Nagar 🍽️", "What anime are you watching right now?", "Why does Sarath watch anime? 🎌"], True)}
{nudges(["Is a green dashboard ever telling the truth?", "Should a delivery manager say no to sales?", "What's the one lesson from 14 years?", "Is 100% utilisation good?"])}
          </div>
        </div>
      </div>
    """
s = s[:a] + LANDING + s[b:]
rep("""  window.twinNudge = function(btn) {""", """  document.querySelectorAll('.twin-tab').forEach(tab => tab.addEventListener('click', () => {
    document.querySelectorAll('.twin-tab').forEach(t => { const on = t === tab; t.classList.toggle('active', on); t.setAttribute('aria-selected', on); });
    document.querySelectorAll('.twin-panel').forEach(p => { p.hidden = p.dataset.panel !== tab.dataset.tab; });
  }));

  window.twinNudge = function(btn) {""", label="tabs js")
rep(".replace(/[🎌🏏⚽☕]/g, '')", ".replace(/[🎌🏏⚽☕🤯🍽️]/gu, '')", label="emoji strip")
TWIN_CSS = """
/* Ask AI landing tabs */
.twin-avail { display: inline-block; margin: 2px 4px 0 0; font-family: var(--mono); font-size: 10.5px; letter-spacing: 1.4px; text-transform: uppercase; color: #6EE7B7; background: rgba(110,231,183,0.1); border: 1px solid rgba(110,231,183,0.25); border-radius: 999px; padding: 2px 9px; }
.twin-tabs { display: flex; gap: 4px; margin-bottom: 10px; overflow-x: auto; scrollbar-width: none; }
.twin-tabs::-webkit-scrollbar { display: none; }
.twin-tab { flex: none; font-family: var(--mono); font-size: 11px; letter-spacing: 1.2px; text-transform: uppercase; color: rgba(255,255,255,0.45); background: none; border: 1px solid transparent; border-radius: 8px; padding: 6px 10px; cursor: pointer; transition: color .2s, background .2s, border-color .2s; }
.twin-tab:hover { color: rgba(255,255,255,0.8); }
.twin-tab.active { color: #fff; background: rgba(255,255,255,0.08); border-color: rgba(255,255,255,0.14); }
.twin-tab:focus-visible, .twin-nudge:focus-visible { outline: 2px solid #7FA2FF; outline-offset: 2px; }
.twin-panel-hint { font-size: 12.5px; color: rgba(255,255,255,0.4); margin: 0 0 8px 2px; font-family: var(--sans); }
.twin-trigger-icon { display: none; color: #fff; }
.twin-landing .twin-nudge { white-space: normal; text-align: left; line-height: 1.35; }
@media (max-width: 480px) { .twin-tab { letter-spacing: .5px; padding: 6px 7px; font-size: 10.5px; } }

/* ═══ Mobile readability and touch targets (phones only) ═══ */
@media (max-width: 768px) {
  .snapshot-label, .snapshot-open-chevron, .essay-read-time, .essay-cta, .essay-arrow, .work-tag,
  .clients-header div, .twin-trigger-hint, .twin-header-status, .twin-avail, .tl-lesson-label, .tag,
  .tl-stat-label, .tl-cat-essay-live, .tl-tag, .case-tag, .case-status, .case-users, .tier2-tag,
  .lab-type, .nav-contact, .snapshot-tag, .work-link, .case-link, .case-col-label, .tk-track-label,
  .tk-type-cat, .tk-fmt, .tk-path i { font-size: 11.5px !important; }
  .twin-tab { font-size: 11px !important; }

  .thinking-see-all, .reader-back, .footer-links a, .tier2-link, .lab-link, .tk-section-head a, .case-link, .work-link {
    display: inline-flex; align-items: center; min-height: 44px;
  }
  .lab-link { min-width: 44px; justify-content: center; }
  .footer-links { gap: 4px 18px; }
  .nav-contact, .nav-cta { min-height: 40px; display: inline-flex; align-items: center; }
  .mtab button { min-height: 46px; font-size: 11px; }
  body { padding-bottom: calc(70px + env(safe-area-inset-bottom)); }
  .twin-trigger { bottom: calc(84px + env(safe-area-inset-bottom)) !important; }
  .twin-close, .twin-home-btn, .t-nav-btn { min-width: 40px; min-height: 40px; display: inline-flex; align-items: center; justify-content: center; }
  .twin-tab { min-height: 36px; }
  .twin-nudge { min-height: 38px; padding-top: 8px; padding-bottom: 8px; }
  .twin-voice, .twin-send, .tl-filter, .reader-share-btn { min-height: 40px; }
  .t-dot { position: relative; }
  .t-dot::after { content: ""; position: absolute; inset: -14px -8px; }
  .reader-body .dd-option { padding: 16px; }
  .twin-trigger { width: 56px; height: 56px; padding: 0 !important; border-radius: 50% !important; justify-content: center; right: max(14px, env(safe-area-inset-right)) !important; }
  .twin-trigger .twin-trigger-text { display: none; }
  .twin-trigger .twin-trigger-icon { display: block; }
  .twin-trigger .twin-trigger-dot { position: absolute; top: 9px; right: 10px; margin: 0; }
  #vcardOverlay button[onclick*="'none'"] { min-width: 44px; min-height: 44px; font-size: 22px !important; top: 6px !important; right: 6px !important; }
  #vcardOverlay div[style*="font-size:10px"], #vcardOverlay div[style*="font-size:10.5px"] { font-size: 11.5px !important; }
}
"""
rep("\n</style>\n</head>", TWIN_CSS + "\n</style>\n</head>", label="twin css")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8").write(s)
print(f"Wrote {OUT}: {len(s):,} chars; {len(new_essays)} essays added at indices {base_idx}-{base_idx + len(new_essays) - 1}")
