import os

from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt, Emu

import data as D
from data import name, fmt_date

INK = RGBColor(0x1B, 0x2A, 0x3A); ACCENT = RGBColor(0x0F, 0x5E, 0x6E); MUTED = RGBColor(0x5B, 0x67, 0x73)
ALT = RGBColor(0xF1, 0xF4, 0xF6); WHITE = RGBColor(0xFF, 0xFF, 0xFF); ORANGE = RGBColor(0xD9, 0x82, 0x2B)
RAG = {"Green": RGBColor(0x5F, 0xA3, 0x6B), "Amber": RGBColor(0xE0, 0xA4, 0x3A), "Red": RGBColor(0xC8, 0x55, 0x3D),
       "Complete": RGBColor(0x5F, 0xA3, 0x6B), "On track": RGBColor(0x5F, 0xA3, 0x6B), "At risk": RGBColor(0xE0, 0xA4, 0x3A)}


def text(slide, x, y, w, h, s, size=14, bold=False, color=INK, align=PP_ALIGN.LEFT):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True
    lines = s if isinstance(s, list) else [s]
    for i, line in enumerate(lines):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = align
        r = para.add_run(); r.text = line; r.font.size = Pt(size); r.font.bold = bold; r.font.color.rgb = color; r.font.name = "Calibri"
        para.space_after = Pt(6)
    return tb


def box(slide, x, y, w, h, fill, line=None):
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line: shp.line.color.rgb = line
    else: shp.line.fill.background()
    shp.shadow.inherit = False
    return shp


def frame(prs, title, eyebrow):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    text(s, 0.6, 0.35, 10, 0.3, eyebrow.upper(), 10, True, ACCENT)
    text(s, 0.6, 0.6, 12, 0.7, title, 26, True, INK)
    text(s, 0.6, 7.05, 9, 0.3, D.SAMPLE_NOTE, 8, False, MUTED)
    text(s, 10.2, 7.05, 2.6, 0.3, f"SteerCo #5 · 24 Jun 2026", 8, False, MUTED, PP_ALIGN.RIGHT)
    return s


def table(slide, x, y, w, rows, col_w, font=11, rag_col=None, row_h=0.36):
    t = slide.shapes.add_table(len(rows), len(rows[0]), Inches(x), Inches(y), Inches(w), Inches(row_h * len(rows))).table
    for i, cw in enumerate(col_w): t.columns[i].width = Inches(cw)
    for ri, row in enumerate(rows):
        for ci, v in enumerate(row):
            c = t.cell(ri, ci); c.text = str(v)
            para = c.text_frame.paragraphs[0]; f = para.runs[0].font
            f.size = Pt(font); f.name = "Calibri"; f.color.rgb = WHITE if ri == 0 else INK; f.bold = ri == 0
            c.fill.solid(); c.fill.fore_color.rgb = INK if ri == 0 else (ALT if ri % 2 == 0 else WHITE)
            c.margin_left = c.margin_right = Inches(0.08); c.vertical_anchor = MSO_ANCHOR.MIDDLE
            if ri and rag_col is not None and ci == rag_col and v in RAG:
                c.fill.fore_color.rgb = RAG[v]; f.color.rgb = WHITE; f.bold = True
    return t


def build(out):
    prs = Presentation(); prs.slide_width = Inches(13.333); prs.slide_height = Inches(7.5)
    pv = sum(D.PV[:5]); ev = sum(D.EV[:5]); ac = sum(D.AC[:5])

    # 1 title
    s = prs.slides.add_slide(prs.slide_layouts[6])
    box(s, 0, 0, 13.333, 7.5, INK)
    box(s, 0.6, 2.2, 0.12, 2.0, ACCENT)
    text(s, 0.95, 2.1, 11, 0.4, "STEERING COMMITTEE #5", 12, True, RGBColor(0x9C, 0xC9, 0xCF))
    text(s, 0.95, 2.5, 11, 1.0, D.PROJECT_FULL, 36, True, WHITE)
    text(s, 0.95, 3.6, 11, 0.5, f"{D.ORG} · 24 June 2026 · Presented by {name('pm')}", 16, False, RGBColor(0xC9, 0xD1, 0xD8))
    text(s, 0.95, 6.6, 11, 0.4, D.SAMPLE_NOTE, 10, False, RGBColor(0x9C, 0xA7, 0xB1))

    # 2 exec summary
    s = frame(prs, "Amber: go-live holds, cost needs a decision today", "Executive summary")
    tiles = [("Overall", "Amber"), ("Schedule", "Amber"), ("Cost", "Amber"), ("Scope", "Green"), ("Quality", "Green")]
    for i, (lab, rag_) in enumerate(tiles):
        x = 0.6 + i * 2.45
        box(s, x, 1.5, 2.25, 1.1, RAG[rag_])
        text(s, x + 0.15, 1.58, 2, 0.3, lab.upper(), 11, True, WHITE)
        text(s, x + 0.15, 1.9, 2, 0.5, rag_, 24, True, WHITE)
    text(s, 0.6, 2.95, 7.4, 3.5, [
        "• Build 50% complete; go-live 28 Sep confirmed with 2 weeks buffer (was 4)",
        "• POS integration 2 weeks late: legacy API rate limits. Batch fallback approved for 30 stores",
        f"• CPI {ev/ac:.2f}, SPI {ev/pv:.2f}. Overrun is on POS work, not spread across the project",
        "• Identity match rate up to 91% on dry run 2 (target 97%)",
        "• Contact-centre training plan changed to super-user model"], 15)
    box(s, 8.4, 2.95, 4.3, 3.4, ALT)
    text(s, 8.6, 3.05, 4, 0.4, "DECISION TODAY", 11, True, ACCENT)
    text(s, 8.6, 3.45, 3.95, 2.8, ["Approve CR-007", "+$65k from contingency (vendor absorbs another $65k)",
                                    "SIT complete moves to 14 Aug", "Go-live unchanged"], 14)

    # 3 milestones
    s = frame(prs, "Two build milestones slip; the go-live date holds", "Milestones")
    rows = [["Milestone", "Baseline", "Forecast", "Status"]] + [[m[0], fmt_date(m[1]), fmt_date(m[2]), m[3]] for m in D.MILESTONES]
    table(s, 0.6, 1.5, 12.1, rows, [6.1, 2, 2, 2], 12, rag_col=3)

    # 4 financials chart
    s = frame(prs, f"Earned value ${ev/1000:,.0f}k against ${ac/1000:,.0f}k spent", "Cost and earned value")
    cd = CategoryChartData(); cd.categories = D.MONTHS
    def cum(xs):
        out_, c = [], 0
        for v in xs:
            if v is None: out_.append(None)
            else: c += v; out_.append(c / 1000)
        return out_
    cd.add_series("Planned (PV)", cum(D.PV)); cd.add_series("Earned (EV)", cum(D.EV)); cd.add_series("Actual (AC)", cum(D.AC))
    gf = s.shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS, Inches(0.6), Inches(1.5), Inches(7.6), Inches(5.2), cd)
    ch = gf.chart; ch.has_legend = True; ch.legend.position = XL_LEGEND_POSITION.BOTTOM; ch.legend.include_in_layout = False
    ch.value_axis.tick_labels.number_format = '"$"#,##0"k"'; ch.value_axis.tick_labels.number_format_is_linked = False
    ch.value_axis.major_gridlines.format.line.color.rgb = RGBColor(0xE3, 0xE7, 0xEA)
    for ser, col in zip(ch.series, [MUTED, ACCENT, ORANGE]):
        ser.format.line.color.rgb = col; ser.format.line.width = Pt(2.5); ser.smooth = False
        ser.marker.format.fill.solid(); ser.marker.format.fill.fore_color.rgb = col; ser.marker.format.line.color.rgb = col
    for ax in (ch.value_axis, ch.category_axis): ax.tick_labels.font.size = Pt(11)
    rows = [["Measure", "Value"], ["Budget (BAC)", "$1,850,000"], ["Planned to date", f"${pv:,.0f}"], ["Earned to date", f"${ev:,.0f}"],
            ["Spent to date", f"${ac:,.0f}"], ["CPI / SPI", f"{ev/ac:.2f} / {ev/pv:.2f}"], ["EAC (BAC/CPI)", f"${D.BAC/(ev/ac):,.0f}"],
            ["EAC if CR-007 approved", "$1,915,000"]]
    table(s, 8.5, 1.6, 4.2, rows, [2.4, 1.8], 12)

    # 5 risks
    s = frame(prs, "Top risks: POS integration and cost", "Risks and issues")
    top = sorted([r for r in D.RISKS if r[9] == "Open"], key=lambda r: -r[4] * r[5])[:5]
    rows = [["ID", "Risk", "Score", "Owner", "Mitigation"]] + [[r[0], r[1], str(r[4] * r[5]), name(r[6]), r[8]] for r in top]
    table(s, 0.6, 1.5, 12.1, rows, [0.8, 3.3, 0.8, 1.9, 5.3], 11, row_h=0.6)

    # 6 CR-007
    s = frame(prs, "CR-007: approve +$65k to keep go-live on 28 Sep", "Decision required")
    rows = [["Option", "Cost", "Go-live", "Trade-off"],
            ["1. Approve CR-007 (recommended)", "+$65k", "28 Sep", "UAT 1 week shorter; extra QA engineer added"],
            ["2. BOPIS in 90 stores at launch", "+$20k", "28 Sep", "Lose ~$140k year-1 margin"],
            ["3. Move go-live to 26 Oct", "+$95k", "26 Oct", "Inside peak-trading risk window"]]
    table(s, 0.6, 1.6, 12.1, rows, [3.6, 1.4, 1.4, 5.7], 13, row_h=0.6)
    text(s, 0.6, 4.4, 12, 1.2, ["Funding: sponsor contingency $150k, unused so far. $85k left after approval.",
                                "Brightpath Systems absorbs a further $65k under SOW clause 9.2."], 15)

    # 7 asks
    s = frame(prs, "What we need from this committee", "Asks and next steps")
    text(s, 0.6, 1.5, 6, 4.5, ["Decisions", "1. Approve CR-007", "2. Approve Gate 3 entry criteria", "", "Support",
                               "3. Escalate UAT environment with Cloud Platform team", "4. Release 2 store managers for UAT (Aug)"], 16)
    text(s, 7, 1.5, 5.6, 4.5, ["Next 30 days", "• Sprint 8 and 9 complete; MVP build done 10 Jul", "• SIT starts 29 Jun",
                               "• Agent super-user training wave 1", "• Data migration dry run 3 (target 95%)",
                               "", "Next SteerCo: 22 Jul 2026"], 16)
    prs.save(os.path.join(out, "steering-committee-deck.pptx"))
