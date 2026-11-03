"""Single source of sample data shared by every template.

Everything here is fictional. Change it once and re-run build.py to
regenerate every document, spreadsheet and deck with consistent numbers.
"""
from datetime import date, timedelta

BRAND = "Sarath MS · sarathms.com"  # shown in every template footer
SAMPLE_NOTE = "Sample data. Fictional company and people. Replace before use."

ORG = "Halcyon Outfitters"      # fictional retailer
PROJECT = "Project Lighthouse"
PROJECT_FULL = "Project Lighthouse: Omnichannel Customer Platform"
PROGRAM = "Digital Commerce Transformation Program"
PROJECT_ID = "DCT-PRJ-014"
METHOD = "Hybrid (stage-gated governance, 2-week Scrum sprints for build)"

START = date(2026, 2, 2)
GO_LIVE = date(2026, 9, 28)
END = date(2026, 10, 30)
STATUS_DATE = date(2026, 6, 19)   # "today" in the sample status reports
BAC = 1_850_000
CONTINGENCY = 150_000
CURRENCY = "$"

PEOPLE = {
    "sponsor":  ("Priya Raman", "VP Digital, Executive Sponsor"),
    "program":  ("Sam Okafor", "Program Manager, DCT Program"),
    "delivery": ("Jordan Lee", "Delivery Manager"),
    "pm":       ("Alex Morgan", "Senior Project Manager"),
    "po":       ("Maria Santos", "Product Owner"),
    "tech":     ("Wei Chen", "Technical Lead / Architect"),
    "qa":       ("Daniel Kim", "QA Lead"),
    "finance":  ("Hannah Brooks", "Finance Business Partner"),
    "security": ("Omar Haddad", "Information Security Lead"),
    "stores":   ("Lucy Grant", "Head of Store Operations"),
    "service":  ("Ravi Patel", "Head of Customer Service"),
    "vendor":   ("Elena Petrova", "Engagement Lead, Brightpath Systems (SI partner)"),
    "ux":       ("Tomás Rivera", "UX Lead"),
    "data":     ("Aisha Khan", "Data & Analytics Lead"),
}

def name(k): return PEOPLE[k][0]
def role(k): return PEOPLE[k][1]

OBJECTIVES = [
    ("Single customer view", "Unify online, store and service data into one customer profile", "100% of active customers matched to one profile by go-live"),
    ("Order visibility", "Let customers and staff see any order across channels in real time", "Order status latency < 60 seconds"),
    ("Service efficiency", "Cut contact-centre handling time with a unified agent console", "Average handle time down 20% within 90 days of go-live"),
    ("Revenue", "Enable buy-online-pick-up-in-store (BOPIS) for all 120 stores", "BOPIS at 8% of online orders within 6 months"),
]

IN_SCOPE = [
    "Customer data platform (CDP) build and identity resolution",
    "Integration with e-commerce, POS (120 stores) and contact-centre CRM",
    "Unified agent console for 180 contact-centre agents",
    "BOPIS journey on web and mobile app",
    "Data migration of 2.4M customer records",
    "Training, change management and 4 weeks of hypercare",
]
OUT_SCOPE = [
    "Loyalty programme redesign (separate project: Loyalty 2.0)",
    "Replacement of store POS hardware",
    "International sites (UK, DE): planned for phase 2",
    "Marketing automation journeys beyond the 5 launch campaigns",
]

MILESTONES = [  # name, baseline, forecast/actual, status
    ("Project kickoff", date(2026, 2, 2), date(2026, 2, 2), "Complete"),
    ("Discovery complete", date(2026, 3, 6), date(2026, 3, 6), "Complete"),
    ("Solution design sign-off (Gate 2)", date(2026, 4, 3), date(2026, 4, 10), "Complete"),
    ("MVP build complete (Sprint 8)", date(2026, 6, 26), date(2026, 7, 10), "At risk"),
    ("System integration test complete", date(2026, 7, 31), date(2026, 8, 14), "At risk"),
    ("UAT sign-off (Gate 3)", date(2026, 8, 28), date(2026, 9, 4), "On track"),
    ("Go-live", date(2026, 9, 28), date(2026, 9, 28), "On track"),
    ("Hypercare exit and closure (Gate 4)", date(2026, 10, 30), date(2026, 10, 30), "On track"),
]

# WBS: id, name, owner key, start, end, pct complete, predecessor
def d(m, dd): return date(2026, m, dd)
WBS = [
    ("1", "Initiation", None, None, None, None, ""),
    ("1.1", "Project charter and business case approval", "pm", d(2, 2), d(2, 13), 100, ""),
    ("1.2", "Stakeholder mapping and kickoff", "pm", d(2, 2), d(2, 6), 100, ""),
    ("2", "Discovery", None, None, None, None, ""),
    ("2.1", "Current-state process and data assessment", "tech", d(2, 9), d(2, 27), 100, "1.2"),
    ("2.2", "Customer research and journey mapping", "ux", d(2, 9), d(3, 6), 100, "1.2"),
    ("2.3", "Vendor and platform selection", "pm", d(2, 16), d(3, 6), 100, "1.2"),
    ("3", "Design", None, None, None, None, ""),
    ("3.1", "Solution architecture and integration design", "tech", d(3, 9), d(4, 3), 100, "2.3"),
    ("3.2", "UX design and prototype testing", "ux", d(3, 9), d(4, 3), 100, "2.2"),
    ("3.3", "Security and privacy impact assessment", "security", d(3, 16), d(4, 10), 100, "3.1"),
    ("4", "Build (Sprints 1-8)", None, None, None, None, ""),
    ("4.1", "CDP and identity resolution", "tech", d(3, 9), d(5, 29), 90, "3.1"),
    ("4.2", "POS integration (120 stores)", "vendor", d(4, 6), d(6, 26), 55, "3.1"),
    ("4.3", "Agent console", "tech", d(4, 6), d(6, 26), 70, "3.2"),
    ("4.4", "BOPIS web and app journey", "tech", d(4, 20), d(7, 10), 50, "3.2"),
    ("4.5", "Data migration scripts and dry runs", "data", d(5, 4), d(7, 17), 40, "4.1"),
    ("5", "Test", None, None, None, None, ""),
    ("5.1", "System integration testing", "qa", d(6, 29), d(8, 14), 0, "4.2"),
    ("5.2", "Performance and security testing", "qa", d(7, 20), d(8, 14), 0, "5.1"),
    ("5.3", "User acceptance testing", "po", d(8, 17), d(9, 4), 0, "5.1"),
    ("6", "Deploy and adopt", None, None, None, None, ""),
    ("6.1", "Training (180 agents, 120 store leads)", "service", d(8, 24), d(9, 18), 0, "5.3"),
    ("6.2", "Cutover rehearsal and go-live", "tech", d(9, 7), d(9, 28), 0, "5.3"),
    ("6.3", "Hypercare", "delivery", d(9, 28), d(10, 23), 0, "6.2"),
    ("7", "Closure", None, None, None, None, ""),
    ("7.1", "Benefits baseline, lessons learned, closure report", "pm", d(10, 19), d(10, 30), 0, "6.3"),
]

# Cost / EVM (monthly, in dollars)
MONTHS = ["Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct"]
PV = [120_000, 160_000, 210_000, 240_000, 250_000, 260_000, 250_000, 230_000, 130_000]
EV = [115_000, 150_000, 200_000, 228_000, 236_000, None, None, None, None]
AC = [118_000, 172_000, 226_000, 251_000, 262_000, None, None, None, None]

BUDGET_LINES = [  # category, budget, actual to date, forecast at completion
    ("Internal labour", 520_000, 301_000, 548_000),
    ("SI partner (Brightpath Systems)", 690_000, 402_000, 742_000),
    ("Software licences (CDP, 3 years upfront yr 1)", 310_000, 210_000, 310_000),
    ("Cloud infrastructure", 95_000, 41_000, 101_000),
    ("Testing and security services", 85_000, 22_000, 88_000),
    ("Training and change management", 90_000, 18_000, 90_000),
    ("Travel and expenses", 25_000, 11_000, 24_000),
    ("Management reserve held by sponsor", 35_000, 24_000, 35_000),
]

# Sprints: name, start, committed pts, completed pts, scope added
SPRINTS = [
    ("Sprint 1", d(3, 9), 34, 28, 0),
    ("Sprint 2", d(3, 23), 36, 33, 2),
    ("Sprint 3", d(4, 6), 40, 38, 3),
    ("Sprint 4", d(4, 20), 42, 41, 1),
    ("Sprint 5", d(5, 4), 44, 39, 5),
    ("Sprint 6", d(5, 18), 44, 42, 2),
    ("Sprint 7", d(6, 1), 45, 37, 6),
]
CURRENT_SPRINT = ("Sprint 8", d(6, 15), 44)
BURNDOWN = [44, 44, 41, 38, 36, None, None, None, None, None, None]  # 10 working days, day 0..10

RISKS = [  # id, title, cause/effect, category, prob, impact, owner, response, mitigation, status, trend
    ("R-01", "POS integration slips further", "Legacy POS API rate limits found in Sprint 5; may delay SIT entry by 2+ weeks", "Schedule", 4, 4, "vendor", "Mitigate", "Add batch sync fallback; vendor adding 2 integration engineers from 22 Jun", "Open", "Rising"),
    ("R-02", "Data quality below match target", "Duplicate and incomplete records in legacy CRM reduce identity match rate", "Quality", 3, 4, "data", "Mitigate", "Run dedupe rules on dry-run 2; agree manual review queue for <5% unmatched", "Open", "Stable"),
    ("R-03", "Contact-centre adoption", "Peak season staffing leaves little time for agent training", "People", 3, 3, "service", "Mitigate", "Train super-users first; 45-min micro-modules; floor walkers week 1", "Open", "Stable"),
    ("R-04", "Budget overrun", "CPI at 0.90 driven by SI partner effort on POS work", "Cost", 4, 3, "pm", "Mitigate", "Change request CR-007 to rebaseline; vendor to absorb 50% of POS overrun under SOW clause 9", "Open", "Rising"),
    ("R-05", "Key person dependency", "Only one architect knows identity resolution design", "People", 2, 4, "tech", "Mitigate", "Pair with second engineer; record design walkthroughs", "Open", "Falling"),
    ("R-06", "Privacy regulator guidance change", "Pending guidance on consent for profile merging", "Compliance", 2, 5, "security", "Monitor", "Legal tracking; consent flags built configurable", "Open", "Stable"),
    ("R-07", "Peak trading freeze", "Change freeze from 1 Nov makes go-live slip costly", "Schedule", 2, 5, "delivery", "Mitigate", "Hold go-live 28 Sep with 4-week buffer before freeze", "Open", "Stable"),
    ("R-08", "Performance at peak load", "Black Friday volumes 6x normal", "Technical", 3, 4, "qa", "Mitigate", "Load test at 8x in August; auto-scaling policies agreed", "Open", "Stable"),
    ("R-09", "Licence true-up cost", "Profile volume may exceed licence tier", "Cost", 2, 2, "finance", "Accept", "Budget 5% contingency; review volumes at Gate 3", "Open", "Stable"),
    ("R-10", "Vendor resource churn", "SI partner rotated 2 developers in May", "People", 3, 2, "vendor", "Mitigate", "Named-resource clause; 2-week handover minimum", "Closed", "Falling"),
]
ISSUES = [  # id, title, impact, priority, owner, raised, due, status, resolution
    ("I-01", "POS API rate limit blocks real-time sync", "Order status latency 4-6 min vs 60s target", "High", "vendor", d(5, 12), d(6, 30), "In progress", "Batch fallback in build; vendor escalated to POS supplier"),
    ("I-02", "UAT environment not provisioned", "UAT prep blocked for 2 squads", "Medium", "tech", d(6, 3), d(6, 24), "In progress", "Cloud team ticket CLD-881 prioritised"),
    ("I-03", "Two open security findings from design review", "Gate 3 entry criteria at risk", "Medium", "security", d(5, 20), d(7, 3), "Open", "Fixes planned in Sprint 8"),
    ("I-04", "Store Ops SME availability", "BOPIS acceptance criteria not signed off", "Medium", "stores", d(5, 27), d(6, 19), "Resolved", "Two store managers seconded 2 days/week"),
    ("I-05", "Velocity dip in Sprint 7", "8 points carried over", "Low", "po", d(6, 12), d(6, 26), "Open", "Root cause: unplanned production support; agreed support rota"),
]
ASSUMPTIONS = [
    ("A-01", "POS supplier provides sandbox access for full SIT window", "vendor", "Validated"),
    ("A-02", "Contact-centre headcount stays at 180 through go-live", "service", "Open"),
    ("A-03", "CDP vendor meets 99.9% SLA in production", "tech", "Validated"),
    ("A-04", "Legal approves consent model before UAT", "security", "Open"),
    ("A-05", "No major e-commerce platform upgrade before October", "program", "Open"),
]
DEPENDENCIES = [  # id, description, type, from/to, owner, needed by, status
    ("D-01", "Payments Modernisation delivers tokenised card API", "Inbound", "Payments Modernisation", "program", d(7, 31), "On track"),
    ("D-02", "Loyalty 2.0 consumes unified customer ID", "Outbound", "Loyalty 2.0", "program", d(9, 30), "At risk"),
    ("D-03", "Cloud platform team provisions UAT and prod", "Inbound", "Cloud Platform team", "tech", d(6, 24), "Late"),
    ("D-04", "Store network upgrade at 14 legacy stores", "Inbound", "IT Infrastructure", "stores", d(8, 28), "On track"),
    ("D-05", "Data Platform Migration exposes customer events", "Inbound", "Data Platform Migration", "data", d(7, 17), "On track"),
]
DECISIONS = [  # id, decision, rationale, made by, date, impact
    ("DEC-01", "Select Brightpath Systems as SI partner", "Best score on capability and price (weighted 78/100)", "Steering Committee", d(3, 4), "Vendor onboarding from 9 Mar"),
    ("DEC-02", "Adopt hybrid delivery: stage gates plus Scrum build", "Governance needs gates; build needs iteration", "Sponsor", d(2, 10), "8 sprints planned"),
    ("DEC-03", "Defer UK and DE sites to phase 2", "Protects October go-live", "Steering Committee", d(4, 8), "Scope reduced; $120k avoided"),
    ("DEC-04", "Use batch sync fallback for 30 legacy stores", "POS API limits; keeps real-time for 90 stores", "Design Authority", d(6, 10), "Latency target met for 75% of stores at launch"),
    ("DEC-05", "Train super-users before general agents", "Peak staffing constraint", "Delivery Manager", d(6, 15), "Training plan v2"),
    ("DEC-06", "Raise CR-007 to rebaseline cost", "CPI below 0.95 threshold for 2 months", "Program Manager", d(6, 17), "Goes to SteerCo 24 Jun"),
]

STAKEHOLDERS = [  # key, dept, interest(1-5), influence(1-5), attitude, needs, engagement current->desired, freq
    ("sponsor", "Digital", 5, 5, "Champion", "Benefits on track; no surprises", "Leading", "Leading", "Weekly 1:1, monthly SteerCo"),
    ("program", "PMO", 5, 4, "Supporter", "Dependencies and program-level RAG", "Supportive", "Leading", "Weekly"),
    ("finance", "Finance", 3, 4, "Neutral", "Spend vs budget, capitalisation", "Neutral", "Supportive", "Monthly"),
    ("security", "InfoSec", 3, 5, "Neutral", "Privacy and security controls", "Neutral", "Supportive", "Fortnightly"),
    ("stores", "Store Operations", 4, 4, "Supporter", "Minimal disruption to stores", "Supportive", "Supportive", "Fortnightly"),
    ("service", "Customer Service", 5, 3, "Concerned", "Training time during peak", "Resistant", "Supportive", "Weekly"),
    ("vendor", "Brightpath Systems", 5, 3, "Supporter", "Clear backlog, timely decisions", "Supportive", "Supportive", "Daily"),
    ("data", "Data & Analytics", 4, 3, "Supporter", "Data model alignment", "Supportive", "Supportive", "Weekly"),
    ("po", "Digital Product", 5, 4, "Champion", "Customer outcomes", "Leading", "Leading", "Daily"),
    (None, "Store managers (120)", 3, 2, "Unaware", "What changes at the counter", "Unaware", "Supportive", "Monthly newsletter"),
    (None, "Contact-centre agents (180)", 4, 1, "Concerned", "Tools that make calls shorter", "Unaware", "Supportive", "Fortnightly huddles"),
]

RACI_ROLES = ["Sponsor", "Program Mgr", "Delivery Mgr", "Project Mgr", "Product Owner", "Tech Lead", "QA Lead", "SI Partner", "InfoSec", "Finance"]
RACI = [
    ("Approve business case and charter", "A", "C", "C", "R", "C", "C", "", "", "", "C"),
    ("Maintain project plan and schedule", "I", "C", "A", "R", "C", "C", "C", "C", "", ""),
    ("Prioritise product backlog", "I", "", "C", "C", "A/R", "C", "", "C", "", ""),
    ("Solution architecture", "", "I", "C", "I", "C", "A/R", "C", "R", "C", ""),
    ("Sprint delivery", "", "", "A", "C", "C", "R", "C", "R", "", ""),
    ("Test strategy and execution", "", "", "C", "I", "C", "C", "A/R", "R", "", ""),
    ("Security and privacy assessment", "I", "", "C", "C", "C", "R", "", "C", "A", ""),
    ("Budget tracking and forecasting", "I", "C", "A", "R", "", "", "", "", "", "C"),
    ("Change request approval (> $50k)", "A", "R", "C", "R", "C", "C", "", "", "", "C"),
    ("RAID management", "I", "C", "A", "R", "C", "C", "C", "C", "C", ""),
    ("Weekly status report", "I", "I", "A", "R", "C", "C", "C", "", "", ""),
    ("Go/no-go decision", "A", "R", "R", "R", "C", "C", "C", "C", "C", "I"),
    ("Training and adoption", "I", "", "A", "R", "C", "", "", "", "", ""),
    ("Benefits realisation tracking", "A", "R", "C", "R", "C", "", "", "", "", "C"),
]

COMMS = [  # communication, audience, purpose, format, frequency, owner, channel
    ("Weekly status report", "Sponsor, Program Mgr, workstream leads", "Progress, RAG, decisions needed", "1-page report", "Weekly (Fri)", "pm", "Email + SharePoint"),
    ("Steering Committee", "Sponsor, heads of Stores, Service, Finance, InfoSec", "Decisions, escalations, gate approvals", "Deck + minutes", "Monthly", "pm", "Meeting (60 min)"),
    ("Program sync", "Program Mgr, PMs of DCT projects", "Cross-project dependencies", "RAID review", "Weekly (Tue)", "program", "Meeting (30 min)"),
    ("Sprint review", "Product Owner, stakeholders, team", "Demo increment, collect feedback", "Live demo", "Bi-weekly", "po", "Meeting (60 min)"),
    ("Daily stand-up", "Delivery team", "Plan the day, surface blockers", "Board walk", "Daily", "delivery", "Teams (15 min)"),
    ("Design Authority", "Tech Lead, architects, InfoSec", "Technical decisions", "Decision log", "Fortnightly", "tech", "Meeting (45 min)"),
    ("Change network update", "Store managers, team leaders", "Upcoming changes, training dates", "Newsletter", "Monthly", "service", "Email + intranet"),
    ("Finance review", "Finance BP, Delivery Mgr", "Actuals, accruals, forecast", "Cost report", "Monthly (WD5)", "delivery", "Meeting (30 min)"),
]

CHANGES = [  # id, title, requested by, date, type, cost impact, schedule impact (days), status, decision date
    ("CR-001", "Add consent preference centre to scope", "security", d(3, 20), "Scope", 28_000, 0, "Approved", d(3, 27)),
    ("CR-002", "Defer UK and DE sites to phase 2", "sponsor", d(4, 2), "Scope", -120_000, -10, "Approved", d(4, 8)),
    ("CR-003", "Extend design phase by 1 week", "tech", d(3, 30), "Schedule", 15_000, 5, "Approved", d(4, 1)),
    ("CR-004", "Add Spanish language to agent console", "service", d(4, 22), "Scope", 18_000, 0, "Rejected", d(5, 6)),
    ("CR-005", "Batch sync fallback for legacy stores", "tech", d(6, 5), "Technical", 22_000, 0, "Approved", d(6, 10)),
    ("CR-006", "Additional load test cycle at 8x", "qa", d(6, 11), "Quality", 12_000, 0, "Approved", d(6, 17)),
    ("CR-007", "Rebaseline cost for POS integration overrun", "pm", d(6, 17), "Cost", 65_000, 14, "Pending SteerCo", None),
]

# Resource plan: role, name/vendor, rate per day, FTE by month Feb..Oct
RESOURCES = [
    ("Senior Project Manager", "Alex Morgan", 850, [1, 1, 1, 1, 1, 1, 1, 1, 1]),
    ("Product Owner", "Maria Santos", 800, [0.5, 1, 1, 1, 1, 1, 1, 1, 0.5]),
    ("Tech Lead / Architect", "Wei Chen", 950, [0.5, 1, 1, 1, 1, 1, 1, 1, 0.5]),
    ("UX Lead", "Tomás Rivera", 750, [0.5, 1, 1, 0.5, 0.5, 0.5, 0.2, 0.2, 0]),
    ("Data Engineer x2", "Internal", 700, [0, 1, 2, 2, 2, 2, 1.5, 1, 0.5]),
    ("SI developers", "Brightpath Systems", 650, [0, 2, 5, 6, 7, 7, 5, 3, 1]),
    ("QA engineers", "Brightpath Systems", 550, [0, 0.5, 1, 1.5, 2, 3, 3, 2, 0.5]),
    ("Business Analyst", "Internal", 650, [1, 1, 1, 1, 1, 1, 0.5, 0.5, 0]),
    ("Change and Training Lead", "Internal", 600, [0, 0.2, 0.2, 0.5, 0.5, 0.5, 1, 1, 0.5]),
    ("Security Analyst", "InfoSec (shared)", 800, [0, 0.2, 0.5, 0.2, 0.2, 0.5, 0.5, 0.2, 0]),
]
CAPACITY = [  # available FTE per role per month (to show over-allocation)
    [1] * 9, [1] * 9, [1] * 9, [1] * 9, [2] * 9, [6, 6, 6, 6, 6, 7, 7, 7, 7], [3] * 9, [1] * 9, [1] * 9, [0.3] * 9,
]

# Quality / delivery metrics, monthly Mar..Jun (+ targets)
QUALITY_MONTHS = ["Mar", "Apr", "May", "Jun"]
DEFECTS = {  # severity: found per month
    "Critical": [0, 1, 2, 1],
    "High": [2, 5, 8, 6],
    "Medium": [6, 12, 15, 11],
    "Low": [8, 10, 13, 9],
}
DEFECTS_CLOSED = [12, 24, 33, 30]
DELIVERY_METRICS = [  # metric, unit, target, Mar, Apr, May, Jun, direction (+ good when up)
    ("Deployment frequency (to test env)", "per week", 5, 2, 4, 5, 6, "+"),
    ("Lead time for changes", "days", 5, 9, 7, 6, 5.5, "-"),
    ("Change failure rate", "%", 15, 22, 18, 14, 12, "-"),
    ("Mean time to restore (test env)", "hours", 4, 9, 6, 5, 3.5, "-"),
    ("Automated test coverage", "%", 70, 35, 48, 58, 64, "+"),
    ("Test case pass rate", "%", 95, 81, 86, 90, 92, "+"),
    ("Escaped defects (found after sprint)", "count", 3, 6, 5, 4, 3, "-"),
    ("Sprint goal attainment", "%", 85, 82, 95, 89, 82, "+"),
]

PORTFOLIO = [  # project, PM, phase, RAG overall, schedule, cost, scope, budget, actual, pct complete, SPI, CPI, next milestone, date, open high risks
    ("Project Lighthouse (Omnichannel CX)", "Alex Morgan", "Build", "Amber", "Amber", "Amber", "Green", 1_850_000, 1_029_000, 50, 0.95, 0.90, "MVP build complete", d(7, 10), 3),
    ("Payments Modernisation", "Nadia Flores", "Test", "Green", "Green", "Green", "Green", 1_200_000, 840_000, 72, 1.02, 0.99, "PCI audit", d(7, 15), 1),
    ("Loyalty 2.0", "Chris Doyle", "Design", "Red", "Red", "Amber", "Amber", 950_000, 310_000, 28, 0.81, 0.93, "Design sign-off", d(7, 3), 4),
    ("Store Ops Mobile App", "Mei Tanaka", "Deploy", "Green", "Green", "Green", "Green", 600_000, 545_000, 91, 1.00, 1.01, "Rollout wave 3", d(6, 29), 0),
    ("Data Platform Migration", "Ben Adeyemi", "Build", "Amber", "Green", "Amber", "Amber", 1_400_000, 760_000, 49, 0.98, 0.91, "Customer events live", d(7, 17), 2),
]

LESSONS = [  # category, what happened, impact, recommendation, type (went well / improve)
    ("Vendor management", "Named-resource clause added after SI partner rotated developers in May", "2 weeks of lost velocity before clause", "Include named-resource and handover clauses in every SOW from day one", "Improve"),
    ("Technical discovery", "POS API rate limits found in Sprint 5, not discovery", "6-week integration slip, $65k overrun", "Run technical spikes against every legacy integration during discovery", "Improve"),
    ("Governance", "Hybrid model: gates for funding, sprints for build", "Sponsor confidence high; team kept agility", "Reuse the hybrid governance pack for DCT projects", "Went well"),
    ("Stakeholders", "Seconded store managers 2 days/week", "BOPIS criteria signed off in 1 week vs 4", "Secure SME secondments in the resource plan, not ad hoc", "Went well"),
    ("Change management", "Super-user model in contact centre", "Training completed despite peak staffing", "Start super-user recruitment at design phase", "Went well"),
    ("Reporting", "One RAID log shared across program", "Dependencies with Loyalty 2.0 seen 6 weeks early", "Make the shared RAID log the program standard", "Went well"),
    ("Estimation", "Data migration estimates assumed clean source data", "Dry run 1 match rate 78% vs 95% target", "Profile source data before estimating migration", "Improve"),
]


def workdays(a, b):
    n, cur = 0, a
    while cur <= b:
        if cur.weekday() < 5:
            n += 1
        cur += timedelta(days=1)
    return n


def money(v, k=False):
    if v is None:
        return ""
    if k:
        return f"{CURRENCY}{v/1000:,.0f}k"
    return f"{CURRENCY}{v:,.0f}"


def fmt_date(x):
    return x.strftime("%d %b %Y") if x else "TBC"
