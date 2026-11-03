/* PM Toolkit front end. No build step, no framework.
 * Data comes from the Cloudflare API when config.js sets apiBase, otherwise from /catalog.json.
 */
(function () {
  "use strict";

  const CFG = Object.assign({ apiBase: "", siteName: "PM Toolkit", portfolioUrl: "https://sarathms.com" }, window.PMT_CONFIG || {});
  ["back-link", "footer-portfolio"].forEach((id) => { const el = document.getElementById(id); if (el) el.href = CFG.portfolioUrl; });
  const API = CFG.apiBase.replace(/\/$/, "");
  const main = document.getElementById("main");
  const PHASES = [
    ["Initiation", "Get approval and set up"],
    ["Planning", "Plan the work, money and people"],
    ["Execution", "Build, change, test and launch"],
    ["Monitoring", "Report and control (runs throughout)"],
    ["Closure", "Hand over and learn"],
  ];
  const PRIORITY_HELP = {
    Essential: "You will struggle without it",
    Recommended: "Use it unless the project is very small",
    Optional: "Useful in some situations",
  };

  let C = null;            // catalogue
  let STATS = null;        // download counts
  const IDX = { docs: {}, types: {}, cats: {}, metricCats: {}, metrics: {}, usedIn: {}, metricsByDoc: {} };

  // ------------------------------------------------------------------ helpers
  const esc = (s) => String(s == null ? "" : s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const $ = (sel, el = document) => el.querySelector(sel);
  let termRe = null, termMap = {}, seenTerms = new Set();

  function buildTerms() {
    const alts = [];
    for (const g of C.glossary) {
      termMap[g.term.toLowerCase()] = g;
      alts.push(g.term);
      if (/[a-z]/.test(g.term)) alts.push(g.term[0].toLowerCase() + g.term.slice(1));
    }
    alts.sort((a, b) => b.length - a.length);
    termRe = new RegExp("\\b(" + alts.map((a) => a.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).join("|") + ")s?\\b", "g");
  }
  // Escape text and underline the first use of each glossary term on the page.
  function T(text) {
    return esc(text).replace(termRe, (m, term) => {
      const key = term.toLowerCase();
      if (seenTerms.has(key) || !termMap[key]) return m;
      seenTerms.add(key);
      return `<abbr class="term" tabindex="0" data-term="${esc(key)}">${m}</abbr>`;
    });
  }
  const fileUrl = (file) => (API ? `${API}/api/download/${file}` : `/files/${file}`);
  const kb = (n) => (n ? `${Math.max(1, Math.round(n / 1024))} KB` : "");
  const chip = (p) => `<span class="chip ${p.toLowerCase()}" title="${esc(PRIORITY_HELP[p])}">${esc(p)}</span>`;
  const fmt = (f) => `<span class="fmt ${f}">${f}</span>`;
  const list = (items, tag = "ul") => `<${tag}>${items.map((i) => `<li>${T(i)}</li>`).join("")}</${tag}>`;
  const dlIcon = `<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 2v8m0 0L4.5 6.5M8 10l3.5-3.5M2.5 13.5h11" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
  function dlButton(doc, label) {
    const n = STATS && STATS.byFile ? STATS.byFile[doc.file] : null;
    return `<a class="btn primary" href="${fileUrl(doc.file)}" download="${esc(doc.file)}" data-dl="${esc(doc.file)}">${dlIcon}${esc(label || "Download " + doc.format.toUpperCase())}</a>
      <span class="dl-count">${esc(kb(doc.size))}${n ? ` · downloaded ${n.toLocaleString()} times` : ""}</span>`;
  }
  function trail(parts) {
    return `<nav class="trail" aria-label="Breadcrumb">${parts.map((p, i) =>
      (i ? `<span class="sep" aria-hidden="true">/</span>` : "") + (p[1] ? `<a href="${p[1]}" data-link>${esc(p[0])}</a>` : `<span>${esc(p[0])}</span>`)).join("")}</nav>`;
  }

  // ------------------------------------------------------------------ data
  async function load() {
    const tryFetch = async (u) => { const r = await fetch(u); if (!r.ok) throw new Error(r.status); return r.json(); };
    try { C = await tryFetch(API ? `${API}/api/catalog` : "/catalog.json"); }
    catch (e) { C = await tryFetch("/catalog.json"); }
    for (const d of C.documents) { IDX.docs[d.id] = d; IDX.usedIn[d.id] = []; IDX.metricsByDoc[d.id] = []; }
    for (const c of C.projectCategories) {
      IDX.cats[c.id] = c;
      for (const t of c.types) {
        IDX.types[t.id] = Object.assign(t, { cat: c });
        for (const e of t.docs) IDX.usedIn[e.doc].push({ type: t, priority: e.priority });
      }
    }
    for (const mc of C.metricCategories) {
      IDX.metricCats[mc.id] = mc;
      for (const m of mc.metrics) { IDX.metrics[m.id] = Object.assign(m, { cat: mc }); IDX.metricsByDoc[m.template].push(m); }
    }
    buildTerms();
    if (API) {
      fetch(`${API}/api/stats`).then((r) => r.json()).then((s) => {
        STATS = s;
        if (s.total) $("#footer-stats").textContent = `${s.total.toLocaleString()} downloads so far.`;
      }).catch(() => {});
    }
  }

  // ------------------------------------------------------------------ pages
  function home() {
    const nTypes = Object.keys(IDX.types).length, nMetrics = Object.keys(IDX.metrics).length;
    const popular = ["weekly-status-report", "raid-log", "project-charter", "budget-evm-tracker", "project-health-dashboard", "steering-committee-deck"];
    const starters = ["agile-product-build", "erp-implementation", "fixed-bid", "cloud-migration", "data-migration", "multi-project-program"];
    return {
      title: CFG.siteName,
      html: `<div class="wrap">
      <section class="hero">
        <div class="eyebrow">Free project templates · Plain English</div>
        <h1>Every document a project needs, and when to use it</h1>
        <p class="lede">Pick your type of project and see exactly which documents it needs, when to create and update each one, how, and who owns it.
          Or look up a metric to see what it means, what happens when it goes wrong, and how to fix it. Every template is filled with a worked example.</p>
      </section>
      <div class="tracks">
        <a class="track" href="/projects" data-link>
          <div class="eyebrow">Track 1</div>
          <h2>Documents by project</h2>
          <p>Start from the kind of project you're running. Get the right documents for it, with timing, ownership and what to update.</p>
          <div class="path"><span>Category</span><i>›</i><span>Project type</span><i>›</i><span>Documents</span><i>›</i><span>When · How · Who · What</span></div>
          <span class="go">Browse ${nTypes} project types →</span>
        </a>
        <a class="track" href="/metrics" data-link>
          <div class="eyebrow">Track 2</div>
          <h2>Metrics playbook</h2>
          <p>Understand the numbers on a status report. For each metric: what it means, what happens when it's off, and what to do about it.</p>
          <div class="path"><span>Category</span><i>›</i><span>Metric</span><i>›</i><span>Impact</span><i>›</i><span>Resolution</span></div>
          <span class="go">Browse ${nMetrics} metrics →</span>
        </a>
      </div>
      <div class="figures">
        <div><b>${C.documents.length}</b><span>ready-to-use templates</span></div>
        <div><b>${nTypes}</b><span>project types mapped</span></div>
        <div><b>${nMetrics}</b><span>metrics explained</span></div>
        <div><b>${C.glossary.length}</b><span>terms in plain English</span></div>
      </div>
      <section class="section">
        <div class="section-head"><h2>Start with a common project</h2><a href="/projects" data-link>All project types</a></div>
        <div class="type-list">${starters.map((id) => typeLink(IDX.types[id], true)).join("")}</div>
      </section>
      <section class="section">
        <div class="section-head"><h2>Most-used templates</h2><a href="/library" data-link>All ${C.documents.length} templates</a></div>
        <div class="grid">${popular.map((id) => libCard(IDX.docs[id])).join("")}</div>
      </section></div>`,
    };
  }

  function typeLink(t, showCat) {
    const ess = t.docs.filter((d) => d.priority === "Essential").length;
    return `<a class="type-link" href="/projects/${t.cat.id}/${t.id}" data-link>
      ${showCat ? `<em>${esc(t.cat.name)}</em>` : ""}
      <strong>${esc(t.name)}</strong><span>${esc(t.plain)}</span>
      <em>${t.docs.length} documents · ${ess} essential · ${esc(t.duration)}</em></a>`;
  }

  function projectsIndex() {
    return {
      title: "Documents by project",
      html: `<div class="wrap"><header class="page-head">
        ${trail([["Home", "/"], ["Documents by project"]])}
        <div class="eyebrow">Track 1 · Category › Project type › Documents › When · How · Who · What</div>
        <h1>What kind of project are you running?</h1>
        <p class="lede">Choose the closest match. Each project type lists only the documents it really needs, in the order you'll need them.</p>
      </header>
      ${C.projectCategories.map((c) => `<section class="cat-block" id="${c.id}">
        <div class="cat-title"><h2><a href="/projects/${c.id}" data-link style="color:inherit;text-decoration:none">${esc(c.name)}</a></h2><p class="muted">${esc(c.plain)}</p></div>
        <div class="type-list">${c.types.map((t) => typeLink(t)).join("")}</div></section>`).join("")}</div>`,
    };
  }

  function categoryPage(c) {
    return {
      title: c.name,
      html: `<div class="wrap"><header class="page-head">
        ${trail([["Home", "/"], ["Documents by project", "/projects"], [c.name]])}
        <div class="eyebrow">Category</div><h1>${esc(c.name)}</h1><p class="lede">${esc(c.plain)}</p></header>
        <div class="type-list">${c.types.map((t) => typeLink(t)).join("")}</div></div>`,
    };
  }

  function typePage(t) {
    const byPhase = {};
    for (const e of t.docs) { const d = IDX.docs[e.doc]; (byPhase[d.phase] = byPhase[d.phase] || []).push([d, e]); }
    const order = { Essential: 0, Recommended: 1, Optional: 2 };
    let step = 0;
    const groups = PHASES.filter(([p]) => byPhase[p]).map(([p, sub]) => {
      step++;
      const rows = byPhase[p].sort((a, b) => order[a[1].priority] - order[b[1].priority]);
      return `<section class="phase"><div class="phase-label"><span class="step">${step}</span>${esc(p)} <span style="text-transform:none;letter-spacing:0;font-weight:400">· ${esc(sub)}</span></div>
        ${rows.map(([d, e]) => docRow(d, e, t)).join("")}</section>`;
    }).join("");
    return {
      title: t.name,
      html: `<div class="wrap"><header class="page-head">
        ${trail([["Home", "/"], ["Documents by project", "/projects"], [t.cat.name, `/projects/${t.cat.id}`], [t.name]])}
        <div class="eyebrow">Project type</div><h1>${esc(t.name)}</h1>
        <p class="lede">${T(t.plain)}</p>
        <div class="facts"><span><b>Examples</b>${esc(t.examples)}</span><span><b>Approach</b>${esc(t.method)}</span><span><b>Typical length</b>${esc(t.duration)}</span><span><b>Team</b>${esc(t.team)}</span></div>
      </header>
      <div class="reading" style="max-width:none">
        <div class="legend"><span>${t.docs.length} documents, grouped by when you'll need them. Open any one to see <b>when</b>, <b>how</b>, <b>who</b> and <b>what</b> to update.</span></div>
        <div class="legend" style="margin-top:8px">${Object.keys(PRIORITY_HELP).map((p) => `<span>${chip(p)} ${esc(PRIORITY_HELP[p])}</span>`).join("")}</div>
        ${groups}
      </div></div>`,
    };
  }

  function w4(d, e) {
    const when = e && e.when ? e.when : null;
    return `<div class="w4">
      <div class="w"><h4>When <small>to create and update it</small></h4><dl>
        <dt>Create</dt><dd>${T(when || d.when.create)}</dd>
        ${when ? `<dt>Default timing</dt><dd>${T(d.when.create)}</dd>` : ""}
        <dt>Update</dt><dd>${T(d.when.update)}</dd><dt>Rhythm</dt><dd>${T(d.when.cadence)}</dd></dl></div>
      <div class="w"><h4>How <small>to do it well</small></h4>${list(d.how, "ol")}</div>
      <div class="w"><h4>Who <small>is involved</small></h4><dl>
        <dt>Owns it</dt><dd>${T(d.who.owner)}</dd><dt>Writes it</dt><dd>${T(d.who.author)}</dd>
        <dt>Contributes</dt><dd>${T(d.who.contributors)}</dd><dt>Approves</dt><dd>${T(d.who.approver)}</dd></dl></div>
      <div class="w"><h4>What <small>to update each time</small></h4>${list(d.what)}</div>
    </div>`;
  }
  function plainBox(d) {
    return `<div class="plain">
      <div><b>What it is</b><p>${T(d.plain)}</p></div>
      <div><b>Think of it as</b><p>${T(d.like)}</p></div>
      <div><b>Without it</b><p>${T(d.without)}</p></div></div>`;
  }

  function docRow(d, e, t) {
    seenTerms = new Set(); // underline terms again inside each card
    return `<details class="doc" id="${d.id}">
      <summary>
        <div class="doc-title"><h3>${esc(d.title)}</h3>${fmt(d.format)}${chip(e.priority)}<span class="kind">${esc(d.kind)}</span></div>
        <span class="chev" aria-hidden="true">▾</span>
        <p class="doc-plain">${T(d.plain)}</p>
        <p class="doc-when-short"><b>When:</b> ${esc(e.when || d.when.create)}</p>
      </summary>
      <div class="doc-body">
        ${plainBox(d)}
        ${e.note ? `<p class="note"><b>For ${esc(t.name.toLowerCase())}:</b> ${T(e.note)}</p>` : ""}
        ${w4(d, e)}
        <p class="mistake"><b>Common mistake:</b> ${T(d.mistake)}</p>
        <div class="actions">${dlButton(d)}<a class="btn ghost" href="/documents/${d.id}" data-link>Full guide</a></div>
      </div></details>`;
  }

  function docPage(d) {
    const used = IDX.usedIn[d.id];
    const mets = IDX.metricsByDoc[d.id];
    return {
      title: d.title,
      html: `<div class="wrap"><header class="page-head">
        ${trail([["Home", "/"], ["All templates", "/library"], [d.title]])}
        <div class="eyebrow">${esc(d.phase)} · ${esc(d.kind)}</div>
        <h1>${esc(d.title)}</h1><p class="lede">${T(d.summary)}</p>
        <div class="actions">${dlButton(d)}</div>
      </header>
      <div style="display:grid;gap:22px">
        ${plainBox(d)}
        <div class="card"><h3>What's inside the template</h3>${list(d.inside)}
          <p class="muted" style="font-size:.9rem">Filled in with the worked example: ${esc(C.sample.project)} at ${esc(C.sample.org)}. ${esc(C.sample.note)}</p></div>
        ${w4(d)}
        <p class="mistake"><b>Common mistake:</b> ${T(d.mistake)}</p>
        ${mets.length ? `<div class="card"><h3>Metrics tracked here</h3><div class="used-in">${mets.map((m) => `<a href="/metrics/${m.cat.id}/${m.id}" data-link>${esc(m.name)}</a>`).join("")}</div></div>` : ""}
        <div class="card"><h3>Used in ${used.length} project types</h3><div class="used-in">${used.map((u) =>
          `<a href="/projects/${u.type.cat.id}/${u.type.id}#${d.id}" data-link>${esc(u.type.name)} · ${esc(u.priority)}</a>`).join("")}</div></div>
      </div></div>`,
    };
  }

  function metricsIndex() {
    return {
      title: "Metrics playbook",
      html: `<div class="wrap"><header class="page-head">
        ${trail([["Home", "/"], ["Metrics playbook"]])}
        <div class="eyebrow">Track 2 · Category › Metric › Impact › Resolution</div>
        <h1>What is this number telling me?</h1>
        <p class="lede">Each metric explains what it measures in plain words, what happens when it's off target, and the steps to fix it.</p>
      </header>
      ${C.metricCategories.map((mc) => `<section class="cat-block" id="${mc.id}">
        <div class="cat-title"><h2>${esc(mc.name)}</h2><p class="muted">${esc(mc.plain)}</p></div>
        <div class="metric-list">${mc.metrics.map((m) => `<a class="metric-link" href="/metrics/${mc.id}/${m.id}" data-link>
          <strong>${esc(m.name)}</strong><code class="formula">${esc(m.formula)}</code><span>${T(m.plain)}</span></a>`).join("")}</div></section>`).join("")}</div>`,
    };
  }

  function metricPage(m) {
    const tpl = IDX.docs[m.template];
    const th = m.thresholds;
    return {
      title: m.name,
      html: `<div class="wrap"><header class="page-head">
        ${trail([["Home", "/"], ["Metrics playbook", "/metrics"], [m.cat.name, `/metrics#${m.cat.id}`], [m.name]])}
        <div class="eyebrow">${esc(m.cat.name)} · ${esc(m.cat.plain)}</div>
        <h1>${esc(m.name)}</h1><p class="lede">${T(m.plain)}</p>
      </header>
      <div class="flow">
        <section class="measure"><h3><span class="n">1</span>The metric</h3>
          <code class="formula">${esc(m.formula)}</code>
          <p class="example"><b>Example:</b> ${T(m.example)}</p>
          <div class="thresholds"><div class="g"><b>Green</b>${esc(th.green)}</div><div class="a"><b>Amber</b>${esc(th.amber)}</div><div class="r"><b>Red</b>${esc(th.red)}</div></div>
          <p class="muted" style="font-size:.9rem">Check it: ${esc(m.frequency)}</p></section>
        <section class="impact"><h3><span class="n">2</span>Impact when it's off</h3>
          <p class="lead">${T(m.impact.summary)}</p>${list(m.impact.effects)}</section>
        <section class="resolve"><h3><span class="n">3</span>Resolution</h3>
          <p><b>First, find the cause:</b></p>${list(m.resolution.diagnose)}
          <p><b>Then act:</b></p>${list(m.resolution.actions, "ol")}
          <p class="escalate"><b>Escalate when:</b> ${T(m.resolution.escalate)}</p></section>
      </div>
      <section class="section"><h2>Track it in</h2>
        <div class="card" style="max-width:720px"><div class="doc-title"><h3>${esc(tpl.title)}</h3>${fmt(tpl.format)}</div>
          <p>${T(tpl.plain)}</p><div class="actions">${dlButton(tpl)}<a class="btn ghost" href="/documents/${tpl.id}" data-link>Full guide</a></div></div>
      </section>
      <section class="section"><h2>Other ${esc(m.cat.name.toLowerCase())} metrics</h2>
        <div class="used-in">${m.cat.metrics.filter((x) => x.id !== m.id).map((x) => `<a href="/metrics/${m.cat.id}/${x.id}" data-link>${esc(x.name)}</a>`).join("")}</div></section>
      </div>`,
    };
  }

  function libCard(d) {
    return `<div class="card lib-card">
      <div class="top">${fmt(d.format)}<span class="kind">${esc(d.phase)} · ${esc(d.kind)}</span></div>
      <h3><a href="/documents/${d.id}" data-link style="color:inherit">${esc(d.title)}</a></h3>
      <p>${esc(d.plain)}</p>
      <div class="actions">${dlButton(d, "Download")}</div></div>`;
  }

  function library() {
    const phases = PHASES.map((p) => p[0]);
    const kinds = [...new Set(C.documents.map((d) => d.kind))];
    return {
      title: "All templates",
      html: `<div class="wrap"><header class="page-head">
        ${trail([["Home", "/"], ["All templates"]])}
        <div class="eyebrow">Library</div><h1>All ${C.documents.length} templates</h1>
        <p class="lede">Word documents, Excel trackers and dashboards (with working formulas and charts) and a PowerPoint deck. All filled with one consistent example project.</p>
      </header>
      <div class="filters" role="search">
        <input id="q" type="search" placeholder="Search, e.g. risk, budget, status" aria-label="Search templates">
        <select id="f-phase" aria-label="Stage"><option value="">Every stage</option>${phases.map((p) => `<option>${p}</option>`).join("")}</select>
        <select id="f-kind" aria-label="Type"><option value="">Every type</option>${kinds.map((k) => `<option>${k}</option>`).join("")}</select>
        <select id="f-format" aria-label="Format"><option value="">Every format</option><option value="docx">Word</option><option value="xlsx">Excel</option><option value="pptx">PowerPoint</option></select>
      </div>
      <div id="lib" class="grid" style="margin-top:18px"></div></div>`,
      after() {
        const q = $("#q"), fp = $("#f-phase"), fk = $("#f-kind"), ff = $("#f-format"), out = $("#lib");
        const draw = () => {
          const s = q.value.trim().toLowerCase();
          const rows = C.documents.filter((d) => (!fp.value || d.phase === fp.value) && (!fk.value || d.kind === fk.value) && (!ff.value || d.format === ff.value) &&
            (!s || [d.title, d.summary, d.plain, d.kind].join(" ").toLowerCase().includes(s)));
          out.innerHTML = rows.length ? rows.map(libCard).join("") : `<p class="empty">No templates match. Clear a filter or try another word.</p>`;
        };
        [q, fp, fk, ff].forEach((el) => el.addEventListener("input", draw));
        draw();
      },
    };
  }

  function glossary() {
    const items = [...C.glossary].sort((a, b) => a.term.localeCompare(b.term));
    return {
      title: "Glossary",
      html: `<div class="wrap"><header class="page-head">
        ${trail([["Home", "/"], ["Glossary"]])}
        <div class="eyebrow">Plain English</div><h1>Project jargon, explained</h1>
        <p class="lede">Dotted underlines across the site link to these definitions. Hover or tap a term to read it.</p></header>
        <dl class="glossary">${items.map((g) => `<div id="${esc(g.term.toLowerCase().replace(/\W+/g, "-"))}"><dt>${esc(g.term)}</dt><dd>${esc(g.definition)}</dd></div>`).join("")}</dl></div>`,
    };
  }

  function notFound() {
    return { title: "Not found", html: `<div class="wrap"><header class="page-head"><h1>That page doesn't exist</h1>
      <p class="lede">The link may be old. Try <a href="/projects" data-link>documents by project</a> or the <a href="/metrics" data-link>metrics playbook</a>.</p></header></div>` };
  }

  // ------------------------------------------------------------------ router
  const routes = [
    [/^\/$/, () => home()],
    [/^\/projects\/?$/, () => projectsIndex()],
    [/^\/projects\/([\w-]+)\/?$/, (c) => IDX.cats[c] && categoryPage(IDX.cats[c])],
    [/^\/projects\/([\w-]+)\/([\w-]+)\/?$/, (c, t) => IDX.types[t] && IDX.types[t].cat.id === c && typePage(IDX.types[t])],
    [/^\/documents\/([\w-]+)\/?$/, (d) => IDX.docs[d] && docPage(IDX.docs[d])],
    [/^\/metrics\/?$/, () => metricsIndex()],
    [/^\/metrics\/([\w-]+)\/([\w-]+)\/?$/, (c, m) => IDX.metrics[m] && IDX.metrics[m].cat.id === c && metricPage(IDX.metrics[m])],
    [/^\/library\/?$/, () => library()],
    [/^\/glossary\/?$/, () => glossary()],
  ];

  function render() {
    const path = location.pathname;
    seenTerms = new Set();
    let page = null;
    for (const [re, fn] of routes) { const m = path.match(re); if (m) { page = fn(...m.slice(1)); break; } }
    page = page || notFound();
    main.innerHTML = page.html;
    document.title = page.title === CFG.siteName ? `${CFG.siteName} · Sarath MS` : `${page.title} · ${CFG.siteName}`;
    const section = path.split("/")[1] || "";
    const navKey = section === "documents" ? "library" : section;
    document.querySelectorAll("[data-nav]").forEach((a) => (a.dataset.nav === navKey ? a.setAttribute("aria-current", "page") : a.removeAttribute("aria-current")));
    if (page.after) page.after();
    if (location.hash) {
      const el = document.getElementById(decodeURIComponent(location.hash.slice(1)));
      if (el) { if (el.tagName === "DETAILS") el.open = true; el.scrollIntoView({ block: "start" }); return; }
    }
    window.scrollTo(0, 0);
  }

  document.addEventListener("click", (ev) => {
    const a = ev.target.closest("a");
    if (!a || a.hasAttribute("download") || a.target || ev.metaKey || ev.ctrlKey || ev.shiftKey || ev.button !== 0) return;
    const url = new URL(a.href, location.href);
    if (url.origin !== location.origin) return;
    if (url.pathname === location.pathname && url.hash) return; // same-page anchor
    ev.preventDefault();
    history.pushState(null, "", url.pathname + url.hash);
    render();
    main.focus({ preventScroll: true });
  });
  window.addEventListener("popstate", render);

  // ------------------------------------------------------------------ glossary popovers
  const pop = document.getElementById("term-pop");
  function showTerm(el) {
    const g = termMap[el.dataset.term];
    if (!g) return;
    pop.innerHTML = `<b>${esc(g.term)}</b>${esc(g.definition)}`;
    pop.hidden = false;
    const r = el.getBoundingClientRect(), pw = pop.offsetWidth, ph = pop.offsetHeight;
    let left = Math.min(Math.max(16, r.left + r.width / 2 - pw / 2), window.innerWidth - pw - 16);
    let top = r.bottom + 8;
    if (top + ph > window.innerHeight - 8) top = r.top - ph - 8;
    pop.style.left = left + "px"; pop.style.top = top + "px";
  }
  const hideTerm = () => { pop.hidden = true; };
  document.addEventListener("mouseover", (e) => { const t = e.target.closest("abbr.term"); if (t) showTerm(t); });
  document.addEventListener("mouseout", (e) => { if (e.target.closest("abbr.term")) hideTerm(); });
  document.addEventListener("focusin", (e) => { const t = e.target.closest("abbr.term"); t ? showTerm(t) : hideTerm(); });
  document.addEventListener("click", (e) => {
    const t = e.target.closest("abbr.term");
    if (t) { e.preventDefault(); e.stopPropagation(); pop.hidden ? showTerm(t) : hideTerm(); }
    else hideTerm();
  }, true);
  window.addEventListener("scroll", hideTerm, { passive: true });

  load().then(render).catch((err) => {
    console.error(err);
    main.innerHTML = `<div class="wrap"><header class="page-head"><h1>The toolkit didn't load</h1><p class="lede">Check your connection and refresh the page.</p></header></div>`;
  });
})();
