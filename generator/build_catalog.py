import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from catalog_documents import DOCS, DOC_IDS
from catalog_projects import CATEGORIES
from catalog_metrics import METRIC_CATEGORIES
from glossary import GLOSSARY
import data as D

ROOT = os.path.join(os.path.dirname(__file__), "..")
FILES = os.path.join(ROOT, "frontend", "files")

def build():
    errors = []
    for d in DOCS:
        p = os.path.join(FILES, d["file"])
        if not os.path.exists(p): errors.append(f"missing file {d['file']}")
        else: d["size"] = os.path.getsize(p)
    for c in CATEGORIES:
        for t in c["types"]:
            out = []
            for doc_id, prio, when, note in t["docs"]:
                if doc_id not in DOC_IDS: errors.append(f"{t['id']}: unknown doc {doc_id}")
                out.append({"doc": doc_id, "priority": prio, "when": when, "note": note})
            t["docs"] = out
    for mc in METRIC_CATEGORIES:
        for m in mc["metrics"]:
            if m["template"] not in DOC_IDS: errors.append(f"metric {m['id']}: unknown template {m['template']}")
    if errors:
        sys.exit("Catalogue errors:\n" + "\n".join(errors))
    catalog = {
        "version": 1,
        "sample": {"org": D.ORG, "project": D.PROJECT_FULL, "note": D.SAMPLE_NOTE},
        "documents": DOCS, "projectCategories": CATEGORIES, "metricCategories": METRIC_CATEGORIES,
        "glossary": [{"term": k, "definition": v} for k, v in GLOSSARY.items()],
    }
    return catalog

if __name__ == "__main__":
    cat = build()
    targets = [os.path.join(ROOT, "frontend", "catalog.json"), os.path.join(ROOT, "backend", "src", "catalog.json")]
    for t in targets:
        os.makedirs(os.path.dirname(t), exist_ok=True)
        json.dump(cat, open(t, "w"), ensure_ascii=False, indent=1)
    n_types = sum(len(c["types"]) for c in cat["projectCategories"])
    n_metrics = sum(len(m["metrics"]) for m in cat["metricCategories"])
    print(f"{len(cat['documents'])} documents, {len(cat['projectCategories'])} categories, {n_types} project types, "
          f"{len(cat['metricCategories'])} metric categories, {n_metrics} metrics, {len(cat['glossary'])} glossary terms")
