"""Resource management templates.

Worked example: the Bengaluru delivery centre of Brightpath Systems (fictional),
the SI partner that staffs Project Lighthouse in the project templates.
Status date matches the project templates: 19 Jun 2026.
"""
import os
import random
from datetime import date, timedelta

from xlsxwriter.utility import xl_col_to_name as colname

import data as D
from gen_xlsx import Book, _dt, ACCENT

RM_ORG = "Brightpath Systems · Bengaluru Delivery Centre"
STATUS = D.STATUS_DATE

SKILLS = ["Java", "React", "Python / SQL", "AWS", "QA Automation", "UX Design", "Business Analysis", "Salesforce", "Power BI", "Delivery Mgmt"]

# name, role, grade, cost rate ($/day), bill rate ($/day), primary skills {skill: level 0-4}
PEOPLE = [
    ("Ananya Rao", "Tech Lead", "G6", 420, 950, {"Java": 4, "AWS": 3, "React": 2, "Delivery Mgmt": 2}),
    ("Karthik Iyer", "Senior Developer", "G5", 330, 750, {"Java": 4, "React": 2, "AWS": 2}),
    ("Meera Nair", "Senior Developer", "G5", 330, 750, {"React": 4, "Java": 2, "UX Design": 1}),
    ("Rohan Gupta", "Developer", "G4", 240, 600, {"Java": 3, "Python / SQL": 2}),
    ("Divya Menon", "Developer", "G4", 240, 600, {"React": 3, "Java": 1}),
    ("Arjun Reddy", "Developer", "G3", 180, 500, {"Java": 2, "React": 2}),
    ("Sneha Kulkarni", "Data Engineer", "G5", 330, 750, {"Python / SQL": 4, "AWS": 3, "Power BI": 2}),
    ("Vikram Shetty", "Data Engineer", "G4", 240, 600, {"Python / SQL": 3, "Power BI": 3}),
    ("Priyanka Das", "Cloud Engineer", "G5", 330, 750, {"AWS": 4, "Python / SQL": 2, "Java": 1}),
    ("Nikhil Joshi", "QA Lead", "G5", 300, 700, {"QA Automation": 4, "Java": 2}),
    ("Kavya Pillai", "QA Engineer", "G3", 170, 450, {"QA Automation": 3}),
    ("Rahul Verma", "QA Engineer", "G3", 170, 450, {"QA Automation": 2, "Python / SQL": 1}),
    ("Ishita Bose", "UX Designer", "G4", 250, 650, {"UX Design": 4, "React": 1}),
    ("Aditya Hegde", "Business Analyst", "G4", 240, 600, {"Business Analysis": 4, "Power BI": 2}),
    ("Pooja Sharma", "Business Analyst", "G3", 180, 500, {"Business Analysis": 3, "Salesforce": 1}),
    ("Siddharth Rao", "Salesforce Developer", "G4", 260, 650, {"Salesforce": 4, "Java": 1}),
    ("Neha Agarwal", "Salesforce Developer", "G3", 190, 520, {"Salesforce": 3}),
    ("Manoj Kumar", "Project Manager", "G6", 400, 900, {"Delivery Mgmt": 4, "Business Analysis": 2}),
    ("Lakshmi Prasad", "Project Manager", "G5", 330, 750, {"Delivery Mgmt": 3, "Business Analysis": 2}),
    ("Farhan Ali", "Developer", "G3", 180, 500, {"React": 2, "Java": 1}),
    ("Deepa Krishnan", "BI Developer", "G4", 240, 600, {"Power BI": 4, "Python / SQL": 3}),
    ("Varun Malhotra", "Cloud Engineer", "G4", 250, 620, {"AWS": 3, "Java": 1}),
    ("Shreya Banerjee", "Developer", "G2", 130, 380, {"Java": 1, "React": 1}),
    ("Gautam Naidu", "Developer", "G2", 130, 380, {"Python / SQL": 1, "React": 1}),
]
ACCOUNTS = ["Halcyon Outfitters (Lighthouse)", "Kestrel Insurance", "Verdant Foods", "Orbit Telecom"]


class RMBook(Book):
    """Same look as the project templates, with the delivery-centre header."""
    def sheet(self, *a, **k):
        ws, r = super().sheet(*a, **k)
        ws.write(0, 0, "BRIGHTPATH SYSTEMS  ·  BENGALURU DELIVERY CENTRE", self.f["eyebrow"])
        return ws, r


def _rng():
    return random.Random(42)


# ---------------------------------------------------------------- skills matrix
def skills_matrix(out):
    b = RMBook(os.path.join(out, "skills-matrix.xlsx"))
    ws, r = b.sheet("Skills", "Skills Matrix", f"{RM_ORG} · 24 people x 10 skills · 0 = none, 4 = can lead and teach",
                    "Rate each person 0-4 on each skill with their manager. The bottom rows count how many people can work "
                    "independently (3+) on each skill. Red = fewer than 2: one resignation away from a gap.",
                    [20, 20, 7] + [11] * len(SKILLS) + [10])
    r = b.header(ws, r, ["Name", "Role", "Grade"] + SKILLS + ["Top skill"])
    first = r
    lvl = b.wb.add_format({"font_name": "Calibri", "font_size": 10, "border": 1, "border_color": "#D5DCE2", "align": "center", "num_format": '0;-0;"·"'})
    for nm, role, gr, _, _, sk in PEOPLE:
        ws.write(r, 0, nm, b.f["cell"]); ws.write(r, 1, role, b.f["cell"]); ws.write(r, 2, gr, b.f["cell"])
        for j, s in enumerate(SKILLS):
            ws.write_number(r, 3 + j, sk.get(s, 0), lvl)
        last = colname(2 + len(SKILLS))
        ws.write_formula(r, 3 + len(SKILLS), f"=INDEX($D${first}:${last}${first},1,MATCH(MAX(D{r+1}:{last}{r+1}),D{r+1}:{last}{r+1},0))", b.f["cell"])
        r += 1
    grid = f"D{first+1}:{colname(2+len(SKILLS))}{r}"
    ws.conditional_format(grid, {"type": "3_color_scale", "min_type": "num", "min_value": 0, "mid_type": "num", "mid_value": 2,
                                 "max_type": "num", "max_value": 4, "min_color": "#F4F5F7", "mid_color": "#A9BEF2", "max_color": "#1C4ED8"})
    b.lists(ws, grid, ["0", "1", "2", "3", "4"])
    ws.write(r + 1, 1, "People at 3+ (independent)", b.f["bold"]); ws.write(r + 2, 1, "People at 4 (can lead)", b.f["bold"])
    ws.write(r + 3, 1, "Coverage risk", b.f["bold"])
    for j in range(len(SKILLS)):
        L = colname(3 + j)
        ws.write_formula(r + 1, 3 + j, f'=COUNTIF({L}{first+1}:{L}{r},">=3")', b.f["num"])
        ws.write_formula(r + 2, 3 + j, f'=COUNTIF({L}{first+1}:{L}{r},4)', b.f["num"])
        ws.write_formula(r + 3, 3 + j, f'=IF({L}{r+2}<2,"Gap",IF({L}{r+2}<3,"Thin","OK"))', b.f["cell"])
    b.rag(ws, f"D{r+4}:{colname(2+len(SKILLS))}{r+4}", {"OK": "green", "Thin": "amber", "Gap": "red"})
    ws.freeze_panes(first, 3)
    ws.write(r + 5, 0, "Scale: 0 none · 1 aware · 2 works with help · 3 works independently · 4 can lead and teach", b.f["note"])
    b.close()


# ---------------------------------------------------------------- bench tracker
BENCH = [  # name, bench since, reason, next opportunity, probability, action, owner
    ("Arjun Reddy", date(2026, 5, 29), "Verdant Foods phase 1 ended", "Orbit Telecom app rebuild (RR-118)", "Proposed", "Shadow Karthik on Lighthouse; React refresher", "Manoj Kumar"),
    ("Neha Agarwal", date(2026, 5, 4), "Salesforce demand slowed", "Kestrel CRM change requests (RR-121)", "Pipeline", "Cross-skill to Power BI (2-week course)", "Lakshmi Prasad"),
    ("Shreya Banerjee", date(2026, 6, 8), "Joined from campus hiring", "Lighthouse ramp-up (RR-116)", "Soft booked", "Onboarding + internal accelerator", "Ananya Rao"),
    ("Gautam Naidu", date(2026, 6, 8), "Joined from campus hiring", "Data Platform support (RR-119)", "Pipeline", "Python / SQL bootcamp", "Sneha Kulkarni"),
    ("Pooja Sharma", date(2026, 4, 20), "Kestrel discovery ended early", "None confirmed", "None", "Internal: PMO tooling; escalate to delivery head", "Manoj Kumar"),
]


def bench_tracker(out):
    b = RMBook(os.path.join(out, "bench-tracker.xlsx"))
    ws, r = b.sheet("Bench", "Bench Tracker", f"{RM_ORG} · status date {D.fmt_date(STATUS)}",
                    "Everyone not on billable work today. Days on bench and bench cost calculate from the status date in B5 of "
                    "the Summary tab. Every row needs a next opportunity and an action. 30+ days is red: escalate.",
                    [20, 14, 9, 13, 30, 34, 13, 40, 18])
    r = b.header(ws, r, ["Name", "Bench since", "Days", "Bench cost", "Why on bench", "Next opportunity", "Likelihood", "Action meanwhile", "Owner"])
    first = r
    rate = {p[0]: p[3] for p in PEOPLE}
    for nm, since, why, nxt, prob, act, own in BENCH:
        ws.write(r, 0, nm, b.f["cell"]); ws.write_datetime(r, 1, _dt(since), b.f["date"])
        ws.write_formula(r, 2, f"=NETWORKDAYS(B{r+1},Summary!$B$5)", b.f["num"])
        ws.write_formula(r, 3, f"=C{r+1}*{rate[nm]}", b.f["money"])
        for c, v in zip(range(4, 9), [why, nxt, prob, act, own]):
            ws.write(r, c, v, b.f["cell"])
        r += 1
    ws.conditional_format(f"C{first+1}:C{r+20}", {"type": "cell", "criteria": ">=", "value": 30, "format": b.f["red"]})
    ws.conditional_format(f"C{first+1}:C{r+20}", {"type": "cell", "criteria": "between", "minimum": 15, "maximum": 29, "format": b.f["amber"]})
    b.lists(ws, f"G{first+1}:G{r+20}", ["Hard booked", "Soft booked", "Proposed", "Pipeline", "None"])
    b.rag(ws, f"G{first+1}:G{r+20}", {"Hard booked": "green", "Soft booked": "green", "Proposed": "amber", "Pipeline": "amber", "None": "red"})
    ws.freeze_panes(first, 1)

    ws2, r2 = b.sheet("Summary", "Bench Summary", "Updates automatically from the Bench tab", None, [34, 16])
    ws2.write(4, 0, "Status date", b.f["bold"]); ws2.write_datetime(4, 1, _dt(STATUS), b.f["date"])
    rows = [("People on bench", "=COUNTA(Bench!A8:A100)", "num"),
            ("Bench % of 24 people", "=B7/24", "pct"),
            ("Average days on bench", "=AVERAGE(Bench!C8:C100)", "num"),
            ("On bench 30+ days", '=COUNTIF(Bench!C8:C100,">=30")', "num"),
            ("Bench cost to date", "=SUM(Bench!D8:D100)", "money"),
            ("With no next opportunity", '=COUNTIF(Bench!G8:G100,"None")', "num")]
    for i, (k, f, fmt) in enumerate(rows):
        ws2.write(6 + i, 0, k, b.f["cell"]); ws2.write_formula(6 + i, 1, f, b.f[fmt])
    b.close()


# ---------------------------------------------------------------- utilisation & billability
def utilisation_tracker(out):
    rng = _rng()
    b = RMBook(os.path.join(out, "utilisation-billability-tracker.xlsx"))
    weeks = [STATUS - timedelta(days=STATUS.weekday()) - timedelta(weeks=7 - i) for i in range(8)]
    bench_names = {x[0] for x in BENCH}
    ws, r = b.sheet("Weekly hours", "Utilisation & Billability Tracker", f"{RM_ORG} · 8 weeks to {D.fmt_date(STATUS)} · 40 available hours per week",
                    "Enter hours from timesheets each Monday. Utilisation = (billable + non-billable project) / available. "
                    "Billability = billable / available. Targets: utilisation 85%, billability 75%. Leave reduces available hours.",
                    [12, 20, 10, 10, 12, 12, 10, 12, 12])
    r = b.header(ws, r, ["Week of", "Name", "Available", "Leave", "Billable", "Non-billable project", "Internal / bench", "Utilisation", "Billability"])
    first = r
    for wk in weeks:
        for nm, role, *_ in PEOPLE:
            joined = {x[0]: x[1] for x in BENCH if x[2].startswith("Joined")}
            if nm in joined and wk < joined[nm] - timedelta(days=joined[nm].weekday()):
                continue
            leave = 8 if rng.random() < 0.12 else 0
            avail = 40 - leave
            if nm in bench_names and wk >= (dict((x[0], x[1]) for x in BENCH)[nm] - timedelta(days=7)):
                bill, nbp = 0, rng.choice([0, 4, 8])
            elif role in ("Project Manager",):
                bill, nbp = rng.choice([28, 32]), rng.choice([4, 6])
            else:
                bill = rng.choice([28, 30, 32, 34, 36, 38]); nbp = rng.choice([0, 2, 4])
            bill = min(bill, avail); nbp = min(nbp, avail - bill)
            internal = avail - bill - nbp
            ws.write_datetime(r, 0, _dt(wk), b.f["date"]); ws.write(r, 1, nm, b.f["cell"])
            ws.write_number(r, 2, avail, b.f["num"]); ws.write_number(r, 3, leave, b.f["num"])
            ws.write_number(r, 4, bill, b.f["num"]); ws.write_number(r, 5, nbp, b.f["num"]); ws.write_number(r, 6, internal, b.f["num"])
            ws.write_formula(r, 7, f"=IFERROR((E{r+1}+F{r+1})/C{r+1},0)", b.f["pct"])
            ws.write_formula(r, 8, f"=IFERROR(E{r+1}/C{r+1},0)", b.f["pct"])
            r += 1
    last = r
    for col in ("H", "I"):
        tgt = 0.85 if col == "H" else 0.75
        ws.conditional_format(f"{col}{first+1}:{col}{last}", {"type": "cell", "criteria": ">=", "value": tgt, "format": b.f["green"]})
        ws.conditional_format(f"{col}{first+1}:{col}{last}", {"type": "cell", "criteria": "between", "minimum": tgt - 0.15, "maximum": tgt - 0.0001, "format": b.f["amber"]})
        ws.conditional_format(f"{col}{first+1}:{col}{last}", {"type": "cell", "criteria": "<", "value": tgt - 0.15, "format": b.f["red"]})
    ws.freeze_panes(first, 2); ws.autofilter(first - 1, 0, last - 1, 8)

    ws2, r2 = b.sheet("Team trend", "Team Utilisation & Billability", "Weekly totals across the delivery centre",
                      "Calculated from the Weekly hours tab. Watch the gap between the two lines: a big gap means people are busy "
                      "on work nobody is paying for.", [12, 12, 12, 12, 12])
    r2 = b.header(ws2, r2, ["Week of", "Available", "Billable", "Utilisation", "Billability"])
    f2 = r2
    for wk in weeks:
        ws2.write_datetime(r2, 0, _dt(wk), b.f["date"])
        crit = f"'Weekly hours'!$A${first+1}:$A${last},A{r2+1}"
        ws2.write_formula(r2, 1, f"=SUMIFS('Weekly hours'!$C${first+1}:$C${last},{crit})", b.f["num"])
        ws2.write_formula(r2, 2, f"=SUMIFS('Weekly hours'!$E${first+1}:$E${last},{crit})", b.f["num"])
        ws2.write_formula(r2, 3, f"=(C{r2+1}+SUMIFS('Weekly hours'!$F${first+1}:$F${last},{crit}))/B{r2+1}", b.f["pct"])
        ws2.write_formula(r2, 4, f"=C{r2+1}/B{r2+1}", b.f["pct"])
        r2 += 1
    ch = b.wb.add_chart({"type": "line"})
    for col, name, color in ((3, "Utilisation", ACCENT), (4, "Billability", "#D9822B")):
        ch.add_series({"name": name, "categories": ["Team trend", f2, 0, r2 - 1, 0], "values": ["Team trend", f2, col, r2 - 1, col],
                       "line": {"color": color, "width": 2.5}, "marker": {"type": "circle", "size": 6, "fill": {"color": color}, "border": {"color": color}}})
    ch.set_y_axis({"num_format": "0%", "min": 0.5, "max": 1, "major_gridlines": {"visible": True, "line": {"color": "#E3E7EA"}}})
    ch.set_x_axis({"num_format": "dd-mmm"}); ch.set_title({"name": "Utilisation vs billability (target 85% / 75%)", "name_font": {"size": 11}})
    ch.set_legend({"position": "bottom"}); ch.set_size({"width": 680, "height": 320})
    ws2.insert_chart(r2 + 2, 0, ch)
    b.close()


# ---------------------------------------------------------------- resource request log
REQUESTS = [  # id, account, role, skills, grade, start, weeks, raised, status, proposed/filled, filled date
    ("RR-112", ACCOUNTS[0], "Senior Developer", "Java, AWS", "G5", date(2026, 5, 4), 20, date(2026, 4, 13), "Filled", "Karthik Iyer", date(2026, 4, 24)),
    ("RR-113", ACCOUNTS[0], "QA Engineer", "QA Automation", "G3", date(2026, 5, 18), 16, date(2026, 4, 20), "Filled", "Kavya Pillai", date(2026, 5, 8)),
    ("RR-114", ACCOUNTS[1], "Salesforce Developer", "Salesforce", "G4", date(2026, 5, 11), 12, date(2026, 4, 22), "Filled", "Siddharth Rao", date(2026, 4, 29)),
    ("RR-115", ACCOUNTS[2], "Data Engineer", "Python / SQL, AWS", "G4", date(2026, 6, 1), 24, date(2026, 5, 6), "Filled", "Vikram Shetty", date(2026, 5, 27)),
    ("RR-116", ACCOUNTS[0], "Developer", "Java, React", "G2-G3", date(2026, 6, 22), 16, date(2026, 5, 25), "Soft booked", "Shreya Banerjee", None),
    ("RR-117", ACCOUNTS[3], "Tech Lead", "Java, AWS, leadership", "G6", date(2026, 7, 6), 26, date(2026, 5, 28), "Open", "", None),
    ("RR-118", ACCOUNTS[3], "Developer", "React", "G3", date(2026, 7, 6), 26, date(2026, 5, 28), "Proposed", "Arjun Reddy", None),
    ("RR-119", ACCOUNTS[2], "Data Engineer", "Python / SQL", "G2-G3", date(2026, 7, 1), 12, date(2026, 6, 3), "Proposed", "Gautam Naidu", None),
    ("RR-120", ACCOUNTS[0], "Performance Tester", "QA Automation, JMeter", "G4", date(2026, 7, 20), 4, date(2026, 6, 10), "Open", "", None),
    ("RR-121", ACCOUNTS[1], "Salesforce Developer", "Salesforce", "G3", date(2026, 7, 13), 8, date(2026, 6, 15), "Open", "", None),
    ("RR-111", ACCOUNTS[1], "UX Designer", "UX Design", "G4", date(2026, 4, 20), 6, date(2026, 3, 30), "Lost", "", None),
]


def request_log(out):
    b = RMBook(os.path.join(out, "resource-request-log.xlsx"))
    ws, r = b.sheet("Requests", "Resource Request Log", f"{RM_ORG} · demand pipeline · status date {D.fmt_date(STATUS)}",
                    "One row per role requested, from the moment an account lead asks. Days open runs until it is filled. "
                    "Open requests starting within 3 weeks turn red. Lost requests stay in the log: they show where you couldn't staff.",
                    [9, 28, 20, 22, 8, 11, 8, 11, 13, 18, 11, 11, 10])
    r = b.header(ws, r, ["ID", "Account", "Role", "Skills", "Grade", "Start", "Weeks", "Raised", "Status", "Proposed / filled by", "Filled on", "Time to fill (days)", "Starts in (days)"])
    first = r
    for x in REQUESTS:
        for c, v in enumerate(x):
            if c in (5, 7, 10):
                if v: ws.write_datetime(r, c, _dt(v), b.f["date"])
                else: ws.write(r, c, "", b.f["cell"])
            elif c == 6: ws.write_number(r, c, v, b.f["num"])
            else: ws.write(r, c, v, b.f["cell"])
        ws.write_formula(r, 11, f'=IF(K{r+1}<>"",NETWORKDAYS(H{r+1},K{r+1}),"")', b.f["num"])
        ws.write_formula(r, 12, f'=IF(OR(I{r+1}="Filled",I{r+1}="Lost"),"",F{r+1}-Summary!$B$5)', b.f["num"])
        r += 1
    b.lists(ws, f"I{first+1}:I{r+30}", ["Open", "Proposed", "Soft booked", "Filled", "Lost"])
    b.rag(ws, f"I{first+1}:I{r+30}", {"Filled": "green", "Soft booked": "green", "Proposed": "amber", "Open": "amber", "Lost": "red"})
    ws.conditional_format(f"M{first+1}:M{r+30}", {"type": "cell", "criteria": "between", "minimum": -999, "maximum": 21, "format": b.f["red"]})
    ws.freeze_panes(first, 1); ws.autofilter(first - 1, 0, r - 1, 12)

    ws2, _ = b.sheet("Summary", "Demand Summary", "Updates automatically from the Requests tab", None, [36, 14])
    ws2.write(4, 0, "Status date", b.f["bold"]); ws2.write_datetime(4, 1, _dt(STATUS), b.f["date"])
    rows = [("Requests logged", "=COUNTA(Requests!A8:A200)", "num"),
            ("Filled", '=COUNTIF(Requests!I8:I200,"Filled")', "num"),
            ("Lost (could not staff)", '=COUNTIF(Requests!I8:I200,"Lost")', "num"),
            ("Fill rate (filled / closed)", "=B8/(B8+B9)", "pct"),
            ("Average time to fill (working days)", "=AVERAGE(Requests!L8:L200)", "num"),
            ("Open or proposed", '=COUNTIF(Requests!I8:I200,"Open")+COUNTIF(Requests!I8:I200,"Proposed")', "num"),
            ("Open and starting within 3 weeks", '=COUNTIFS(Requests!I8:I200,"Open",Requests!M8:M200,"<=21")', "num")]
    for i, (k, f, fmt) in enumerate(rows):
        ws2.write(6 + i, 0, k, b.f["cell"]); ws2.write_formula(6 + i, 1, f, b.f[fmt])
    b.close()


# ---------------------------------------------------------------- allocation heatmap
def allocation_heatmap(out):
    rng = random.Random(7)
    b = RMBook(os.path.join(out, "allocation-heatmap.xlsx"))
    weeks = [STATUS - timedelta(days=STATUS.weekday()) + timedelta(weeks=i) for i in range(12)]
    bench_names = {x[0] for x in BENCH}
    ws, r = b.sheet("Allocation", "Allocation Heatmap", f"{RM_ORG} · next 12 weeks from {D.fmt_date(weeks[0])} · % of each person's week",
                    "Enter planned allocation per person per week (hard + soft bookings). Blue = healthy 80-100%. Amber = under 80% "
                    "(capacity to sell). Red = over 100% (someone is double-booked). Review weekly with account leads.",
                    [20, 18, 26] + [7] * len(weeks) + [9])
    r = b.header(ws, r, ["Name", "Role", "Main account"] + [w.strftime("%d-%b") for w in weeks] + ["Avg"])
    first = r
    for i, (nm, role, *_rest) in enumerate(PEOPLE):
        acct = ACCOUNTS[i % len(ACCOUNTS)] if nm not in bench_names else "Bench"
        ws.write(r, 0, nm, b.f["cell"]); ws.write(r, 1, role, b.f["cell"]); ws.write(r, 2, acct, b.f["cell"])
        for j in range(len(weeks)):
            if nm in bench_names:
                v = 0 if j < 2 else rng.choice([0, 50, 100]) if nm != "Pooja Sharma" else 0
            elif nm in ("Ananya Rao", "Manoj Kumar") and j in (3, 4, 5):
                v = 120
            elif j >= 9 and acct.startswith("Verdant"):
                v = 50
            else:
                v = rng.choice([80, 100, 100, 100, 90])
            ws.write_number(r, 3 + j, v / 100, b.f["pct"])
        L1, L2 = colname(3), colname(2 + len(weeks))
        ws.write_formula(r, 3 + len(weeks), f"=AVERAGE({L1}{r+1}:{L2}{r+1})", b.f["pct"])
        r += 1
    grid = f"D{first+1}:{colname(2+len(weeks))}{r}"
    ws.conditional_format(grid, {"type": "cell", "criteria": ">", "value": 1, "format": b.f["red"]})
    ws.conditional_format(grid, {"type": "cell", "criteria": "between", "minimum": 0.8, "maximum": 1,
                                 "format": b.wb.add_format({"bg_color": "#C9D7FA", "bold": True})})
    ws.conditional_format(grid, {"type": "cell", "criteria": "<", "value": 0.8, "format": b.f["amber"]})
    ws.write(r, 2, "Team average", b.f["bold"])
    for j in range(len(weeks) + 1):
        L = colname(3 + j); ws.write_formula(r, 3 + j, f"=AVERAGE({L}{first+1}:{L}{r})", b.wb.add_format({"bold": True, "num_format": "0%", "bg_color": "#F1F4F6", "border": 1, "border_color": "#D5DCE2"}))
    ws.write(r + 1, 2, "People over 100%", b.f["bold"])
    for j in range(len(weeks)):
        L = colname(3 + j); ws.write_formula(r + 1, 3 + j, f'=COUNTIF({L}{first+1}:{L}{r},">1")', b.f["num"])
    ws.write(r + 2, 2, "People under 50%", b.f["bold"])
    for j in range(len(weeks)):
        L = colname(3 + j); ws.write_formula(r + 2, 3 + j, f'=COUNTIF({L}{first+1}:{L}{r},"<0.5")', b.f["num"])
    ws.freeze_panes(first, 1)
    b.close()


def build(out):
    for fn in (skills_matrix, bench_tracker, utilisation_tracker, request_log, allocation_heatmap):
        fn(out)
