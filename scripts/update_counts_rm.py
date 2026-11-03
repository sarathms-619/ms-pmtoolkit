"""One-off: update toolkit counts and copy after adding Resource Management (Nov 2026)."""
import sys

ROOT = "/home/user/pm-toolkit/"


def edit(path, pairs):
    s = open(path, encoding="utf-8").read()
    for old, new in pairs:
        if s.count(old) != 1:
            sys.exit(f"{path}: expected 1 match, found {s.count(old)}: {old[:70]!r}")
        s = s.replace(old, new)
    open(path, "w", encoding="utf-8").write(s)
    print("updated", path)


# ---------- toolkit site
edit(ROOT + "frontend/app.js", [
    ('<div class="eyebrow">Free project templates · Plain English</div>',
     '<div class="eyebrow">Free project & resource management templates · Plain English</div>'),
    ('const starters = ["agile-product-build", "erp-implementation", "fixed-bid", "cloud-migration", "data-migration", "multi-project-program"];',
     'const starters = ["agile-product-build", "erp-implementation", "fixed-bid", "new-account-staffing", "bench-redeployment", "multi-project-program"];'),
])
edit(ROOT + "frontend/index.html", [
    ('content="Every document, tracker and dashboard a project needs, filled with sample data and explained in plain English. Free to download."',
     'content="Every document, tracker and dashboard a project or resource management team needs, filled with sample data and explained in plain English. Free to download."'),
])

# ---------- one-pager
edit(ROOT + "onepager/index.html", [
    ("A free PM toolkit: 25 templates filled with one worked example, mapped to 18 project types, with a 27-metric playb",
     "A free PM toolkit: 30 project and resource management templates filled with worked examples, mapped to 22 project types, with a 33-metric playb"),
    ('content="25 free templates, 18 project types, 27 metrics explained in plain English. Built by Sarath MS."',
     'content="30 free project and resource management templates, 22 project types, 33 metrics explained in plain English. Built by Sarath MS."'),
    ('<div class="hero-eyebrow">A free PM toolkit — explained so anyone can use it</div>',
     '<div class="hero-eyebrow">Project &amp; resource management — explained so anyone can use it</div>'),
    ('<strong>25</strong> templates', '<strong>30</strong> templates'),
    ('<strong>18</strong> project types', '<strong>22</strong> project types'),
    ('<strong>27</strong> metrics explained', '<strong>33</strong> metrics explained'),
    ('<strong>51</strong> terms in plain English', '<strong>62</strong> terms in plain English'),
    ("18 project types across 7 categories: software and digital, enterprise IT, infrastructure and cloud, data and AI, business transformation, programs and PMOs, and client-services work like fixed-bid and retainer engagements.",
     "22 project types across 8 categories: software and digital, enterprise IT, infrastructure and cloud, data and AI, business transformation, programs and PMOs, client-services work like fixed-bid and retainer engagements, and resource management."),
    ('<div class="module-name">25 working templates</div>', '<div class="module-name">30 working templates</div>'),
    ("10 <span class=\"fmt d\">DOCX</span> documents, 14 <span class=\"fmt x\">XLSX</span> trackers and dashboards,",
     "10 <span class=\"fmt d\">DOCX</span> documents, 19 <span class=\"fmt x\">XLSX</span> trackers and dashboards,"),
    ("27 metrics across 9 categories: schedule, cost, scope, quality, agile flow, engineering (DORA), risk and governance, people, and value.",
     "33 metrics across 10 categories: schedule, cost, scope, quality, agile flow, engineering (DORA), risk and governance, people, value, and resource management."),
    ('<a href="https://ms-pmtoolkit.netlify.app/library" target="_blank" rel="noopener">All 25 templates</a>',
     '<a href="https://ms-pmtoolkit.netlify.app/library" target="_blank" rel="noopener">All 30 templates</a>'),
    ("""    <div class="module-row">
      <div class="module-num">04</div>
      <div>
        <div class="module-name">One worked example, everywhere</div>""",
     """    <div class="module-row">
      <div class="module-num">04</div>
      <div>
        <div class="module-name">Resource management</div>
        <div class="module-tagline">The right people, on the right work, at the right time.</div>
        <div class="module-desc">A skills matrix that flags single points of failure, a bench tracker with ageing and cost, a utilisation and billability tracker, a resource request log with time to fill and fill rate, and a 12-week allocation heatmap that shows who is double-booked. Four resource management situations, from staffing a new account to annual hiring plans, and six RM metrics including billability and bench %.</div>
      </div>
    </div>
    <div class="module-row">
      <div class="module-num">05</div>
      <div>
        <div class="module-name">One worked example, everywhere</div>"""),
    ("""      <div class="module-num">05</div>
      <div>
        <div class="module-name">A plain-English layer</div>""",
     """      <div class="module-num">06</div>
      <div>
        <div class="module-name">A plain-English layer</div>"""),
    ("a 51-term glossary sits behind it.", "a 62-term glossary sits behind it."),
    ("One fictional project runs through all 25 files", "One fictional project runs through the project templates, and its delivery partner runs through the resource ones"),
    ("Python builds all 25 Word, Excel and PowerPoint files", "Python builds all 30 Word, Excel and PowerPoint files"),
])

# ---------- carousel + post
edit(ROOT + "onepager/linkedin-carousel.html", [
    ('<div class="stat"><b>25</b><span>Templates</span><small>Word, Excel, PowerPoint. Formulas and charts already working.</small></div>',
     '<div class="stat"><b>30</b><span>Templates</span><small>Project and resource management. Formulas and charts already working.</small></div>'),
    ('<div class="stat"><b>18</b><span>Project types</span>', '<div class="stat"><b>22</b><span>Project types</span>'),
    ('<div class="stat"><b>27</b><span>Metrics</span>', '<div class="stat"><b>33</b><span>Metrics</span>'),
    ("<span>51 terms explained</span>", "<span>62 terms explained</span>"),
])
edit(ROOT + "onepager/linkedin/linkedin-post.txt", [
    ("So I wrote it all down. A free PM toolkit:\n→ 25 templates, already filled in so you can see what good looks like\n→ 18 project types, so you only see what yours needs\n→ 27 metrics, each with what to do when it slips",
     "So I wrote it all down. A free toolkit for project and resource management:\n→ 30 templates, already filled in so you can see what good looks like\n→ 22 project types, so you only see what yours needs\n→ Resource management too: skills matrix, bench tracker, utilisation, allocation heatmap\n→ 33 metrics, each with what to do when it slips"),
])

# ---------- portfolio Toolkit page + teaser
edit(ROOT + "portfolio/source/build.py", [
    ("A free library of 25 project templates, filled with one worked example so every number lines up across documents.",
     "A free library of 30 project and resource management templates, filled with worked examples so every number lines up across documents."),
    ("<div><b>25</b><span>Templates</span></div>", "<div><b>30</b><span>Templates</span></div>"),
    ("<div><b>18</b><span>Project types mapped</span></div>", "<div><b>22</b><span>Project types mapped</span></div>"),
    ("<div><b>27</b><span>Metrics explained</span></div>", "<div><b>33</b><span>Metrics explained</span></div>"),
    ("<div><b>51</b><span>Terms in plain English</span></div>", "<div><b>62</b><span>Terms in plain English</span></div>"),
    ('rel="noopener">All 18 project types ↗</a>', 'rel="noopener">All 22 project types ↗</a>'),
    ('rel="noopener">All 25 templates ↗</a>', 'rel="noopener">All 30 templates ↗</a>'),
    ("<b>The PM Toolkit.</b> 25 templates, mapped to 18 project types, with a metrics playbook.",
     "<b>The PM Toolkit.</b> 30 project and resource management templates, 22 project types and a metrics playbook."),
    ('    ("infrastructure-cloud/cloud-migration", "Infrastructure & Cloud", "Cloud migration", "11 documents · 6-18 months"),',
     '    ("resource-management/bench-redeployment", "Resource Management", "Bench management and redeployment", "5 documents · ongoing"),'),
])

# ---------- Ask AI prompt
edit("/home/user/ask-ai-worker/worker.js", [
    ("   • Built the PM Toolkit — 25 free templates + a metrics playbook",
     "   • Built the PM Toolkit — 30 free project and resource management templates + a metrics playbook"),
    ("   • PM Toolkit: free library of 25 PM templates, mapped to 18 project types, with a 27-metric playbook",
     "   • PM Toolkit: free library of 30 project and resource management templates, mapped to 22 project types, with a 33-metric playbook"),
    ("   • 25 templates: charter, RAID log, EVM tracker, status report, SteerCo deck, dashboards and more",
     "   • 30 templates: charter, RAID log, EVM tracker, status report, SteerCo deck, dashboards and more\n   • Resource management: skills matrix, bench tracker, utilisation & billability tracker, resource request log, allocation heatmap"),
    ("   • Pick a project type (18 of them)", "   • Pick a project type (22 of them, including resource management situations like bench redeployment)"),
    ("   • Metrics playbook: 27 metrics,", "   • Metrics playbook: 33 metrics (including billability, bench %, time to fill),"),
    ("• PM Toolkit: 25 free templates, 18 project types, 27-metric playbook", "• PM Toolkit: 30 free templates (project + resource management), 22 project types, 33-metric playbook"),
])
print("done")
