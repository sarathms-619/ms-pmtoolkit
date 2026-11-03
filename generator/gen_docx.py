import os
from datetime import date

import data as D
from docx_helpers import (new_doc, doc_control, h, p, bullets, guidance, table,
                          kv_table, signature_block, MUTED)
from data import d, name, role, money, fmt_date


def evm_now():
    pv = sum(D.PV[:5]); ev = sum(D.EV[:5]); ac = sum(D.AC[:5])
    return pv, ev, ac, ev / pv, ev / ac


# ---------------------------------------------------------------- charter
def project_charter(out):
    doc = new_doc("Project Charter", "Initiation")
    doc_control(doc, "1.0", d(2, 13), "pm", "sponsor", "Approved")
    guidance(doc, "The charter formally authorises the project and gives the PM authority to use resources. Keep it to 3-5 pages. "
                  "Get it signed before any spend beyond discovery.")
    h(doc, "1. Purpose and background")
    p(doc, f"{D.ORG} sells through 120 stores, a website, a mobile app and a 180-seat contact centre. Each channel holds its own "
           "customer and order data. Customers who buy online and call the contact centre are often asked to repeat details, and "
           "store staff cannot see web orders. Customer satisfaction for cross-channel journeys is 61 (NPS +4) against 74 (NPS +31) "
           "for single-channel journeys.")
    p(doc, f"{D.PROJECT} will build one customer and order view across all channels, and launch buy-online-pick-up-in-store (BOPIS).")
    h(doc, "2. Objectives and success criteria")
    table(doc, ["Objective", "Description", "Success measure"], D.OBJECTIVES, widths=(3.5, 7, 6.5))
    h(doc, "3. Scope")
    h(doc, "In scope", 2); bullets(doc, D.IN_SCOPE)
    h(doc, "Out of scope", 2); bullets(doc, D.OUT_SCOPE)
    h(doc, "4. Key deliverables")
    bullets(doc, ["Customer data platform with identity resolution", "Integration layer to e-commerce, POS and CRM",
                  "Agent console", "BOPIS journey (web and app)", "Migrated customer data (2.4M records)",
                  "Training materials and trained users", "Operational runbooks and support handover"])
    h(doc, "5. Milestones")
    table(doc, ["Milestone", "Target date"], [(m[0], fmt_date(m[1])) for m in D.MILESTONES], widths=(11, 5))
    h(doc, "6. Budget summary")
    kv_table(doc, [("Approved budget (BAC)", money(D.BAC)), ("Contingency (held by sponsor)", money(D.CONTINGENCY)),
                   ("Total funding envelope", money(D.BAC + D.CONTINGENCY)), ("Funding source", "FY26 Digital capex, DCT program"),
                   ("Change authority", "PM up to $10k; Program Mgr up to $50k; SteerCo above $50k")])
    h(doc, "7. High-level risks")
    table(doc, ["Risk", "Response"], [
        ("Legacy POS integration complexity", "Technical spike in discovery; SI partner with POS experience"),
        ("Customer data quality", "Data profiling and two migration dry runs"),
        ("Adoption in contact centre during busy periods", "Super-user model and short training modules"),
        ("Go-live inside peak trading freeze", "Go-live 28 Sep with 4-week buffer before 1 Nov freeze")], widths=(7, 10))
    h(doc, "8. Assumptions and constraints")
    bullets(doc, ["POS supplier provides sandbox access for the full test window",
                  "Change freeze from 1 November to 10 January (constraint)",
                  "Contact-centre headcount stays at 180 through go-live",
                  "Data must stay in-region (constraint)"])
    h(doc, "9. Governance and roles")
    table(doc, ["Role", "Name", "Responsibility"], [
        ("Executive Sponsor", name("sponsor"), "Owns business case, chairs SteerCo, approves gates"),
        ("Program Manager", name("program"), "Program alignment, cross-project dependencies"),
        ("Delivery Manager", name("delivery"), "Delivery assurance, resourcing, vendor performance"),
        ("Senior Project Manager", name("pm"), "Day-to-day management, plan, RAID, reporting"),
        ("Product Owner", name("po"), "Backlog, acceptance, benefits"),
        ("Technical Lead", name("tech"), "Architecture and technical quality")], widths=(4, 3.5, 9.5))
    p(doc, "Stage gates: Gate 1 Charter (Feb) · Gate 2 Design sign-off (Apr) · Gate 3 Go-live readiness (Sep) · Gate 4 Closure (Oct).", italic=True)
    h(doc, "10. Approval")
    signature_block(doc, ["sponsor", "program", "finance", "pm"])
    doc.save(os.path.join(out, "project-charter.docx"))


# ---------------------------------------------------------------- business case
def business_case(out):
    doc = new_doc("Business Case", "Initiation")
    doc_control(doc, "1.2", d(1, 23), "pm", "sponsor", "Approved by Investment Committee")
    guidance(doc, "Lead with the decision you need and the numbers. Executives read the summary and the financials; "
                  "everything else is evidence. Show at least three options, including 'do nothing'.")
    h(doc, "1. Executive summary")
    p(doc, f"We request {money(D.BAC + D.CONTINGENCY)} (including {money(D.CONTINGENCY)} contingency) to build a unified customer "
           "and order platform. The investment pays back in 26 months, returns a 3-year NPV of $2.4M at an 8% discount rate, and "
           "removes the top cause of customer complaints (no visibility of orders across channels).")
    h(doc, "2. Problem statement")
    bullets(doc, ["34% of contact-centre calls are 'where is my order' queries that agents cannot answer without switching between 3 systems",
                  "Average handle time is 7.8 minutes against an industry benchmark of 5.5",
                  "Store staff cannot see or fulfil web orders, so BOPIS is not possible",
                  "Marketing cannot target customers across channels: 4 separate customer IDs per customer on average"])
    h(doc, "3. Options considered")
    table(doc, ["Option", "Description", "Cost (3 yr)", "Benefit (3 yr)", "Recommendation"], [
        ("A. Do nothing", "Keep current systems", "$0", "$0 (complaints rise)", "Not recommended"),
        ("B. Point fixes", "Order lookup widget in CRM only", "$420k", "$1.1M", "Not recommended"),
        ("C. Unified platform", "CDP, integration layer, agent console, BOPIS", "$2.6M", "$5.6M", "Recommended"),
        ("D. Full re-platform", "Replace e-commerce and POS as well", "$7.9M", "$7.2M", "Not recommended")],
        widths=(3, 5.5, 2.5, 3, 3), font=8.5)
    h(doc, "4. Financial analysis (Option C)")
    table(doc, ["", "Year 0", "Year 1", "Year 2", "Year 3", "Total"], [
        ("Capital cost", "$1,850k", "$0", "$0", "$0", "$1,850k"),
        ("Run cost (licences, cloud, support)", "$0", "$250k", "$250k", "$250k", "$750k"),
        ("Benefit: contact-centre efficiency", "$0", "$540k", "$720k", "$740k", "$2,000k"),
        ("Benefit: BOPIS incremental margin", "$0", "$480k", "$900k", "$1,100k", "$2,480k"),
        ("Benefit: marketing conversion uplift", "$0", "$220k", "$400k", "$500k", "$1,120k"),
        ("Net cash flow", "-$1,850k", "$990k", "$1,770k", "$2,090k", "$3,000k")],
        widths=(5.5, 2, 2, 2, 2, 2.2), font=8.5, align_right=(1, 2, 3, 4, 5))
    kv_table(doc, [("NPV (8%, 3 years)", "$2.4M"), ("IRR", "61%"), ("Payback", "26 months from project start"),
                   ("Sensitivity", "Still NPV-positive if benefits are 40% lower or costs 50% higher")])
    h(doc, "5. Benefits realisation")
    table(doc, ["Benefit", "Measure", "Baseline", "Target", "Owner", "When"], [
        ("Faster service", "Average handle time", "7.8 min", "6.2 min", name("service"), "Go-live + 90 days"),
        ("BOPIS revenue", "% online orders via BOPIS", "0%", "8%", name("stores"), "Go-live + 6 months"),
        ("Customer satisfaction", "Cross-channel NPS", "+4", "+20", name("po"), "Go-live + 6 months"),
        ("Single view", "Customers with one profile", "0%", "100%", name("data"), "Go-live")],
        widths=(3, 3.5, 2, 2, 3, 3), font=8.5)
    h(doc, "6. Strategic alignment")
    bullets(doc, [("FY26 strategy pillar 2", "Seamless customer experience"),
                  ("DCT Program", "Lighthouse provides the customer ID that Loyalty 2.0 and Data Platform Migration depend on")])
    h(doc, "7. Key risks")
    bullets(doc, ["Legacy POS integration complexity", "Data quality affects identity matching", "Adoption during busy periods"])
    h(doc, "8. Recommendation and decision required")
    p(doc, "Approve Option C, funding of $2.0M (including contingency), and release of $180k for discovery immediately.", bold=True)
    signature_block(doc, ["sponsor", "finance"])
    doc.save(os.path.join(out, "business-case.docx"))


# ---------------------------------------------------------------- PMP
def project_management_plan(out):
    doc = new_doc("Project Management Plan", "Planning")
    doc_control(doc, "2.0", d(4, 10), "pm", "delivery", "Baselined at Gate 2")
    guidance(doc, "The PMP says how the project will be run. Link to the detailed logs (RAID, schedule, budget) rather "
                  "than copying them in. Re-baseline only through approved change requests.")
    sections = [
        ("1. Delivery approach", [
            ("Method", D.METHOD),
            ("Lifecycle", "Initiation > Discovery > Design (Gate 2) > Build in 8 sprints > Test > Deploy (Gate 3) > Hypercare > Closure (Gate 4)"),
            ("Definition of done", "Code reviewed, automated tests pass, security scan clean, PO accepted, docs updated")]),
        ("2. Scope management", [
            ("Baseline", "Charter v1.0 plus approved CRs; product backlog in Jira (LH project)"),
            ("Change control", "All scope, cost >$10k or schedule >5 days changes need a CR; see Change Log"),
            ("Acceptance", "Sprint-level acceptance by PO; release-level by UAT sign-off")]),
        ("3. Schedule management", [
            ("Baseline", "Integrated schedule v2.0 (Gate 2)"),
            ("Tolerance", "Milestone slip > 10 working days escalates to SteerCo"),
            ("Tracking", "Weekly milestone forecast; sprint burndown; SPI monthly")]),
        ("4. Cost management", [
            ("Budget", f"{money(D.BAC)} BAC plus {money(D.CONTINGENCY)} sponsor contingency"),
            ("Tolerance", "CPI or SPI < 0.95 for 2 consecutive months triggers re-forecast and CR"),
            ("Reporting", "Monthly EVM report with Finance on working day 5")]),
        ("5. Quality management", [
            ("Standards", "Test strategy v1.1; 70% automated coverage; zero open critical/high defects for go-live"),
            ("Reviews", "Design Authority fortnightly; security review per release"),
            ("Metrics", "Defect density, escaped defects, test pass rate, change failure rate")]),
        ("6. Risk management", [
            ("Process", "Identify > assess (5x5) > respond > monitor in weekly RAID review"),
            ("Escalation", "Score 15+ to Program Manager within 2 days; score 20+ to SteerCo"),
            ("Ownership", "Every risk has a named owner and next review date")]),
        ("7. Resource management", [
            ("Team", "14 FTE peak (internal 6, SI partner 8)"),
            ("Onboarding", "Onboarding checklist, access within 3 days"),
            ("Capacity", "Monthly capacity review with Delivery Manager")]),
        ("8. Communications", [
            ("Plan", "See Communication Plan workbook"),
            ("Status", "Weekly report (Friday); monthly SteerCo deck"),
            ("Tools", "Jira, Confluence, Teams, SharePoint")]),
        ("9. Procurement and vendor management", [
            ("Contract", "Brightpath Systems SOW (time and materials, capped)"),
            ("Performance", "Monthly vendor scorecard: velocity, quality, staffing"),
            ("Clauses", "Named resources, 2-week handover, 50% overrun share on fixed scope items")]),
    ]
    for title, rows in sections:
        h(doc, title)
        kv_table(doc, rows)
    h(doc, "10. Governance calendar")
    table(doc, ["Forum", "Chair", "Frequency", "Inputs", "Outputs"], [
        ("Steering Committee", name("sponsor"), "Monthly", "SteerCo deck, CRs", "Decisions, gate approvals"),
        ("Program sync", name("program"), "Weekly", "RAID, dependency log", "Escalations"),
        ("Design Authority", name("tech"), "Fortnightly", "Design proposals", "Decision log"),
        ("Sprint review", name("po"), "Bi-weekly", "Increment", "Accepted stories, feedback")], widths=(3.5, 3, 2.5, 4, 4))
    doc.save(os.path.join(out, "project-management-plan.docx"))


# ---------------------------------------------------------------- weekly status
def weekly_status_report(out):
    pv, ev, ac, spi, cpi = evm_now()
    doc = new_doc("Weekly Status Report", "Monitoring & Reporting")
    kv_table(doc, [("Reporting period", "15 Jun 2026 to 19 Jun 2026 (week 20 of 39)"),
                   ("Prepared by", f"{name('pm')}, {role('pm')}"),
                   ("Distribution", f"{name('sponsor')}, {name('program')}, {name('delivery')}, workstream leads")])
    h(doc, "Overall status")
    table(doc, ["Overall", "Schedule", "Cost", "Scope", "Quality", "Resources"],
          [("Amber", "Amber", "Amber", "Green", "Green", "Amber")], rag_cols=range(6), font=10)
    p(doc, "Summary: ", bold=True).add_run(
        "Build is 50% complete. POS integration is 2 weeks behind because of legacy API rate limits; a batch fallback for 30 stores "
        "was approved (DEC-04). Cost is 10% over earned value; CR-007 to rebaseline goes to SteerCo on 24 Jun. "
        "Go-live date of 28 Sep holds, with buffer reduced from 4 weeks to 2.").bold = False
    guidance(doc, "Write the summary for someone who reads nothing else. Say what changed since last week, why, and what you need.")
    h(doc, "Key metrics")
    table(doc, ["Metric", "This week", "Last week", "Target", "Trend"], [
        ("% complete (earned)", "50%", "47%", "53%", "Behind"),
        ("SPI", f"{spi:.2f}", "0.96", "≥ 0.95", "Down"),
        ("CPI", f"{cpi:.2f}", "0.91", "≥ 0.95", "Down"),
        ("Spend to date", money(ac), "$968,000", money(pv) + " planned", "Over"),
        ("Sprint 8 burndown", "36 of 44 pts left (day 4)", "n/a", "31 pts left", "Behind"),
        ("Open high/critical defects", "7", "9", "< 10", "Better")], widths=(4.5, 3.5, 3, 3, 2.5))
    h(doc, "Accomplishments this week")
    bullets(doc, ["Sprint 7 review: agent console order timeline demoed to 12 contact-centre team leaders",
                  "Identity resolution dry run 2: match rate 91% (up from 78%)",
                  "Batch sync fallback design approved by Design Authority",
                  "Store Ops SMEs seconded; BOPIS acceptance criteria signed off"])
    h(doc, "Planned next week")
    bullets(doc, ["SteerCo 24 Jun: decision on CR-007 (cost rebaseline +$65k)",
                  "Complete Sprint 8; start SIT readiness review",
                  "UAT environment provisioned (dependency D-03)",
                  "Agent super-user training wave 1 (20 agents)"])
    h(doc, "Milestones")
    table(doc, ["Milestone", "Baseline", "Forecast", "Status"],
          [(m[0], fmt_date(m[1]), fmt_date(m[2]), m[3]) for m in D.MILESTONES], widths=(7.5, 3, 3, 3), rag_cols=(3,))
    h(doc, "Top risks and issues")
    table(doc, ["ID", "Description", "Score / Priority", "Owner", "Action"], [
        (r[0], r[1], f"{r[4]*r[5]} ({r[4]}x{r[5]})", name(r[6]), r[8]) for r in D.RISKS[:2]] + [
        (r[0], r[1], f"{r[4]*r[5]} ({r[4]}x{r[5]})", name(r[6]), r[8]) for r in D.RISKS[3:4]] + [
        (i[0], i[1], i[3], name(i[4]), i[8]) for i in D.ISSUES[:2]],
        widths=(1.3, 4.5, 2.2, 2.7, 6.3), font=8.5)
    h(doc, "Decisions and support needed")
    table(doc, ["Ask", "From", "By"], [
        ("Approve CR-007 cost rebaseline of $65k (vendor absorbs 50% of overrun)", "Steering Committee", "24 Jun"),
        ("Escalate UAT environment ticket CLD-881 with Cloud Platform team", name("program"), "22 Jun"),
        ("Confirm 2 extra integration engineers from Brightpath", name("delivery"), "22 Jun")], widths=(10, 4, 2.5))
    doc.save(os.path.join(out, "weekly-status-report.docx"))


# ---------------------------------------------------------------- change request
def change_request(out):
    doc = new_doc("Change Request CR-007", "Change Control")
    kv_table(doc, [("CR number", "CR-007"), ("Title", "Rebaseline cost for POS integration overrun"),
                   ("Requested by", f"{name('pm')}, {role('pm')}"), ("Date raised", fmt_date(d(6, 17))),
                   ("Change type", "Cost and schedule"), ("Priority", "High"),
                   ("Decision forum", "Steering Committee, 24 Jun 2026"), ("Status", "Pending SteerCo")])
    guidance(doc, "One CR per change. Quantify impact on all four constraints (scope, time, cost, quality) even if zero, "
                  "and always show the alternatives you rejected.")
    h(doc, "1. Description of change")
    p(doc, "Increase the approved budget by $65,000 and move the SIT-complete milestone by 10 working days (31 Jul to 14 Aug) "
           "to cover extra integration effort for the legacy POS estate. Go-live date stays 28 Sep.")
    h(doc, "2. Reason for change")
    bullets(doc, ["Legacy POS API rate limits found in Sprint 5 (issue I-01) were not visible in discovery",
                  "SI partner effort on POS integration is 38% over estimate (420 vs 305 days)",
                  "CPI has been below the 0.95 tolerance for two consecutive months (0.92 May, 0.90 Jun)"])
    h(doc, "3. Impact assessment")
    table(doc, ["Area", "Impact", "Detail"], [
        ("Scope", "None", "Batch fallback for 30 stores already approved under CR-005"),
        ("Schedule", "+10 days", "SIT complete moves to 14 Aug; UAT window shortened by 1 week; go-live unchanged"),
        ("Cost", "+$65,000", "Total $130k overrun; Brightpath absorbs $65k under SOW clause 9.2"),
        ("Quality", "Low risk", "UAT compressed; mitigated by earlier test-case readiness and extra QA engineer"),
        ("Benefits", "None", "BOPIS available in all 120 stores at go-live; 30 stores at 15-min latency for 6 weeks"),
        ("Other projects", "Low", "Loyalty 2.0 dependency D-02 unchanged")], widths=(3, 3, 10.5))
    h(doc, "4. Options")
    table(doc, ["Option", "Cost", "Schedule", "Recommendation"], [
        ("1. Approve CR as proposed", "+$65k", "Go-live holds", "Recommended"),
        ("2. Reduce BOPIS to 90 stores at launch", "+$20k", "Go-live holds", "Not recommended: lose $140k year-1 margin"),
        ("3. Move go-live to 26 Oct", "+$95k", "+4 weeks", "Not recommended: inside peak-trading risk window")],
        widths=(6, 2.5, 3, 5))
    h(doc, "5. Funding source")
    p(doc, "Sponsor contingency ($150k; $0 used to date). After approval, contingency remaining: $85k.")
    h(doc, "6. Decision")
    table(doc, ["Decision", "Approved by", "Date", "Conditions"], [("", "", "", "")], widths=(3.5, 4.5, 2.5, 6))
    doc.save(os.path.join(out, "change-request-form.docx"))


# ---------------------------------------------------------------- SteerCo minutes
def steerco_minutes(out):
    doc = new_doc("Steering Committee Minutes", "Governance")
    kv_table(doc, [("Meeting", "Project Lighthouse Steering Committee #5"), ("Date and time", "24 Jun 2026, 10:00-11:00"),
                   ("Chair", name("sponsor")), ("Minutes by", name("pm")),
                   ("Attendees", ", ".join(name(k) for k in ["sponsor", "program", "delivery", "pm", "finance", "stores", "service", "security", "vendor"])),
                   ("Apologies", name("data"))])
    guidance(doc, "Record decisions and actions, not a transcript. Send within 24 hours. Every action has one owner and a date.")
    h(doc, "1. Agenda")
    bullets(doc, ["Actions from SteerCo #4", "Status and health (Amber)", "CR-007 cost rebaseline (decision)",
                  "Top risks and dependencies", "Gate 3 readiness criteria (for information)", "AOB"], style="List Number")
    h(doc, "2. Discussion summary")
    bullets(doc, [("Status", "PM presented Amber status: SPI 0.95, CPI 0.90. Committee accepted the root cause (POS API limits)."),
                  ("CR-007", "Finance confirmed contingency covers the change. Brightpath confirmed absorbing $65k under SOW clause 9.2."),
                  ("Risks", "Head of Customer Service raised training capacity concerns during busy periods; super-user approach endorsed."),
                  ("Dependencies", "Program Manager flagged Loyalty 2.0 (Red) may need the unified customer ID earlier; to assess.")])
    h(doc, "3. Decisions")
    table(doc, ["ID", "Decision", "Made by"], [
        ("SC5-D1", "CR-007 approved: +$65k budget from contingency; SIT-complete moves to 14 Aug; go-live 28 Sep confirmed", "Sponsor"),
        ("SC5-D2", "Gate 3 entry criteria approved as presented", "Committee"),
        ("SC5-D3", "Monthly vendor scorecard to be added to SteerCo pack", "Sponsor")], widths=(2, 11, 3.5))
    h(doc, "4. Actions")
    table(doc, ["#", "Action", "Owner", "Due", "Status"], [
        ("1", "Update cost baseline and schedule v2.1 after CR-007", name("pm"), "01 Jul 2026", "Open"),
        ("2", "Confirm start of 2 extra integration engineers", name("vendor"), "26 Jun 2026", "Open"),
        ("3", "Assess Loyalty 2.0 request for early customer ID", name("program"), "08 Jul 2026", "Open"),
        ("4", "Share agent training plan v2 with team leaders", name("service"), "03 Jul 2026", "Open"),
        ("5", "Escalate UAT environment (CLD-881)", name("delivery"), "25 Jun 2026", "Closed")],
        widths=(0.8, 8, 3.3, 2.7, 1.8), rag_cols=(4,))
    h(doc, "5. Next meeting")
    p(doc, "SteerCo #6: 22 Jul 2026, 10:00. Focus: SIT progress and go-live readiness.")
    doc.save(os.path.join(out, "steering-committee-minutes.docx"))


# ---------------------------------------------------------------- lessons learned
def lessons_learned(out):
    doc = new_doc("Lessons Learned Report", "Closure")
    doc_control(doc, "1.0", d(10, 27), "pm", "program", "Final")
    guidance(doc, "Collect lessons through the whole project, not only at the end. Each lesson needs a concrete recommendation "
                  "and an owner who will put it into the PMO playbook.")
    h(doc, "1. How we gathered lessons")
    p(doc, "Retrospectives from 9 sprints, a 90-minute closure workshop with 16 participants (21 Oct), and a survey of "
           "stakeholders (24 responses, 71% response rate).")
    h(doc, "2. Summary")
    kv_table(doc, [("What went well (top 3)", "Hybrid governance; SME secondments; shared program RAID log"),
                   ("What to improve (top 3)", "Technical spikes in discovery; vendor contract clauses; data profiling before estimating"),
                   ("Team survey: would work this way again", "88% agree")])
    h(doc, "3. Lessons register")
    table(doc, ["#", "Category", "What happened", "Impact", "Recommendation", "Type"],
          [(i + 1, *l) for i, l in enumerate(D.LESSONS)], widths=(0.7, 2.4, 4, 3.2, 4.5, 1.8), font=8.5)
    h(doc, "4. Actions to embed lessons")
    table(doc, ["Action", "Owner", "Due"], [
        ("Add 'legacy integration spike' to discovery checklist", name("program"), "30 Nov 2026"),
        ("Update SOW template with named-resource and handover clauses", name("delivery"), "15 Nov 2026"),
        ("Publish hybrid governance pack on PMO site", name("pm"), "15 Nov 2026")], widths=(10, 4, 2.5))
    doc.save(os.path.join(out, "lessons-learned-report.docx"))


# ---------------------------------------------------------------- closure report
def closure_report(out):
    doc = new_doc("Project Closure Report", "Closure")
    doc_control(doc, "1.0", d(10, 30), "pm", "sponsor", "Approved at Gate 4")
    guidance(doc, "Compare final results to the baseline, not to your latest forecast. Hand over open items and "
                  "benefits tracking to named owners before the team disbands.")
    h(doc, "1. Summary")
    p(doc, "Project Lighthouse went live on 28 Sep 2026 as planned, in all 120 stores and the contact centre. Final cost was "
           "$1,912,000 against the revised budget of $1,915,000 (original $1,850,000 plus CR-007). Hypercare closed on 23 Oct "
           "with no open critical defects.")
    h(doc, "2. Performance against baseline")
    table(doc, ["Measure", "Baseline", "Actual", "Variance", "Result"], [
        ("Go-live date", "28 Sep 2026", "28 Sep 2026", "0 days", "Met"),
        ("Budget", "$1,850,000", "$1,912,000", "+3.4%", "Partially met"),
        ("Scope", "Charter v1.0", "Delivered + CR-001; UK/DE deferred (CR-002)", "Approved changes", "Met"),
        ("Quality: critical defects at go-live", "0", "0", "-", "Met"),
        ("Identity match rate", "100%", "97.8% auto + manual queue", "-2.2%", "Partially met")],
        widths=(4.5, 3, 4, 2.5, 2.5), rag_cols=(4,))
    h(doc, "3. Objectives and early benefits")
    table(doc, ["Objective", "Target", "Status at closure", "Result"], [
        ("Single customer view", "100% matched", "97.8% (manual review for remainder)", "Partially met"),
        ("Order visibility", "< 60 s latency", "90 stores real-time; 30 stores 15 min until Dec", "Partially met"),
        ("Service efficiency", "AHT -20% by Jan 2027", "-11% after 4 weeks", "On track"),
        ("BOPIS", "8% of online orders by Mar 2027", "3.1% after 4 weeks", "On track")],
        widths=(4, 4, 6, 2.5), rag_cols=(3,))
    h(doc, "4. Deliverables handed over")
    table(doc, ["Deliverable", "Received by", "Date accepted"], [
        ("Customer data platform and runbooks", "Digital Platforms Ops", "23 Oct 2026"),
        ("Agent console and knowledge articles", "Customer Service", "16 Oct 2026"),
        ("BOPIS store procedures", "Store Operations", "09 Oct 2026"),
        ("Benefits tracking dashboard", "Digital PMO", "30 Oct 2026")], widths=(7, 5, 4))
    h(doc, "5. Open items transferred")
    table(doc, ["Item", "Owner", "Due"], [
        ("Move 30 batch-sync stores to real-time after POS upgrade", name("tech"), "15 Dec 2026"),
        ("Clear manual identity review queue (52k records)", name("data"), "30 Nov 2026"),
        ("Benefits reviews at 90 days and 6 months", name("po"), "Jan and Apr 2027")], widths=(9, 4, 3.5))
    h(doc, "6. Financial closure")
    kv_table(doc, [("Purchase orders closed", "Yes, 4 of 4"), ("Final vendor invoice", "Received and approved 28 Oct"),
                   ("Capitalised", "$1,540,000"), ("Contingency returned", "$85,000")])
    h(doc, "7. Approval to close")
    signature_block(doc, ["sponsor", "program", "finance", "pm"])
    doc.save(os.path.join(out, "project-closure-report.docx"))


# ---------------------------------------------------------------- UAT sign-off
def uat_signoff(out):
    doc = new_doc("UAT Sign-off Certificate", "Testing & Acceptance")
    kv_table(doc, [("Release", "Lighthouse Release 1.0"), ("UAT window", "17 Aug 2026 to 04 Sep 2026"),
                   ("Environment", "UAT-2 (production-like)"), ("Test lead", name("qa")), ("Business owner", name("po"))])
    guidance(doc, "Sign-off is a business decision. State exactly what was tested, what is still open, and the conditions "
                  "attached to acceptance.")
    h(doc, "1. Test execution summary")
    table(doc, ["Area", "Test cases", "Passed", "Failed", "Blocked", "Pass rate"], [
        ("Customer profile and identity", 64, 62, 2, 0, "97%"),
        ("Agent console", 88, 86, 2, 0, "98%"),
        ("BOPIS web and app", 72, 70, 1, 1, "97%"),
        ("Store order fulfilment", 41, 41, 0, 0, "100%"),
        ("Reporting and data", 25, 24, 1, 0, "96%"),
        ("Total", 290, 283, 6, 1, "97.6%")], widths=(5.5, 2.2, 2, 2, 2, 2.3), align_right=(1, 2, 3, 4, 5))
    h(doc, "2. Open defects at sign-off")
    table(doc, ["ID", "Summary", "Severity", "Workaround", "Fix by"], [
        ("LH-1182", "Pick-up notification text truncated on small Android screens", "Low", "Text still readable in app", "Release 1.0.1"),
        ("LH-1190", "Agent console export misses time zone in CSV", "Medium", "Manual note in export", "Release 1.0.1"),
        ("LH-1201", "Duplicate profile shown for 0.3% of test customers", "Medium", "Manual merge queue", "Before go-live")],
        widths=(2, 6.5, 2, 4, 2.5))
    h(doc, "3. Acceptance criteria")
    table(doc, ["Criterion", "Met?"], [
        ("No open critical or high defects", "Yes"), ("Pass rate ≥ 95%", "Yes"),
        ("All BOPIS end-to-end journeys pass in 3 pilot stores", "Yes"),
        ("Performance test passed at 8x load", "Yes"), ("Security findings closed", "Yes")], widths=(13, 3.5), rag_cols=(1,))
    h(doc, "4. Decision")
    p(doc, "The business accepts Release 1.0 for production, on condition that LH-1201 is fixed and retested before cutover.", bold=True)
    signature_block(doc, ["po", "service", "stores", "qa"])
    doc.save(os.path.join(out, "uat-signoff-certificate.docx"))


# ---------------------------------------------------------------- Go/no-go
def go_no_go(out):
    doc = new_doc("Go/No-Go Readiness Checklist", "Deployment")
    kv_table(doc, [("Release", "Lighthouse Release 1.0"), ("Decision meeting", "25 Sep 2026, 16:00"),
                   ("Planned go-live", "28 Sep 2026, 05:00 (cutover window 22:00 Sat to 05:00 Mon)"),
                   ("Decision owner", name("sponsor"))])
    guidance(doc, "Agree the criteria at least 4 weeks before go-live so the meeting is a check, not a debate. "
                  "Any 'No' on a mandatory item means no-go unless the sponsor accepts the risk in writing.")
    groups = [
        ("Product and quality", [("UAT signed off with conditions met", "Yes", name("po")),
                                 ("Zero open critical/high defects", "Yes", name("qa")),
                                 ("Performance test passed at 8x load", "Yes", name("qa")),
                                 ("Security penetration test findings closed", "Yes", name("security"))]),
        ("Operations", [("Runbooks reviewed by Ops", "Yes", name("tech")), ("Monitoring and alerts live", "Yes", name("tech")),
                        ("Support rota for hypercare (24x7 week 1)", "Yes", name("delivery")),
                        ("Rollback plan rehearsed (2 dry runs)", "Yes", name("tech"))]),
        ("People and business", [("180 agents trained (≥ 95%)", "Yes", name("service")),
                                 ("120 store leads trained", "Yes", name("stores")),
                                 ("Customer comms approved", "Yes", name("po")),
                                 ("No conflicting business events in go-live week", "Yes", name("program"))]),
        ("Data", [("Final migration dry run within tolerance (≥ 97% match)", "Yes", name("data")),
                  ("Data reconciliation sign-off", "No", name("data"))]),
    ]
    for g, items in groups:
        h(doc, g, 2)
        table(doc, ["Criterion", "Ready?", "Owner", "Evidence"], [(c, r, o, "Link") for c, r, o in items],
              widths=(8.5, 1.8, 3.5, 2.7), rag_cols=(1,))
    h(doc, "Decision")
    kv_table(doc, [("Outcome", "GO with condition"),
                   ("Condition", "Data reconciliation sign-off by 27 Sep 12:00, else cutover moves 1 week"),
                   ("Approved by", f"{name('sponsor')}, 25 Sep 2026")])
    doc.save(os.path.join(out, "go-no-go-checklist.docx"))


def build(out):
    for fn in (project_charter, business_case, project_management_plan, weekly_status_report, change_request,
               steerco_minutes, lessons_learned, closure_report, uat_signoff, go_no_go):
        fn(out)
