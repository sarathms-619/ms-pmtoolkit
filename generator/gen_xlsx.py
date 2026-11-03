import os
from datetime import timedelta

import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell as rc, xl_col_to_name as colname

import data as D
from data import name, money

INK = "#0F1F3D"; ACCENT = "#1C4ED8"; MUTED = "#5B6773"; ALT = "#F1F4F6"; GUIDE = "#E9EEFB"
GREEN = "#CDEBD3"; AMBER = "#FBE3B5"; RED = "#F6C6C2"
SERIES = ["#0F5E6E", "#D9822B", "#5B6773", "#8FA9EE", "#B5523B"]


class Book:
    def __init__(self, path):
        self.wb = xlsxwriter.Workbook(path)
        wb = self.wb
        base = {"font_name": "Calibri", "font_size": 10, "valign": "top", "text_wrap": True}
        self.f = {
            "title": wb.add_format({"font_name": "Calibri", "font_size": 18, "bold": True, "font_color": INK}),
            "sub": wb.add_format({"font_name": "Calibri", "font_size": 10, "font_color": MUTED}),
            "eyebrow": wb.add_format({"font_name": "Calibri", "font_size": 9, "bold": True, "font_color": ACCENT}),
            "head": wb.add_format({**base, "bold": True, "font_color": "white", "bg_color": INK, "border": 1, "border_color": "#C9D1D8", "valign": "vcenter"}),
            "cell": wb.add_format({**base, "border": 1, "border_color": "#D5DCE2"}),
            "date": wb.add_format({**base, "border": 1, "border_color": "#D5DCE2", "num_format": "dd-mmm-yy"}),
            "money": wb.add_format({**base, "border": 1, "border_color": "#D5DCE2", "num_format": "$#,##0"}),
            "num": wb.add_format({**base, "border": 1, "border_color": "#D5DCE2", "num_format": "0"}),
            "dec": wb.add_format({**base, "border": 1, "border_color": "#D5DCE2", "num_format": "0.00"}),
            "dec1": wb.add_format({**base, "border": 1, "border_color": "#D5DCE2", "num_format": "0.0"}),
            "pct": wb.add_format({**base, "border": 1, "border_color": "#D5DCE2", "num_format": "0%"}),
            "bold": wb.add_format({**base, "bold": True, "border": 1, "border_color": "#D5DCE2", "bg_color": ALT}),
            "bmoney": wb.add_format({**base, "bold": True, "border": 1, "border_color": "#D5DCE2", "bg_color": ALT, "num_format": "$#,##0"}),
            "guide": wb.add_format({"font_name": "Calibri", "font_size": 9, "italic": True, "font_color": INK, "bg_color": GUIDE, "text_wrap": True, "valign": "top"}),
            "note": wb.add_format({"font_name": "Calibri", "font_size": 8, "italic": True, "font_color": MUTED}),
            "kpi_label": wb.add_format({"font_name": "Calibri", "font_size": 9, "bold": True, "font_color": MUTED, "bg_color": ALT, "align": "center", "valign": "vcenter", "border": 1, "border_color": "#D5DCE2"}),
            "kpi_val": wb.add_format({"font_name": "Calibri", "font_size": 20, "bold": True, "font_color": INK, "bg_color": ALT, "align": "center", "valign": "vcenter", "border": 1, "border_color": "#D5DCE2"}),
            "kpi_val_money": wb.add_format({"font_name": "Calibri", "font_size": 20, "bold": True, "font_color": INK, "bg_color": ALT, "align": "center", "valign": "vcenter", "num_format": "$#,##0,\"k\"", "border": 1, "border_color": "#D5DCE2"}),
            "kpi_val_dec": wb.add_format({"font_name": "Calibri", "font_size": 20, "bold": True, "font_color": INK, "bg_color": ALT, "align": "center", "valign": "vcenter", "num_format": "0.00", "border": 1, "border_color": "#D5DCE2"}),
            "kpi_val_pct": wb.add_format({"font_name": "Calibri", "font_size": 20, "bold": True, "font_color": INK, "bg_color": ALT, "align": "center", "valign": "vcenter", "num_format": "0%", "border": 1, "border_color": "#D5DCE2"}),
            "green": wb.add_format({"bg_color": GREEN, "bold": True}),
            "amber": wb.add_format({"bg_color": AMBER, "bold": True}),
            "red": wb.add_format({"bg_color": RED, "bold": True}),
        }

    def sheet(self, name_, title, subtitle, guide=None, widths=None, landscape=True):
        ws = self.wb.add_worksheet(name_)
        ws.hide_gridlines(2)
        if landscape: ws.set_landscape()
        ws.fit_to_pages(1, 0)
        ws.write(0, 0, f"{D.PROJECT.upper()}  ·  {D.ORG.upper()}", self.f["eyebrow"])
        ws.write(1, 0, title, self.f["title"])
        ws.write(2, 0, subtitle, self.f["sub"])
        ws.set_row(1, 26)
        if widths:
            for i, w in enumerate(widths):
                ws.set_column(i, i, w)
        row = 4
        if guide:
            last = max(len(widths or [1]) - 1, 6)
            ws.merge_range(row, 0, row, last, "How to use: " + guide, self.f["guide"])
            ws.set_row(row, 32)
            row = 6
        ws.set_footer(f"&L&8{D.SAMPLE_NOTE}&R&8{D.BRAND}")
        return ws, row

    def header(self, ws, row, headers):
        for i, h in enumerate(headers):
            ws.write(row, i, h, self.f["head"])
        ws.set_row(row, 30)
        return row + 1

    def rag(self, ws, rng, words=None):
        words = words or {"Green": "green", "On track": "green", "Complete": "green", "Closed": "green", "Resolved": "green",
                          "Approved": "green", "Validated": "green", "Amber": "amber", "At risk": "amber", "Open": "amber",
                          "In progress": "amber", "Pending SteerCo": "amber", "Red": "red", "Late": "red", "Rejected": "red"}
        for w, fmt in words.items():
            ws.conditional_format(rng, {"type": "cell", "criteria": "==", "value": f'"{w}"', "format": self.f[fmt]})

    def lists(self, ws, rng, values):
        ws.data_validation(rng, {"validate": "list", "source": values})

    def close(self):
        self.wb.close()


# ---------------------------------------------------------------- stakeholder register
def stakeholder_register(out):
    b = Book(os.path.join(out, "stakeholder-register.xlsx"))
    ws, r = b.sheet("Register", "Stakeholder Register", "Who is affected, how much they matter, and how we engage them",
                    "Interest and Influence are scored 1-5. Quadrant is calculated. Review monthly and after any re-organisation. "
                    "Engagement gap = where Current is short of Desired: plan actions for those rows first.",
                    [24, 26, 18, 9, 9, 18, 14, 30, 13, 13, 22])
    r = b.header(ws, r, ["Name", "Role", "Department", "Interest (1-5)", "Influence (1-5)", "Quadrant", "Attitude",
                         "Key needs / concerns", "Current engagement", "Desired engagement", "Communication"])
    first = r
    for s in D.STAKEHOLDERS:
        k = s[0]
        nm, rl = (name(k), D.role(k)) if k else (s[1], "Group")
        ws.write(r, 0, nm, b.f["cell"]); ws.write(r, 1, rl, b.f["cell"]); ws.write(r, 2, s[1], b.f["cell"])
        ws.write(r, 3, s[2], b.f["num"]); ws.write(r, 4, s[3], b.f["num"])
        ws.write_formula(r, 5, f'=IF(AND(D{r+1}>=3,E{r+1}>=3),"Manage closely",IF(E{r+1}>=3,"Keep satisfied",IF(D{r+1}>=3,"Keep informed","Monitor")))', b.f["cell"])
        for c, v in zip(range(6, 11), s[4:9]):
            ws.write(r, c, v, b.f["cell"])
        r += 1
    b.lists(ws, f"D{first+1}:E{r+20}", ["1", "2", "3", "4", "5"])
    b.lists(ws, f"G{first+1}:G{r+20}", ["Champion", "Supporter", "Neutral", "Concerned", "Resistant", "Unaware"])
    b.lists(ws, f"I{first+1}:J{r+20}", ["Unaware", "Resistant", "Neutral", "Supportive", "Leading"])
    ws.conditional_format(f"F{first+1}:F{r}", {"type": "text", "criteria": "containing", "value": "Manage closely", "format": b.f["red"]})
    ws.conditional_format(f"F{first+1}:F{r}", {"type": "text", "criteria": "containing", "value": "Keep satisfied", "format": b.f["amber"]})
    ws.conditional_format(f"F{first+1}:F{r}", {"type": "text", "criteria": "containing", "value": "Keep informed", "format": b.f["green"]})
    ws.freeze_panes(first, 1)
    ws.autofilter(first - 1, 0, r - 1, 10)

    # Power-interest grid as scatter
    ch = b.wb.add_chart({"type": "scatter"})
    ch.add_series({"name": "Stakeholders", "categories": ["Register", first, 3, r - 1, 3], "values": ["Register", first, 4, r - 1, 4],
                   "marker": {"type": "circle", "size": 9, "fill": {"color": ACCENT}, "border": {"color": "white"}},
                   "data_labels": {"custom": [{"value": (name(s[0]) if s[0] else s[1]).split(" (")[0]} for s in D.STAKEHOLDERS],
                                   "position": "right", "font": {"size": 8}}})
    ch.set_x_axis({"name": "Interest", "min": 0, "max": 5.5, "major_unit": 2.75, "major_gridlines": {"visible": True, "line": {"color": "#AAB4BD"}}})
    ch.set_y_axis({"name": "Influence", "min": 0, "max": 5.5, "major_unit": 2.75, "major_gridlines": {"visible": True, "line": {"color": "#AAB4BD"}}})
    ch.set_title({"name": "Influence / interest grid", "name_font": {"size": 11}})
    ch.set_legend({"none": True}); ch.set_size({"width": 760, "height": 460})
    ws.insert_chart(r + 2, 0, ch)
    b.close()


# ---------------------------------------------------------------- RACI
def raci(out):
    b = Book(os.path.join(out, "raci-matrix.xlsx"))
    ws, r = b.sheet("RACI", "RACI Matrix", "Who is Responsible, Accountable, Consulted and Informed for each activity",
                    "Exactly one A per row. The check column flags rows with zero or several A's. "
                    "Use A/R when the same person is accountable and does the work.",
                    [40] + [11] * len(D.RACI_ROLES) + [14])
    r = b.header(ws, r, ["Activity / deliverable"] + D.RACI_ROLES + ["Check"])
    first = r
    for row in D.RACI:
        ws.write(r, 0, row[0], b.f["cell"])
        for i, v in enumerate(row[1:], start=1):
            ws.write(r, i, v, b.f["cell"])
        last = colname(len(D.RACI_ROLES))
        ws.write_formula(r, len(D.RACI_ROLES) + 1, f'=IF(COUNTIF(B{r+1}:{last}{r+1},"A*")=1,"OK","Fix: need one A")', b.f["cell"])
        r += 1
    rng = f"B{first+1}:{colname(len(D.RACI_ROLES))}{r}"
    for v, fmt in (("A", "red"), ("A/R", "red"), ("R", "amber"), ("C", "green")):
        ws.conditional_format(rng, {"type": "cell", "criteria": "==", "value": f'"{v}"', "format": b.f[fmt]})
    ws.conditional_format(f"{colname(len(D.RACI_ROLES)+1)}{first+1}:{colname(len(D.RACI_ROLES)+1)}{r}",
                          {"type": "text", "criteria": "begins with", "value": "Fix", "format": b.f["red"]})
    b.lists(ws, f"{rng.split(':')[0]}:{colname(len(D.RACI_ROLES))}{r+20}", ["R", "A", "A/R", "C", "I"])
    ws.freeze_panes(first, 1)
    ws.write(r + 1, 0, "R = Responsible (does the work)  ·  A = Accountable (one per row, signs off)  ·  C = Consulted (two-way)  ·  I = Informed (one-way)", b.f["note"])
    b.close()


# ---------------------------------------------------------------- RAID
def raid_log(out):
    b = Book(os.path.join(out, "raid-log.xlsx"))
    # Summary
    ws, r = b.sheet("Summary", "RAID Summary", "Counts update automatically from the other tabs", None, [30, 14, 14])
    ws.write(4, 0, "Status date", b.f["bold"]); ws.write_datetime(4, 1, _dt(D.STATUS_DATE), b.f["date"])
    rows = [("Open risks", '=COUNTIF(Risks!K:K,"Open")'), ("Open risks scored 15+", '=COUNTIFS(Risks!K:K,"Open",Risks!G:G,">=15")'),
            ("Open issues", '=COUNTIFS(Issues!H:H,"<>Resolved",Issues!A:A,"I-*")'), ("High-priority issues", '=COUNTIFS(Issues!D:D,"High",Issues!H:H,"<>Resolved")'),
            ("Open assumptions", '=COUNTIF(Assumptions!D:D,"Open")'), ("Late dependencies", '=COUNTIF(Dependencies!G:G,"Late")'),
            ("Decisions logged", '=COUNTIF(Decisions!A:A,"DEC-*")')]
    for i, (k, f) in enumerate(rows):
        ws.write(6 + i, 0, k, b.f["cell"]); ws.write_formula(6 + i, 1, f, b.f["num"])
    # Risks
    ws, r = b.sheet("Risks", "RAID Log: Risks", "Uncertain events that would affect objectives if they happen",
                    "Score = Probability x Impact (1-5 each). 15+ escalate to Program Manager; 20+ to SteerCo. "
                    "Review every open risk weekly; close risks that can no longer happen.",
                    [7, 30, 40, 12, 8, 8, 8, 18, 11, 44, 10, 9])
    r = b.header(ws, r, ["ID", "Risk", "Cause and effect", "Category", "Prob.", "Impact", "Score", "Owner", "Response", "Mitigation / actions", "Status", "Trend"])
    first = r
    for x in D.RISKS:
        vals = [x[0], x[1], x[2], x[3], x[4], x[5], None, name(x[6]), x[7], x[8], x[9], x[10]]
        for c, v in enumerate(vals):
            if c == 6:
                ws.write_formula(r, 6, f"=E{r+1}*F{r+1}", b.f["num"])
            else:
                ws.write(r, c, v, b.f["num"] if c in (4, 5) else b.f["cell"])
        r += 1
    ws.conditional_format(f"G{first+1}:G{r+30}", {"type": "cell", "criteria": ">=", "value": 15, "format": b.f["red"]})
    ws.conditional_format(f"G{first+1}:G{r+30}", {"type": "cell", "criteria": "between", "minimum": 8, "maximum": 14, "format": b.f["amber"]})
    ws.conditional_format(f"G{first+1}:G{r+30}", {"type": "cell", "criteria": "between", "minimum": 1, "maximum": 7, "format": b.f["green"]})
    b.rag(ws, f"K{first+1}:K{r+30}")
    b.lists(ws, f"E{first+1}:F{r+30}", ["1", "2", "3", "4", "5"])
    b.lists(ws, f"I{first+1}:I{r+30}", ["Avoid", "Mitigate", "Transfer", "Accept", "Monitor", "Exploit"])
    b.lists(ws, f"K{first+1}:K{r+30}", ["Open", "Closed"])
    b.lists(ws, f"L{first+1}:L{r+30}", ["Rising", "Stable", "Falling"])
    ws.freeze_panes(first, 2); ws.autofilter(first - 1, 0, r - 1, 11)

    # heat map
    hr = r + 2
    ws.write(hr, 1, "Heat map: count of OPEN risks by probability (rows) and impact (columns)", b.f["eyebrow"])
    ws.write(hr + 1, 1, "Probability \\ Impact", b.f["head"])
    for i in range(1, 6):
        ws.write(hr + 1, 1 + i, i, b.f["head"])
    for pi, prob in enumerate(range(5, 0, -1)):
        ws.write(hr + 2 + pi, 1, prob, b.f["head"])
        for ii in range(1, 6):
            ws.write_formula(hr + 2 + pi, 1 + ii,
                             f'=COUNTIFS($E${first+1}:$E${r},{prob},$F${first+1}:$F${r},{ii},$K${first+1}:$K${r},"Open")', b.f["num"])
            score = prob * ii
            fmt = b.f["red"] if score >= 15 else b.f["amber"] if score >= 8 else b.f["green"]
            ws.conditional_format(hr + 2 + pi, 1 + ii, hr + 2 + pi, 1 + ii, {"type": "no_errors", "format": fmt})

    # Issues
    ws, r = b.sheet("Issues", "RAID Log: Issues", "Problems happening now that need action",
                    "An issue is a risk that has happened. Give each one a priority, an owner and a due date. "
                    "Days open is calculated against the status date in cell B5 of the Summary sheet.",
                    [7, 34, 36, 10, 18, 11, 11, 13, 40, 9])
    r = b.header(ws, r, ["ID", "Issue", "Impact", "Priority", "Owner", "Raised", "Due", "Status", "Resolution / next step", "Days open"])
    first = r
    for x in D.ISSUES:
        vals = [x[0], x[1], x[2], x[3], name(x[4]), x[5], x[6], x[7], x[8]]
        for c, v in enumerate(vals):
            ws.write(r, c, v, b.f["date"] if c in (5, 6) else b.f["cell"])
        ws.write_formula(r, 9, f'=IF(H{r+1}="Resolved","",Summary!$B$5-F{r+1})', b.f["num"])
        r += 1
    b.rag(ws, f"H{first+1}:H{r+30}")
    ws.conditional_format(f"D{first+1}:D{r+30}", {"type": "cell", "criteria": "==", "value": '"High"', "format": b.f["red"]})
    ws.conditional_format(f"D{first+1}:D{r+30}", {"type": "cell", "criteria": "==", "value": '"Medium"', "format": b.f["amber"]})
    b.lists(ws, f"D{first+1}:D{r+30}", ["High", "Medium", "Low"])
    b.lists(ws, f"H{first+1}:H{r+30}", ["Open", "In progress", "Resolved"])
    ws.freeze_panes(first, 2)

    # Assumptions
    ws, r = b.sheet("Assumptions", "RAID Log: Assumptions", "Things we believe true but have not proven",
                    "Validate each assumption by a date. If it turns out false, raise a risk or issue.", [7, 60, 22, 14])
    r = b.header(ws, r, ["ID", "Assumption", "Owner", "Status"])
    first = r
    for x in D.ASSUMPTIONS:
        for c, v in enumerate([x[0], x[1], name(x[2]), x[3]]):
            ws.write(r, c, v, b.f["cell"])
        r += 1
    b.rag(ws, f"D{first+1}:D{r+30}")

    # Dependencies
    ws, r = b.sheet("Dependencies", "RAID Log: Dependencies", "Work this project needs from others, or others need from us",
                    "Inbound = we need it. Outbound = someone needs it from us. Agree the date with the other owner and review in the program sync.",
                    [7, 48, 11, 26, 18, 12, 12])
    r = b.header(ws, r, ["ID", "Dependency", "Direction", "Other party", "Owner", "Needed by", "Status"])
    first = r
    for x in D.DEPENDENCIES:
        for c, v in enumerate([x[0], x[1], x[2], x[3], name(x[4]), x[5], x[6]]):
            ws.write(r, c, v, b.f["date"] if c == 5 else b.f["cell"])
        r += 1
    b.rag(ws, f"G{first+1}:G{r+30}")

    # Decisions
    ws, r = b.sheet("Decisions", "RAID Log: Decisions", "Decisions made, by whom and why",
                    "Log a decision the day it is made. It stops the same debate happening twice.", [9, 44, 44, 20, 12, 36])
    r = b.header(ws, r, ["ID", "Decision", "Rationale", "Made by", "Date", "Impact"])
    for x in D.DECISIONS:
        for c, v in enumerate(x):
            ws.write(r, c, v, b.f["date"] if c == 4 else b.f["cell"])
        r += 1

    b.close()


def _dt(x):
    from datetime import datetime
    return datetime(x.year, x.month, x.day)


# ---------------------------------------------------------------- schedule / gantt
def schedule(out):
    b = Book(os.path.join(out, "project-schedule-gantt.xlsx"))
    weeks = []
    w = D.START
    while w <= D.END:
        weeks.append(w); w += timedelta(days=7)
    ws, r = b.sheet("Schedule", "Integrated Project Schedule", "Baseline v2.1 · weekly Gantt · status date 19 Jun 2026",
                    "Edit Start, Finish and % complete; bars redraw automatically. Dark bar = done, light = remaining, "
                    "red column = status date. Phase rows are summaries.",
                    [6, 42, 16, 11, 11, 7, 8, 8] + [3.2] * len(weeks), landscape=True)
    ws.write(4, 8 + len(weeks) - 6, "Status date", b.f["note"])
    ws.write_datetime(4, 8 + len(weeks) - 3, _dt(D.STATUS_DATE), b.wb.add_format({"num_format": "dd-mmm", "font_size": 8, "bold": True}))
    status_cell = rc(4, 8 + len(weeks) - 3, True, True)
    hdr = ["WBS", "Task", "Owner", "Start", "Finish", "Days", "% done", "Pred."]
    for i, hd in enumerate(hdr):
        ws.write(r, i, hd, b.f["head"])
    wk = b.wb.add_format({"font_size": 7, "rotation": 90, "num_format": "dd-mmm", "align": "center", "bg_color": INK, "font_color": "white", "border": 1, "border_color": "#C9D1D8"})
    for i, x in enumerate(weeks):
        ws.write_datetime(r, 8 + i, _dt(x), wk)
    ws.set_row(r, 40)
    hrow = r; r += 1; first = r
    phase_fmt = b.wb.add_format({"bold": True, "bg_color": ALT, "border": 1, "border_color": "#D5DCE2", "font_size": 10})
    phase_date = b.wb.add_format({"bold": True, "bg_color": ALT, "border": 1, "border_color": "#D5DCE2", "font_size": 10, "num_format": "dd-mmm-yy"})
    phase_rows = []
    for x in D.WBS:
        if x[2] is None:
            phase_rows.append(r)
            ws.write(r, 0, x[0], phase_fmt); ws.write(r, 1, x[1], phase_fmt); ws.write(r, 2, "", phase_fmt)
            for c in range(3, 8): ws.write(r, c, "", phase_fmt)
        else:
            ws.write(r, 0, x[0], b.f["cell"]); ws.write(r, 1, "    " + x[1], b.f["cell"]); ws.write(r, 2, name(x[2]), b.f["cell"])
            ws.write_datetime(r, 3, _dt(x[3]), b.f["date"]); ws.write_datetime(r, 4, _dt(x[4]), b.f["date"])
            ws.write_formula(r, 5, f"=NETWORKDAYS(D{r+1},E{r+1})", b.f["num"])
            ws.write_number(r, 6, x[5] / 100, b.f["pct"]); ws.write(r, 7, x[6], b.f["cell"])
        r += 1
    # phase summaries
    phase_rows.append(r)
    for a, nxt in zip(phase_rows, phase_rows[1:]):
        ws.write_formula(a, 3, f"=MIN(D{a+2}:D{nxt})", phase_date)
        ws.write_formula(a, 4, f"=MAX(E{a+2}:E{nxt})", phase_date)
        ws.write_formula(a, 5, f"=NETWORKDAYS(D{a+1},E{a+1})", phase_fmt)
        ws.write_formula(a, 6, f"=SUMPRODUCT(F{a+2}:F{nxt},G{a+2}:G{nxt})/SUM(F{a+2}:F{nxt})",
                         b.wb.add_format({"bold": True, "bg_color": ALT, "num_format": "0%", "border": 1, "border_color": "#D5DCE2"}))
    last = r
    grid = f"I{first+1}:{colname(8+len(weeks)-1)}{last}"
    tl = f"I${hrow+1}"
    done = b.wb.add_format({"bg_color": ACCENT}); todo = b.wb.add_format({"bg_color": "#A9BEF2"})
    today = b.wb.add_format({"left": 2, "left_color": "#C0392B"})
    ws.conditional_format(grid, {"type": "formula", "criteria": f"=AND({tl}+6>=$D{first+1},{tl}<=$E{first+1},{tl}<=$D{first+1}+($E{first+1}-$D{first+1})*$G{first+1})", "format": done})
    ws.conditional_format(grid, {"type": "formula", "criteria": f"=AND({tl}+6>=$D{first+1},{tl}<=$E{first+1})", "format": todo})
    ws.conditional_format(f"I{hrow+1}:{colname(8+len(weeks)-1)}{last}", {"type": "formula", "criteria": f"=AND({status_cell}>={tl},{status_cell}<{tl}+7)", "format": today})
    ws.freeze_panes(first, 2)

    # milestones
    ws2, r2 = b.sheet("Milestones", "Milestone Tracker", "Baseline vs forecast; variance in working days",
                      "Update Forecast every week. Variance > 10 working days goes to SteerCo.", [40, 13, 13, 11, 13])
    r2 = b.header(ws2, r2, ["Milestone", "Baseline", "Forecast / actual", "Variance (days)", "Status"])
    f2 = r2
    for m in D.MILESTONES:
        ws2.write(r2, 0, m[0], b.f["cell"]); ws2.write_datetime(r2, 1, _dt(m[1]), b.f["date"]); ws2.write_datetime(r2, 2, _dt(m[2]), b.f["date"])
        ws2.write_formula(r2, 3, f"=IF(C{r2+1}>B{r2+1},NETWORKDAYS(B{r2+1},C{r2+1})-1,-(NETWORKDAYS(C{r2+1},B{r2+1})-1))", b.f["num"])
        ws2.write(r2, 4, m[3], b.f["cell"]); r2 += 1
    b.rag(ws2, f"E{f2+1}:E{r2}")
    ws2.conditional_format(f"D{f2+1}:D{r2}", {"type": "cell", "criteria": ">", "value": 10, "format": b.f["red"]})
    ws2.conditional_format(f"D{f2+1}:D{r2}", {"type": "cell", "criteria": "between", "minimum": 1, "maximum": 10, "format": b.f["amber"]})
    b.close()


# ---------------------------------------------------------------- budget & EVM
def budget_evm(out):
    b = Book(os.path.join(out, "budget-evm-tracker.xlsx"))
    ws, r = b.sheet("EVM", "Budget and Earned Value Tracker", "Monthly, cumulative, all figures in USD",
                    "Enter monthly Planned Value (PV), Earned Value (EV = % complete x budget) and Actual Cost (AC). "
                    "CPI and SPI below 0.95 for two months triggers a re-forecast. EAC uses BAC / CPI.",
                    [22] + [12] * 9 + [14])
    r = b.header(ws, r, ["Measure"] + D.MONTHS + ["Total / latest"])
    first = r
    labels = ["PV (monthly)", "EV (monthly)", "AC (monthly)", "PV (cumulative)", "EV (cumulative)", "AC (cumulative)",
              "Schedule variance (EV-PV)", "Cost variance (EV-AC)", "SPI (EV/PV)", "CPI (EV/AC)"]
    for i, lab in enumerate(labels):
        ws.write(first + i, 0, lab, b.f["bold"])
    for m in range(9):
        col = 1 + m; L = colname(col)
        for i, series in enumerate([D.PV, D.EV, D.AC]):
            v = series[m]
            if v is None: ws.write_blank(first + i, col, None, b.f["money"])
            else: ws.write_number(first + i, col, v, b.f["money"])
        for i in range(3):
            src = first + i + 1
            ws.write_formula(first + 3 + i, col, f'=IF({L}{src}="",NA(),SUM($B{src}:{L}{src}))', b.f["money"])
        c = {k: f"{L}{first+1+k}" for k in range(10)}
        ws.write_formula(first + 6, col, f'=IFERROR({c[4]}-{c[3]},"")', b.f["money"])
        ws.write_formula(first + 7, col, f'=IFERROR({c[4]}-{c[5]},"")', b.f["money"])
        ws.write_formula(first + 8, col, f'=IFERROR({c[4]}/{c[3]},"")', b.f["dec"])
        ws.write_formula(first + 9, col, f'=IFERROR({c[4]}/{c[5]},"")', b.f["dec"])
    ws.conditional_format(first + 3, 1, first + 9, 9, {"type": "errors", "format": b.wb.add_format({"font_color": "#FFFFFF"})})
    tot = 10
    for i in range(3):
        ws.write_formula(first + i, tot, f"=SUM(B{first+i+1}:J{first+i+1})", b.f["bmoney"])
    for i in range(6, 10):
        fmt = b.f["dec"] if i >= 8 else b.f["money"]
        ws.write_formula(first + i, tot, f"=LOOKUP(2,1/ISNUMBER(B{first+i+1}:J{first+i+1}),B{first+i+1}:J{first+i+1})", fmt)
    for row_ in (first + 8, first + 9):
        rng = f"B{row_+1}:K{row_+1}"
        ws.conditional_format(rng, {"type": "cell", "criteria": ">=", "value": 0.95, "format": b.f["green"]})
        ws.conditional_format(rng, {"type": "cell", "criteria": "between", "minimum": 0.85, "maximum": 0.9499, "format": b.f["amber"]})
        ws.conditional_format(rng, {"type": "cell", "criteria": "<", "value": 0.85, "format": b.f["red"]})
    # forecasts
    fr = first + 12
    ws.write(fr - 1, 0, "Forecast at completion", b.f["eyebrow"])
    kv = [("BAC (budget at completion)", D.BAC, "money"),
          ("CPI (latest)", f"=K{first+10}", "dec"), ("SPI (latest)", f"=K{first+9}", "dec"),
          ("EAC = BAC / CPI", f"=B{fr+1}/B{fr+2}", "money"),
          ("EAC = AC + (BAC - EV) (if overrun is one-off)", f"=K{first+3}+(B{fr+1}-K{first+2})", "money"),
          ("VAC (BAC - EAC)", f"=B{fr+1}-B{fr+4}", "money"),
          ("TCPI to hit BAC = (BAC-EV)/(BAC-AC)", f"=(B{fr+1}-K{first+2})/(B{fr+1}-K{first+3})", "dec"),
          ("% complete (EV / BAC)", f"=K{first+2}/B{fr+1}", "pct"), ("% spent (AC / BAC)", f"=K{first+3}/B{fr+1}", "pct")]
    for i, (k, v, f) in enumerate(kv):
        ws.write(fr + i, 0, k, b.f["bold"])
        (ws.write_formula if isinstance(v, str) else ws.write_number)(fr + i, 1, v, b.f[f])
    ws.set_column(0, 0, 40)
    # S-curve
    ch = b.wb.add_chart({"type": "line"})
    for i, (lab, color, dash) in enumerate([("PV (cumulative)", SERIES[2], "dash"), ("EV (cumulative)", SERIES[0], "solid"), ("AC (cumulative)", SERIES[1], "solid")]):
        ch.add_series({"name": lab, "categories": ["EVM", first - 1, 1, first - 1, 9], "values": ["EVM", first + 3 + i, 1, first + 3 + i, 9],
                       "line": {"color": color, "width": 2.25, "dash_type": dash}, "marker": {"type": "circle", "size": 5, "fill": {"color": color}, "border": {"color": color}}})
    ch.set_title({"name": "S-curve: planned vs earned vs actual", "name_font": {"size": 11}})
    ch.set_y_axis({"num_format": "$#,##0,\"k\"", "major_gridlines": {"visible": True, "line": {"color": "#E3E7EA"}}})
    ch.set_legend({"position": "bottom"}); ch.set_size({"width": 760, "height": 340}); ch.show_na_as_empty_cell()
    ws.insert_chart(fr + len(kv) + 1, 0, ch)

    # budget by category
    ws2, r2 = b.sheet("Budget", "Budget by Cost Category", "Budget, actuals to date and forecast at completion",
                      "Update actuals monthly from the finance ledger. Forecast is your best estimate of final cost, not budget minus spend.",
                      [44, 14, 14, 14, 14, 14, 10])
    r2 = b.header(ws2, r2, ["Category", "Budget", "Actual to date", "Remaining", "Forecast at completion", "Variance (Budget - FAC)", "% spent"])
    f2 = r2
    for x in D.BUDGET_LINES:
        ws2.write(r2, 0, x[0], b.f["cell"]); ws2.write(r2, 1, x[1], b.f["money"]); ws2.write(r2, 2, x[2], b.f["money"])
        ws2.write_formula(r2, 3, f"=B{r2+1}-C{r2+1}", b.f["money"]); ws2.write(r2, 4, x[3], b.f["money"])
        ws2.write_formula(r2, 5, f"=B{r2+1}-E{r2+1}", b.f["money"]); ws2.write_formula(r2, 6, f"=C{r2+1}/B{r2+1}", b.f["pct"])
        r2 += 1
    ws2.write(r2, 0, "Total", b.f["bold"])
    for c in range(1, 6):
        L = colname(c); ws2.write_formula(r2, c, f"=SUM({L}{f2+1}:{L}{r2})", b.f["bmoney"])
    ws2.write_formula(r2, 6, f"=C{r2+1}/B{r2+1}", b.f["pct"])
    ws2.conditional_format(f"F{f2+1}:F{r2+1}", {"type": "cell", "criteria": "<", "value": 0, "format": b.f["red"]})
    ch2 = b.wb.add_chart({"type": "bar"})
    ch2.add_series({"name": "Budget", "categories": ["Budget", f2, 0, r2 - 1, 0], "values": ["Budget", f2, 1, r2 - 1, 1], "fill": {"color": "#AAB4BD"}})
    ch2.add_series({"name": "Forecast at completion", "categories": ["Budget", f2, 0, r2 - 1, 0], "values": ["Budget", f2, 4, r2 - 1, 4], "fill": {"color": ACCENT}})
    ch2.set_title({"name": "Budget vs forecast by category", "name_font": {"size": 11}})
    ch2.set_x_axis({"num_format": "$#,##0,\"k\""}); ch2.set_y_axis({"reverse": True})
    ch2.set_legend({"position": "bottom"}); ch2.set_size({"width": 760, "height": 380})
    ws2.insert_chart(r2 + 3, 0, ch2)
    b.close()


# ---------------------------------------------------------------- resource plan
def resource_plan(out):
    b = Book(os.path.join(out, "resource-capacity-plan.xlsx"))
    ws, r = b.sheet("Demand", "Resource and Capacity Plan", "FTE demand by role and month, with cost and over-allocation flags",
                    "Enter planned FTE per month. Capacity tab holds what is available. Cells turn red where demand exceeds capacity. "
                    "Cost uses 20 working days per month.",
                    [28, 22, 10] + [7] * 9 + [10, 14])
    r = b.header(ws, r, ["Role", "Name / supplier", "Day rate"] + D.MONTHS + ["FTE-months", "Cost"])
    first = r
    for x in D.RESOURCES:
        ws.write(r, 0, x[0], b.f["cell"]); ws.write(r, 1, x[1], b.f["cell"]); ws.write(r, 2, x[2], b.f["money"])
        for m, v in enumerate(x[3]):
            ws.write_number(r, 3 + m, v, b.f["dec1"])
        ws.write_formula(r, 12, f"=SUM(D{r+1}:L{r+1})", b.f["dec1"])
        ws.write_formula(r, 13, f"=M{r+1}*C{r+1}*20", b.f["money"])
        r += 1
    ws.write(r, 0, "Total demand", b.f["bold"]); ws.write(r, 1, "", b.f["bold"]); ws.write(r, 2, "", b.f["bold"])
    for c in range(3, 14):
        L = colname(c); ws.write_formula(r, c, f"=SUM({L}{first+1}:{L}{r})", b.f["bmoney"] if c == 13 else b.wb.add_format({"bold": True, "bg_color": ALT, "num_format": "0.0", "border": 1, "border_color": "#D5DCE2"}))
    tot_row = r
    ws.write(r + 1, 0, "Total capacity", b.f["bold"])
    for c in range(3, 12):
        L = colname(c); ws.write_formula(r + 1, c, f"=SUM(Capacity!{L}{first+1}:{L}{tot_row})", b.f["dec1"])
    ws.conditional_format(f"D{first+1}:L{tot_row}", {"type": "formula", "criteria": f"=D{first+1}>Capacity!D{first+1}", "format": b.f["red"]})
    ws.freeze_panes(first, 2)
    ch = b.wb.add_chart({"type": "column", "subtype": "stacked"})
    for i in range(len(D.RESOURCES)):
        ch.add_series({"name": ["Demand", first + i, 0], "categories": ["Demand", first - 1, 3, first - 1, 11],
                       "values": ["Demand", first + i, 3, first + i, 11], "gap": 60})
    line = b.wb.add_chart({"type": "line"})
    line.add_series({"name": "Capacity", "categories": ["Demand", first - 1, 3, first - 1, 11], "values": ["Demand", tot_row + 1, 3, tot_row + 1, 11],
                     "line": {"color": "#C0392B", "width": 2.25, "dash_type": "dash"}})
    ch.combine(line)
    ch.set_title({"name": "FTE demand by role vs capacity", "name_font": {"size": 11}})
    ch.set_legend({"position": "right", "font": {"size": 8}}); ch.set_size({"width": 860, "height": 400})
    ws.insert_chart(tot_row + 4, 0, ch)

    ws2, r2 = b.sheet("Capacity", "Available Capacity", "FTE available per role per month (after leave and other commitments)",
                      "Get capacity from line managers and the vendor. Same row order as the Demand tab.", [28, 22, 10] + [7] * 9)
    r2 = b.header(ws2, r2, ["Role", "Name / supplier", ""] + D.MONTHS)
    for x, cap in zip(D.RESOURCES, D.CAPACITY):
        ws2.write(r2, 0, x[0], b.f["cell"]); ws2.write(r2, 1, x[1], b.f["cell"]); ws2.write(r2, 2, "", b.f["cell"])
        for m, v in enumerate(cap): ws2.write_number(r2, 3 + m, v, b.f["dec1"])
        r2 += 1
    b.close()


# ---------------------------------------------------------------- comms plan
def comms_plan(out):
    b = Book(os.path.join(out, "communication-plan.xlsx"))
    ws, r = b.sheet("Plan", "Communication Plan", "What we communicate, to whom, how often and who owns it",
                    "Build this from the Stakeholder Register. Check each 'Manage closely' stakeholder appears in at least one row. "
                    "Review at each phase change.",
                    [26, 34, 32, 16, 16, 18, 18])
    r = b.header(ws, r, ["Communication", "Audience", "Purpose", "Format", "Frequency", "Owner", "Channel"])
    for x in D.COMMS:
        for c, v in enumerate([x[0], x[1], x[2], x[3], x[4], name(x[5]), x[6]]):
            ws.write(r, c, v, b.f["cell"])
        r += 1
    ws.freeze_panes(7, 1)
    b.close()


# ---------------------------------------------------------------- change log
def change_log(out):
    b = Book(os.path.join(out, "change-log.xlsx"))
    ws, r = b.sheet("Change Log", "Change Request Log", "Every requested change to the baseline and its outcome",
                    "Log every CR, including rejected ones. Net approved impact feeds the revised budget and schedule. "
                    "Raise a CR form for the detail.", [9, 40, 18, 11, 11, 13, 12, 17, 12])
    r = b.header(ws, r, ["CR #", "Title", "Requested by", "Raised", "Type", "Cost impact", "Days impact", "Status", "Decision date"])
    first = r
    for x in D.CHANGES:
        vals = [x[0], x[1], name(x[2]), x[3], x[4], x[5], x[6], x[7], x[8]]
        for c, v in enumerate(vals):
            if c in (3, 8):
                if v: ws.write_datetime(r, c, _dt(v), b.f["date"])
                else: ws.write(r, c, "", b.f["cell"])
            elif c == 5: ws.write_number(r, c, v, b.f["money"])
            elif c == 6: ws.write_number(r, c, v, b.f["num"])
            else: ws.write(r, c, v, b.f["cell"])
        r += 1
    b.rag(ws, f"H{first+1}:H{r+30}")
    b.lists(ws, f"H{first+1}:H{r+30}", ["Draft", "Pending SteerCo", "Approved", "Rejected", "Withdrawn"])
    b.lists(ws, f"E{first+1}:E{r+30}", ["Scope", "Schedule", "Cost", "Quality", "Technical"])
    s = r + 1
    ws.write(s, 1, "Original budget", b.f["bold"]); ws.write_number(s, 5, D.BAC, b.f["bmoney"])
    ws.write(s + 1, 1, "Net approved changes", b.f["bold"]); ws.write_formula(s + 1, 5, f'=SUMIF(H{first+1}:H{r},"Approved",F{first+1}:F{r})', b.f["bmoney"])
    ws.write_formula(s + 1, 6, f'=SUMIF(H{first+1}:H{r},"Approved",G{first+1}:G{r})', b.f["num"])
    ws.write(s + 2, 1, "Pending (not yet in baseline)", b.f["bold"]); ws.write_formula(s + 2, 5, f'=SUMIF(H{first+1}:H{r},"Pending*",F{first+1}:F{r})', b.f["bmoney"])
    ws.write(s + 3, 1, "Current approved budget", b.f["bold"]); ws.write_formula(s + 3, 5, f"=F{s+1}+F{s+2}", b.f["bmoney"])
    ws.freeze_panes(first, 2)
    b.close()


# ---------------------------------------------------------------- sprint metrics
def sprint_metrics(out):
    b = Book(os.path.join(out, "agile-sprint-metrics.xlsx"))
    ws, r = b.sheet("Velocity", "Agile Sprint Metrics", "Velocity, say/do ratio and scope change per sprint",
                    "Say/do = completed / committed. Below 80% for two sprints means the team is over-committing or being interrupted. "
                    "Use the 3-sprint rolling average for forecasting, not the best sprint.",
                    [14, 12, 13, 13, 12, 12, 16])
    r = b.header(ws, r, ["Sprint", "Start", "Committed (pts)", "Completed (pts)", "Scope added", "Say/do %", "Rolling avg (3)"])
    first = r
    for x in D.SPRINTS:
        ws.write(r, 0, x[0], b.f["cell"]); ws.write_datetime(r, 1, _dt(x[1]), b.f["date"])
        ws.write(r, 2, x[2], b.f["num"]); ws.write(r, 3, x[3], b.f["num"]); ws.write(r, 4, x[4], b.f["num"])
        ws.write_formula(r, 5, f"=D{r+1}/C{r+1}", b.f["pct"])
        ws.write_formula(r, 6, f"=AVERAGE(D{max(first, r-2)+1}:D{r+1})", b.f["dec1"])
        r += 1
    ws.conditional_format(f"F{first+1}:F{r}", {"type": "cell", "criteria": "<", "value": 0.8, "format": b.f["red"]})
    ws.conditional_format(f"F{first+1}:F{r}", {"type": "cell", "criteria": "between", "minimum": 0.8, "maximum": 0.899, "format": b.f["amber"]})
    ws.conditional_format(f"F{first+1}:F{r}", {"type": "cell", "criteria": ">=", "value": 0.9, "format": b.f["green"]})
    remaining = 130
    ws.write(r + 1, 0, "Forecast", b.f["eyebrow"])
    ws.write(r + 2, 0, "Points remaining in MVP backlog", b.f["bold"]); ws.write(r + 2, 3, remaining, b.f["num"])
    ws.write(r + 3, 0, "Sprints needed at rolling average", b.f["bold"]); ws.write_formula(r + 3, 3, f"=ROUNDUP(D{r+3}/G{r},0)", b.f["num"])
    ch = b.wb.add_chart({"type": "column"})
    ch.add_series({"name": "Committed", "categories": ["Velocity", first, 0, r - 1, 0], "values": ["Velocity", first, 2, r - 1, 2], "fill": {"color": "#AAB4BD"}, "gap": 80})
    ch.add_series({"name": "Completed", "categories": ["Velocity", first, 0, r - 1, 0], "values": ["Velocity", first, 3, r - 1, 3], "fill": {"color": ACCENT}})
    ln = b.wb.add_chart({"type": "line"})
    ln.add_series({"name": "Rolling avg (3)", "categories": ["Velocity", first, 0, r - 1, 0], "values": ["Velocity", first, 6, r - 1, 6],
                   "line": {"color": SERIES[1], "width": 2.25}, "marker": {"type": "circle", "size": 5, "fill": {"color": SERIES[1]}, "border": {"color": SERIES[1]}}})
    ch.combine(ln)
    ch.set_title({"name": "Velocity", "name_font": {"size": 11}}); ch.set_legend({"position": "bottom"}); ch.set_size({"width": 680, "height": 320})
    ch.set_y_axis({"major_gridlines": {"visible": True, "line": {"color": "#E3E7EA"}}})
    ws.insert_chart(r + 6, 0, ch)

    ws2, r2 = b.sheet("Burndown", f"{D.CURRENT_SPRINT[0]} Burndown", f"Committed {D.CURRENT_SPRINT[2]} points · 10 working days · updated daily",
                      "Enter remaining points at the end of each day. A flat line for 2+ days means blocked work: raise it at stand-up.",
                      [10, 14, 14])
    r2 = b.header(ws2, r2, ["Day", "Ideal", "Actual remaining"])
    f2 = r2
    for dday in range(11):
        ws2.write(r2, 0, dday, b.f["num"])
        ws2.write_formula(r2, 1, f"={D.CURRENT_SPRINT[2]}-{D.CURRENT_SPRINT[2]}/10*A{r2+1}", b.f["dec1"])
        v = D.BURNDOWN[dday]
        if v is None: ws2.write_formula(r2, 2, "=NA()", b.f["num"])
        else: ws2.write_number(r2, 2, v, b.f["num"])
        r2 += 1
    ch2 = b.wb.add_chart({"type": "line"})
    ch2.add_series({"name": "Ideal", "categories": ["Burndown", f2, 0, r2 - 1, 0], "values": ["Burndown", f2, 1, r2 - 1, 1], "line": {"color": "#AAB4BD", "dash_type": "dash", "width": 2}})
    ch2.add_series({"name": "Actual", "categories": ["Burndown", f2, 0, r2 - 1, 0], "values": ["Burndown", f2, 2, r2 - 1, 2], "line": {"color": ACCENT, "width": 2.5},
                    "marker": {"type": "circle", "size": 6, "fill": {"color": ACCENT}, "border": {"color": ACCENT}}})
    ch2.set_title({"name": "Sprint burndown", "name_font": {"size": 11}}); ch2.set_legend({"position": "bottom"})
    ch2.set_x_axis({"name": "Working day"}); ch2.set_y_axis({"name": "Points remaining", "min": 0}); ch2.set_size({"width": 620, "height": 320})
    ws2.insert_chart(f2 - 1, 4, ch2)
    b.close()


# ---------------------------------------------------------------- quality / DORA
def quality_metrics(out):
    b = Book(os.path.join(out, "quality-delivery-metrics.xlsx"))
    ws, r = b.sheet("Delivery KPIs", "Quality and Delivery Metrics", "Engineering health: DORA measures, testing and defects",
                    "Status compares the latest month to target. Direction tells you whether higher or lower is better. "
                    "Look at the trend over 3 months before acting on one bad month.",
                    [38, 10, 9, 9, 9, 9, 9, 10, 11])
    r = b.header(ws, r, ["Metric", "Unit", "Target"] + D.QUALITY_MONTHS + ["Better when", "Status"])
    first = r
    for x in D.DELIVERY_METRICS:
        ws.write(r, 0, x[0], b.f["cell"]); ws.write(r, 1, x[1], b.f["cell"]); ws.write(r, 2, x[2], b.f["dec1"])
        for i, v in enumerate(x[3:7]): ws.write_number(r, 3 + i, v, b.f["dec1"])
        ws.write(r, 7, "Higher" if x[7] == "+" else "Lower", b.f["cell"])
        ws.write_formula(r, 8, f'=IF(H{r+1}="Higher",IF(G{r+1}>=C{r+1},"Green",IF(G{r+1}>=C{r+1}*0.9,"Amber","Red")),IF(G{r+1}<=C{r+1},"Green",IF(G{r+1}<=C{r+1}*1.1,"Amber","Red")))', b.f["cell"])
        r += 1
    b.rag(ws, f"I{first+1}:I{r}")
    ws.write(first - 1, 9, "Trend", b.f["head"]); ws.set_column(9, 9, 14)
    for i in range(first, r):
        ws.add_sparkline(i, 9, {"range": f"'Delivery KPIs'!D{i+1}:G{i+1}", "markers": True, "series_color": ACCENT})

    ws2, r2 = b.sheet("Defects", "Defect Trend", "Defects found by severity and defects closed per month",
                      "Open defect backlog should fall from SIT onwards. If found > closed for 2 months, add fix capacity or slow new scope.",
                      [14, 10, 10, 10, 10, 12, 12, 12])
    r2 = b.header(ws2, r2, ["Month", "Critical", "High", "Medium", "Low", "Total found", "Closed", "Open backlog"])
    f2 = r2
    for m, mon in enumerate(D.QUALITY_MONTHS):
        ws2.write(r2, 0, mon, b.f["cell"])
        for i, sev in enumerate(["Critical", "High", "Medium", "Low"]): ws2.write_number(r2, 1 + i, D.DEFECTS[sev][m], b.f["num"])
        ws2.write_formula(r2, 5, f"=SUM(B{r2+1}:E{r2+1})", b.f["num"]); ws2.write_number(r2, 6, D.DEFECTS_CLOSED[m], b.f["num"])
        ws2.write_formula(r2, 7, f"=F{r2+1}-G{r2+1}" + (f"+H{r2}" if m else ""), b.f["num"])
        r2 += 1
    ch = b.wb.add_chart({"type": "column", "subtype": "stacked"})
    for i, (sev, col) in enumerate(zip(["Critical", "High", "Medium", "Low"], ["#B5523B", "#D9822B", "#8FA9EE", "#C9D1D8"])):
        ch.add_series({"name": sev, "categories": ["Defects", f2, 0, r2 - 1, 0], "values": ["Defects", f2, 1 + i, r2 - 1, 1 + i], "fill": {"color": col}, "gap": 70})
    ln = b.wb.add_chart({"type": "line"})
    ln.add_series({"name": "Closed", "categories": ["Defects", f2, 0, r2 - 1, 0], "values": ["Defects", f2, 6, r2 - 1, 6], "line": {"color": ACCENT, "width": 2.5},
                   "marker": {"type": "circle", "size": 6, "fill": {"color": ACCENT}, "border": {"color": ACCENT}}})
    ch.combine(ln)
    ch.set_title({"name": "Defects found (by severity) vs closed", "name_font": {"size": 11}}); ch.set_legend({"position": "bottom"}); ch.set_size({"width": 680, "height": 340})
    ws2.insert_chart(r2 + 2, 0, ch)
    b.close()


# ---------------------------------------------------------------- project health dashboard
def health_dashboard(out):
    b = Book(os.path.join(out, "project-health-dashboard.xlsx"))
    wb = b.wb
    ws = wb.add_worksheet("Dashboard"); data = wb.add_worksheet("Data")
    ws.hide_gridlines(2); ws.set_landscape(); ws.fit_to_pages(1, 1)
    ws.set_column(0, 0, 2); ws.set_column(1, 12, 13)
    ws.write(0, 1, f"{D.PROJECT.upper()}  ·  {D.ORG.upper()}", b.f["eyebrow"])
    ws.write(1, 1, "Project Health Dashboard", b.f["title"]); ws.set_row(1, 28)
    ws.write(2, 1, "Status date 19 Jun 2026 · numbers update from the Data tab", b.f["sub"])

    # Data tab
    data.set_column(0, 0, 26); data.set_column(1, 12, 12)
    data.write_row(0, 0, ["Month"] + D.MONTHS, b.f["head"])
    labels = [("PV cum", D.PV), ("EV cum", D.EV), ("AC cum", D.AC)]
    for i, (lab, series) in enumerate(labels):
        data.write(1 + i, 0, lab, b.f["bold"])
        cum = 0
        for m, v in enumerate(series):
            if v is None: data.write_formula(1 + i, 1 + m, "=NA()", b.f["money"])
            else:
                cum += v; data.write_number(1 + i, 1 + m, cum, b.f["money"])
    data.write(5, 0, "KPI", b.f["head"]); data.write(5, 1, "Value", b.f["head"])
    kpis = [("BAC", D.BAC), ("EV to date", "=F3"), ("AC to date", "=F4"), ("PV to date", "=F2"),
            ("SPI", "=B8/B10"), ("CPI", "=B8/B9"), ("EAC (BAC/CPI)", "=B7/B12"), ("% complete", "=B8/B7"),
            ("Open risks scored 15+", 1), ("Open issues", 4), ("Days to go-live", (D.GO_LIVE - D.STATUS_DATE).days)]
    for i, (k, v) in enumerate(kpis):
        data.write(6 + i, 0, k, b.f["cell"])
        fmt = b.f["dec"] if k in ("SPI", "CPI") else b.f["pct"] if "%" in k else b.f["money"] if k in ("BAC", "EV to date", "AC to date", "PV to date", "EAC (BAC/CPI)") else b.f["num"]
        (data.write_formula if isinstance(v, str) else data.write_number)(6 + i, 1, v, fmt)
    data.write(19, 0, "Risks by category", b.f["head"]); data.write(19, 1, "Open", b.f["head"])
    cats = {}
    for x in D.RISKS:
        if x[9] == "Open": cats[x[3]] = cats.get(x[3], 0) + 1
    for i, (k, v) in enumerate(sorted(cats.items(), key=lambda kv: -kv[1])):
        data.write(20 + i, 0, k, b.f["cell"]); data.write(20 + i, 1, v, b.f["num"])
    ncat = len(cats)
    data.write(28, 0, "Sprint", b.f["head"]); data.write(28, 1, "Committed", b.f["head"]); data.write(28, 2, "Completed", b.f["head"])
    for i, s in enumerate(D.SPRINTS):
        data.write(29 + i, 0, s[0].replace("Sprint ", "S"), b.f["cell"]); data.write(29 + i, 1, s[2], b.f["num"]); data.write(29 + i, 2, s[3], b.f["num"])

    # KPI tiles row
    tiles = [("OVERALL", "Amber", None), ("SPI", "=Data!B11", "kpi_val_dec"), ("CPI", "=Data!B12", "kpi_val_dec"),
             ("% COMPLETE", "=Data!B14", "kpi_val_pct"), ("EAC", "=Data!B13", "kpi_val_money"), ("DAYS TO GO-LIVE", "=Data!B17", "kpi_val")]
    for i, (lab, val, fmt) in enumerate(tiles):
        c = 1 + i * 2
        ws.merge_range(4, c, 4, c + 1, lab, b.f["kpi_label"])
        if fmt is None:
            ws.merge_range(5, c, 6, c + 1, val, wb.add_format({"font_size": 20, "bold": True, "bg_color": AMBER, "align": "center", "valign": "vcenter", "border": 1, "border_color": "#D5DCE2"}))
        else:
            ws.merge_range(5, c, 6, c + 1, "", b.f[fmt]); ws.write_formula(5, c, val, b.f[fmt])
    ws.set_row(5, 24); ws.set_row(6, 24)
    for c in (3, 5):
        ws.conditional_format(5, c, 5, c, {"type": "cell", "criteria": "<", "value": 0.95, "format": wb.add_format({"bg_color": AMBER})})
    # RAG by dimension
    ws.write(8, 1, "Health by dimension", b.f["eyebrow"])
    dims = [("Schedule", "Amber", "MVP +10 days; go-live holds"), ("Cost", "Amber", "CPI 0.90; CR-007 pending"),
            ("Scope", "Green", "No unapproved change"), ("Quality", "Green", "7 open high/critical, falling"),
            ("Resources", "Amber", "POS integration short 2 engineers"), ("Stakeholders", "Green", "Sponsor engaged; service concerns managed")]
    for i, (dim, rag_, note) in enumerate(dims):
        ws.write(9 + i, 1, dim, b.f["bold"]); ws.write(9 + i, 2, rag_, b.f["cell"]); ws.merge_range(9 + i, 3, 9 + i, 6, note, b.f["cell"])
    b.rag(ws, "C10:C15")
    # milestones
    ws.write(8, 8, "Next milestones", b.f["eyebrow"])
    for i, m in enumerate(D.MILESTONES[3:8]):
        ws.merge_range(9 + i, 8, 9 + i, 10, m[0], b.f["cell"]); ws.write_datetime(9 + i, 11, _dt(m[2]), b.f["date"]); ws.write(9 + i, 12, m[3], b.f["cell"])
    b.rag(ws, "M10:M14")
    # charts
    ch = wb.add_chart({"type": "line"})
    for i, (lab, color, dash) in enumerate([("PV", SERIES[2], "dash"), ("EV", SERIES[0], "solid"), ("AC", SERIES[1], "solid")]):
        ch.add_series({"name": lab, "categories": ["Data", 0, 1, 0, 9], "values": ["Data", 1 + i, 1, 1 + i, 9],
                       "line": {"color": color, "width": 2.25, "dash_type": dash}})
    ch.set_title({"name": "Cost S-curve (cumulative)", "name_font": {"size": 10}})
    ch.set_y_axis({"num_format": "$#,##0,\"k\"", "major_gridlines": {"visible": True, "line": {"color": "#E3E7EA"}}})
    ch.set_legend({"position": "bottom"}); ch.set_size({"width": 470, "height": 270}); ch.show_na_as_empty_cell()
    ws.insert_chart(16, 1, ch)
    ch2 = wb.add_chart({"type": "column"})
    ch2.add_series({"name": "Committed", "categories": ["Data", 29, 0, 28 + len(D.SPRINTS), 0], "values": ["Data", 29, 1, 28 + len(D.SPRINTS), 1], "fill": {"color": "#AAB4BD"}})
    ch2.add_series({"name": "Completed", "categories": ["Data", 29, 0, 28 + len(D.SPRINTS), 0], "values": ["Data", 29, 2, 28 + len(D.SPRINTS), 2], "fill": {"color": ACCENT}})
    ch2.set_title({"name": "Velocity (story points)", "name_font": {"size": 10}}); ch2.set_legend({"position": "bottom"}); ch2.set_size({"width": 400, "height": 270})
    ws.insert_chart(16, 7, ch2)
    ch3 = wb.add_chart({"type": "bar"})
    ch3.add_series({"name": "Open risks", "categories": ["Data", 20, 0, 19 + ncat, 0], "values": ["Data", 20, 1, 19 + ncat, 1], "fill": {"color": SERIES[1]}})
    ch3.set_title({"name": "Open risks by category", "name_font": {"size": 10}}); ch3.set_legend({"none": True}); ch3.set_size({"width": 470, "height": 240})
    ch3.set_y_axis({"reverse": True}); ch3.set_x_axis({"major_unit": 1, "min": 0})
    ws.insert_chart(31, 1, ch3)
    ws.write(31, 8, "Decisions needed", b.f["eyebrow"])
    for i, t in enumerate(["Approve CR-007 (+$65k) at SteerCo 24 Jun", "Escalate UAT environment (D-03, late)", "Confirm 2 extra POS integration engineers"]):
        ws.merge_range(32 + i, 8, 32 + i, 12, f"{i+1}. {t}", b.f["cell"])
    ws.set_footer(f"&L&8{D.SAMPLE_NOTE}&R&8{D.BRAND}")
    ws.activate()
    b.close()


# ---------------------------------------------------------------- program / portfolio dashboard
def portfolio_dashboard(out):
    b = Book(os.path.join(out, "program-portfolio-dashboard.xlsx"))
    ws, r = b.sheet("Portfolio", "Program Dashboard", f"{D.PROGRAM} · 5 projects · status date 19 Jun 2026",
                    "Each PM updates their row by Monday noon. Program totals and RAG counts calculate automatically. "
                    "Red projects get a recovery plan within 5 working days.",
                    [34, 15, 9, 9, 9, 9, 9, 13, 13, 10, 7, 7, 22, 11, 9])
    r = b.header(ws, r, ["Project", "PM", "Phase", "Overall", "Schedule", "Cost", "Scope", "Budget", "Actual to date", "% complete", "SPI", "CPI", "Next milestone", "Due", "High risks"])
    first = r
    for x in D.PORTFOLIO:
        for c, v in enumerate(x):
            if c in (7, 8): ws.write_number(r, c, v, b.f["money"])
            elif c == 9: ws.write_number(r, c, v / 100, b.f["pct"])
            elif c in (10, 11): ws.write_number(r, c, v, b.f["dec"])
            elif c == 13: ws.write_datetime(r, c, _dt(v), b.f["date"])
            elif c == 14: ws.write_number(r, c, v, b.f["num"])
            else: ws.write(r, c, v, b.f["cell"])
        r += 1
    b.rag(ws, f"D{first+1}:G{r}")
    for col in ("K", "L"):
        rng = f"{col}{first+1}:{col}{r}"
        ws.conditional_format(rng, {"type": "cell", "criteria": ">=", "value": 0.95, "format": b.f["green"]})
        ws.conditional_format(rng, {"type": "cell", "criteria": "between", "minimum": 0.85, "maximum": 0.9499, "format": b.f["amber"]})
        ws.conditional_format(rng, {"type": "cell", "criteria": "<", "value": 0.85, "format": b.f["red"]})
    ws.write(r, 0, "Program total", b.f["bold"])
    for c in range(1, 15): ws.write(r, c, "", b.f["bold"])
    ws.write_formula(r, 7, f"=SUM(H{first+1}:H{r})", b.f["bmoney"]); ws.write_formula(r, 8, f"=SUM(I{first+1}:I{r})", b.f["bmoney"])
    ws.write_formula(r, 9, f"=SUMPRODUCT(H{first+1}:H{r},J{first+1}:J{r})/H{r+1}", b.f["pct"])
    ws.write_formula(r, 14, f"=SUM(O{first+1}:O{r})", b.f["num"])
    tot = r
    s = tot + 2
    ws.write(s, 0, "Overall RAG count", b.f["eyebrow"])
    for i, rag_ in enumerate(["Green", "Amber", "Red"]):
        ws.write(s + 1 + i, 0, rag_, b.f["cell"]); ws.write_formula(s + 1 + i, 1, f'=COUNTIF(D{first+1}:D{tot},"{rag_}")', b.f["num"])
    b.rag(ws, f"A{s+2}:A{s+4}")
    ch = b.wb.add_chart({"type": "doughnut"})
    ch.add_series({"categories": ["Portfolio", s + 1, 0, s + 3, 0], "values": ["Portfolio", s + 1, 1, s + 3, 1],
                   "points": [{"fill": {"color": "#5FA36B"}}, {"fill": {"color": "#E0A43A"}}, {"fill": {"color": "#C8553D"}}], "data_labels": {"value": True}})
    ch.set_title({"name": "Projects by overall RAG", "name_font": {"size": 10}}); ch.set_hole_size(55); ch.set_size({"width": 360, "height": 260})
    ws.insert_chart(s, 2, ch)
    ch2 = b.wb.add_chart({"type": "bar"})
    ch2.add_series({"name": "Budget", "categories": ["Portfolio", first, 0, tot - 1, 0], "values": ["Portfolio", first, 7, tot - 1, 7], "fill": {"color": "#AAB4BD"}})
    ch2.add_series({"name": "Actual to date", "categories": ["Portfolio", first, 0, tot - 1, 0], "values": ["Portfolio", first, 8, tot - 1, 8], "fill": {"color": ACCENT}})
    ch2.set_title({"name": "Budget vs actual by project", "name_font": {"size": 10}}); ch2.set_x_axis({"num_format": "$#,##0,\"k\""}); ch2.set_y_axis({"reverse": True})
    ch2.set_legend({"position": "bottom"}); ch2.set_size({"width": 560, "height": 260})
    ws.insert_chart(s, 7, ch2)
    ws.freeze_panes(first, 1)
    b.close()


# ---------------------------------------------------------------- cutover plan
def cutover_plan(out):
    b = Book(os.path.join(out, "cutover-runbook.xlsx"))
    ws, r = b.sheet("Runbook", "Cutover Runbook", "Go-live weekend · Sat 26 Sep 22:00 to Mon 28 Sep 05:00",
                    "One row per step, in order. Every step has an owner, a planned time and a check. Rehearse twice. "
                    "Fill Actual and Status live during cutover; the go/no-go points stop the clock until the decision maker confirms.",
                    [6, 12, 12, 46, 18, 12, 12, 12, 30])
    r = b.header(ws, r, ["#", "Planned start", "Duration (min)", "Step", "Owner", "Actual start", "Actual end", "Status", "Check / evidence"])
    first = r
    steps = [
        ("Sat 22:00", 15, "Cutover go/no-go call 1: confirm readiness", "delivery", "Decision recorded in log"),
        ("Sat 22:15", 30, "Freeze order intake on web and app (maintenance page)", "tech", "Maintenance page live"),
        ("Sat 22:45", 60, "Final POS and e-commerce data extract", "data", "Row counts match source"),
        ("Sat 23:45", 180, "Load customer profiles and run identity resolution", "data", "Match rate >= 97%"),
        ("Sun 02:45", 60, "Reconcile record counts and sample 200 profiles", "qa", "Reconciliation report signed"),
        ("Sun 03:45", 15, "Go/no-go call 2: data accepted?", "sponsor", "Decision recorded; rollback if no"),
        ("Sun 04:00", 120, "Switch integrations to new platform (90 real-time, 30 batch)", "vendor", "Health checks green"),
        ("Sun 06:00", 240, "Smoke test: 40 scripted journeys", "qa", "40/40 pass"),
        ("Sun 10:00", 120, "Business verification in 3 pilot stores", "stores", "Store leads confirm"),
        ("Sun 12:00", 15, "Go/no-go call 3: open to customers?", "sponsor", "Decision recorded"),
        ("Sun 12:15", 30, "Remove maintenance page; monitor", "tech", "Orders flowing"),
        ("Mon 05:00", 0, "Hypercare starts; contact centre opens on new console", "service", "Hypercare rota active"),
    ]
    for i, (t, dur, step, own, chk) in enumerate(steps, 1):
        for c, v in enumerate([i, t, dur, step, name(own), "", "", "Not started", chk]):
            ws.write(r, c, v, b.f["num"] if c in (0, 2) else b.f["cell"])
        r += 1
    b.lists(ws, f"H{first+1}:H{r+20}", ["Not started", "In progress", "Done", "Blocked", "Rolled back"])
    for w, fmt in (("Done", "green"), ("In progress", "amber"), ("Blocked", "red"), ("Rolled back", "red")):
        ws.conditional_format(f"H{first+1}:H{r+20}", {"type": "cell", "criteria": "==", "value": f'"{w}"', "format": b.f[fmt]})
    ws.conditional_format(f"D{first+1}:D{r}", {"type": "text", "criteria": "begins with", "value": "Go/no-go", "format": b.f["amber"]})
    ws.freeze_panes(first, 4)
    ws2, r2 = b.sheet("Rollback", "Rollback Plan", "Steps to return to the old platform if a go/no-go call says no",
                      "Rollback must be rehearsed. Agree the latest point at which rollback is still possible (point of no return).", [6, 50, 18, 14])
    r2 = b.header(ws2, r2, ["#", "Step", "Owner", "Duration (min)"])
    for i, (st, own, dur) in enumerate([("Re-point integrations to legacy CRM and order service", "tech", 45),
                                        ("Restore legacy customer database snapshot", "data", 60),
                                        ("Smoke test legacy journeys", "qa", 60),
                                        ("Remove maintenance page; notify stores and contact centre", "service", 15)], 1):
        for c, v in enumerate([i, st, name(own), dur]):
            ws2.write(r2, c, v, b.f["num"] if c in (0, 3) else b.f["cell"])
        r2 += 1
    ws2.write(r2 + 1, 1, "Point of no return: Sun 12:15 (customers placing orders on new platform)", b.f["bold"])
    b.close()


# ---------------------------------------------------------------- benefits register
def benefits_register(out):
    b = Book(os.path.join(out, "benefits-register.xlsx"))
    ws, r = b.sheet("Benefits", "Benefits Register", "Benefits promised in the business case and how we will prove them",
                    "Every benefit needs a baseline, a target, a date and a named business owner (not the PM). "
                    "Measure after go-live at the review points; the project can close before benefits land.",
                    [7, 28, 26, 11, 11, 11, 11, 18, 14, 11, 12])
    r = b.header(ws, r, ["ID", "Benefit", "Measure", "Baseline", "Target", "Actual (latest)", "% of target", "Benefit owner", "Measure from", "Type", "Status"])
    first = r
    rows = [("B-01", "Faster customer service", "Average handle time (min)", 7.8, 6.2, 6.9, "service", "Jan 2027", "Efficiency", "On track"),
            ("B-02", "BOPIS revenue", "% online orders via BOPIS", 0, 8, 3.1, "stores", "Mar 2027", "Revenue", "On track"),
            ("B-03", "Cross-channel satisfaction", "Cross-channel NPS", 4, 20, 9, "po", "Mar 2027", "Customer", "On track"),
            ("B-04", "Single customer view", "% customers with one profile", 0, 100, 97.8, "data", "Oct 2026", "Enabler", "At risk"),
            ("B-05", "Marketing conversion", "Email conversion rate (%)", 1.9, 2.6, 2.0, "po", "Jun 2027", "Revenue", "Not started")]
    for x in rows:
        ws.write(r, 0, x[0], b.f["cell"]); ws.write(r, 1, x[1], b.f["cell"]); ws.write(r, 2, x[2], b.f["cell"])
        for c, v in zip((3, 4, 5), x[3:6]): ws.write_number(r, c, v, b.f["dec1"])
        ws.write_formula(r, 6, f"=IFERROR((F{r+1}-D{r+1})/(E{r+1}-D{r+1}),0)", b.f["pct"])
        ws.write(r, 7, name(x[6]), b.f["cell"]); ws.write(r, 8, x[7], b.f["cell"]); ws.write(r, 9, x[8], b.f["cell"]); ws.write(r, 10, x[9], b.f["cell"])
        r += 1
    b.rag(ws, f"K{first+1}:K{r+20}")
    ws.conditional_format(f"G{first+1}:G{r}", {"type": "data_bar", "bar_color": "#8FA9EE", "bar_solid": True, "min_type": "num", "min_value": 0, "max_type": "num", "max_value": 1})
    ws.write(r + 1, 0, "% of target = (Actual - Baseline) / (Target - Baseline). Works whether the measure should go up or down.", b.f["note"])
    b.close()


def build(out):
    for fn in (stakeholder_register, raci, raid_log, schedule, budget_evm, resource_plan, comms_plan, change_log,
               sprint_metrics, quality_metrics, health_dashboard, portfolio_dashboard, cutover_plan, benefits_register):
        fn(out)
