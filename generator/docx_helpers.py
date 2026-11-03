from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor, Cm

import data as D

INK = RGBColor(0x1B, 0x2A, 0x3A)
ACCENT = RGBColor(0x0F, 0x5E, 0x6E)
MUTED = RGBColor(0x5B, 0x67, 0x73)
HEAD_FILL = "1B2A3A"
ALT_FILL = "F1F4F6"
GUIDE_FILL = "E8F2F3"
RAG_FILL = {"Green": "CDEBD3", "Amber": "FBE3B5", "Red": "F6C6C2",
            "Complete": "CDEBD3", "On track": "CDEBD3", "At risk": "FBE3B5",
            "Late": "F6C6C2", "Approved": "CDEBD3", "Rejected": "F6C6C2",
            "Pending SteerCo": "FBE3B5", "Open": "FBE3B5", "In progress": "FBE3B5",
            "Resolved": "CDEBD3", "Closed": "CDEBD3", "Pass": "CDEBD3", "Fail": "F6C6C2",
            "Met": "CDEBD3", "Partially met": "FBE3B5", "Not met": "F6C6C2", "Yes": "CDEBD3", "No": "F6C6C2"}


def shade(cell, hex_fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_fill)
    tcPr.append(shd)


def set_cell_margins(table, top=60, bottom=60, left=90, right=90):
    tblPr = table._tbl.tblPr
    mar = OxmlElement("w:tblCellMar")
    for k, v in (("top", top), ("bottom", bottom), ("left", left), ("right", right)):
        el = OxmlElement(f"w:{k}")
        el.set(qn("w:w"), str(v))
        el.set(qn("w:type"), "dxa")
        mar.append(el)
    tblPr.append(mar)


def new_doc(title, doc_type, version="1.0", status="Approved", landscape=False):
    doc = Document()
    sec = doc.sections[0]
    if landscape:
        sec.orientation = WD_ORIENT.LANDSCAPE
        sec.page_width, sec.page_height = sec.page_height, sec.page_width
    for side in ("left_margin", "right_margin"):
        setattr(sec, side, Cm(2))
    sec.top_margin = Cm(1.8)
    sec.bottom_margin = Cm(1.8)

    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    st.font.color.rgb = INK
    st.paragraph_format.space_after = Pt(4)
    for lvl, size in ((1, 15), (2, 12.5), (3, 11)):
        hs = doc.styles[f"Heading {lvl}"]
        hs.font.name = "Calibri"
        hs.font.size = Pt(size)
        hs.font.bold = True
        hs.font.color.rgb = ACCENT if lvl == 1 else INK
        hs.paragraph_format.space_before = Pt(14 if lvl == 1 else 10)
        hs.paragraph_format.space_after = Pt(4)
        rpr = hs.element.get_or_add_rPr()
        rfonts = rpr.find(qn("w:rFonts"))
        if rfonts is None:
            rfonts = OxmlElement("w:rFonts"); rpr.append(rfonts)
        for a in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
            rfonts.set(qn(a), "Calibri")

    # header / footer
    hp = sec.header.paragraphs[0]
    hr = hp.add_run(f"{D.ORG}  |  {D.PROJECT}  |  {doc_type}")
    hr.font.size = Pt(8); hr.font.color.rgb = MUTED
    fp = sec.footer.paragraphs[0]
    fr = fp.add_run(f"{D.SAMPLE_NOTE}   Template from {D.BRAND}.")
    fr.font.size = Pt(7.5); fr.font.color.rgb = MUTED

    eyebrow = doc.add_paragraph()
    r = eyebrow.add_run(doc_type.upper()); r.font.size = Pt(9); r.bold = True; r.font.color.rgb = ACCENT
    eyebrow.paragraph_format.space_after = Pt(0)
    t = doc.add_paragraph()
    r = t.add_run(title); r.font.size = Pt(22); r.bold = True; r.font.color.rgb = INK
    t.paragraph_format.space_after = Pt(2)
    s = doc.add_paragraph()
    r = s.add_run(f"{D.PROJECT_FULL}  ·  {D.PROJECT_ID}"); r.font.size = Pt(10.5); r.font.color.rgb = MUTED
    return doc


def doc_control(doc, version, date_, author_key, approver_key, status):
    kv_table(doc, [
        ("Version", version), ("Date", D.fmt_date(date_)), ("Status", status),
        ("Author", f"{D.name(author_key)}, {D.role(author_key)}"),
        ("Approver", f"{D.name(approver_key)}, {D.role(approver_key)}"),
    ], widths=(3.5, 13))


def h(doc, text, lvl=1):
    return doc.add_heading(text, level=lvl)


def p(doc, text, bold=False, italic=False, size=None, color=None):
    para = doc.add_paragraph()
    run = para.add_run(text)
    run.bold = bold; run.italic = italic
    if size: run.font.size = Pt(size)
    if color: run.font.color.rgb = color
    return para


def bullets(doc, items, style="List Bullet"):
    for it in items:
        para = doc.add_paragraph(style=style)
        if isinstance(it, tuple):
            r = para.add_run(it[0] + ": "); r.bold = True
            para.add_run(it[1])
        else:
            para.add_run(it)
        para.paragraph_format.space_after = Pt(2)


def guidance(doc, text):
    """Shaded tip box telling the PM how to use the section."""
    t = doc.add_table(rows=1, cols=1)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = t.rows[0].cells[0]
    shade(c, GUIDE_FILL)
    para = c.paragraphs[0]
    r = para.add_run("How to use: "); r.bold = True; r.font.size = Pt(9); r.font.color.rgb = ACCENT
    r = para.add_run(text); r.italic = True; r.font.size = Pt(9); r.font.color.rgb = INK
    set_cell_margins(t, 80, 80, 140, 140)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)


def table(doc, headers, rows, widths=None, rag_cols=(), font=9, align_right=()):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, hd in enumerate(headers):
        c = t.rows[0].cells[i]
        shade(c, HEAD_FILL)
        c.paragraphs[0].text = ""
        r = c.paragraphs[0].add_run(hd); r.bold = True; r.font.size = Pt(font); r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    for ri, row in enumerate(rows):
        cells = t.add_row().cells
        for i, val in enumerate(row):
            val = "" if val is None else str(val)
            cells[i].paragraphs[0].text = ""
            r = cells[i].paragraphs[0].add_run(val); r.font.size = Pt(font)
            if i in align_right:
                cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
            if i in rag_cols and val in RAG_FILL:
                shade(cells[i], RAG_FILL[val]); r.bold = True
            elif ri % 2 == 1:
                shade(cells[i], ALT_FILL)
    # repeat header row
    trPr = t.rows[0]._tr.get_or_add_trPr()
    th = OxmlElement("w:tblHeader"); th.set(qn("w:val"), "true"); trPr.append(th)
    if widths:
        for row in t.rows:
            for i, w in enumerate(widths):
                row.cells[i].width = Cm(w)
    set_cell_margins(t)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)
    return t


def kv_table(doc, pairs, widths=(4.5, 12)):
    t = doc.add_table(rows=0, cols=2)
    t.style = "Table Grid"
    for k, v in pairs:
        cells = t.add_row().cells
        shade(cells[0], ALT_FILL)
        r = cells[0].paragraphs[0].add_run(k); r.bold = True; r.font.size = Pt(9.5)
        r = cells[1].paragraphs[0].add_run(str(v)); r.font.size = Pt(9.5)
        if str(v) in RAG_FILL:
            shade(cells[1], RAG_FILL[str(v)]); r.bold = True
    for row in t.rows:
        row.cells[0].width = Cm(widths[0]); row.cells[1].width = Cm(widths[1])
    set_cell_margins(t)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)
    return t


def signature_block(doc, keys):
    rows = [(D.name(k), D.role(k), "", "") for k in keys]
    table(doc, ["Name", "Role", "Signature", "Date"], rows, widths=(4, 6, 4, 2.5), font=9.5)
