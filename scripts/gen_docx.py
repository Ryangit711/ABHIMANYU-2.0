#!/usr/bin/env python3
"""Parametric DOCX generator — reads company fit map + SHOOT package, outputs tailored DOCX."""

import sys
import os
import json
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

ONEDRIVE = "/mnt/c/Users/owner/OneDrive/ABHIMANYU-2.0"
LINUX = "/home/aryan/opencode_test/ABHIMANYU-2.0"

NAME = "Aman Kumar"
PHONE = "+1 236-885-2285"
EMAIL = "amankumar7111@outlook.com"
LINKEDIN = "linkedin.com/in/aman1776"
LOCATION = "Vancouver, BC"

# Company-specific configs
CONFIG = {
    "Indeed": {
        "font": "Liberation Sans",
        "size": Pt(10),
        "header_size": Pt(12),
        "margins": Inches(0.75),
        "pages": 1,
        "ats_notes": "Indeed internal ATS — DOCX preferred, Liberation Sans, 0.75in margins"
    },
    "Methanex": {
        "font": "Calibri",
        "size": Pt(11),
        "header_size": Pt(13),
        "margins": Inches(0.75),
        "pages": 2,
        "ats_notes": "Methanex career portal — DOCX, Calibri 11pt, 2-page for Director level"
    },
    "Deloitte": {
        "font": "Calibri",
        "size": Pt(10),
        "header_size": Pt(12),
        "margins": Inches(0.75),
        "pages": 2,
        "ats_notes": "Deloitte Workday ATS — DOCX, Calibri 10pt"
    }
}

def set_margins(doc, margin):
    for section in doc.sections:
        section.top_margin = margin
        section.bottom_margin = margin
        section.left_margin = margin
        section.right_margin = margin

def add_contact(doc, config):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(NAME)
    run.font.name = config["font"]
    run.font.size = Pt(16)
    run.bold = True
    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run2 = p2.add_run(f"{PHONE} | {EMAIL} | {LINKEDIN} | {LOCATION}")
    run2.font.name = config["font"]
    run2.font.size = Pt(9)
    run2.font.color.rgb = RGBColor(80, 80, 80)

def add_section_header(doc, text, config):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(3)
    run = p.add_run(text.upper())
    run.font.name = config["font"]
    run.font.size = config["header_size"]
    run.bold = True
    pPr = p._p.get_or_add_pPr()
    pBdr = pPr.makeelement(qn('w:pBdr'), {})
    bottom = pBdr.makeelement(qn('w:bottom'), {
        qn('w:val'): 'single', qn('w:sz'): '4',
        qn('w:space'): '1', qn('w:color'): '000000',
    })
    pBdr.append(bottom)
    pPr.append(pBdr)

def add_body(doc, text, config, bold=False, italic=False, size=None, space_after=2):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(0)
    run = p.add_run(text)
    run.font.name = config["font"]
    run.font.size = size or config["size"]
    run.bold = bold
    run.italic = italic

def add_bullet(doc, text, config, bold_prefix=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.first_line_indent = Inches(-0.25)
    if bold_prefix:
        run_b = p.add_run(f"• {bold_prefix}")
        run_b.font.name = config["font"]
        run_b.font.size = config["size"]
        run_b.bold = True
        run = p.add_run(text)
        run.font.name = config["font"]
        run.font.size = config["size"]
    else:
        run = p.add_run(f"• {text}")
        run.font.name = config["font"]
        run.font.size = config["size"]

def generate(company):
    config = CONFIG.get(company, CONFIG["Methanex"])
    folder = f"{ONEDRIVE}/2026-06-21/{company}"
    lfolder = f"{LINUX}/2026-06-21/{company}"
    os.makedirs(folder, exist_ok=True)
    os.makedirs(lfolder, exist_ok=True)

    # --- RESUME ---
    doc = Document()
    set_margins(doc, config["margins"])
    add_contact(doc, config)

    add_section_header(doc, "Professional Summary", config)
    if company == "Methanex":
        add_body(doc,
            "Strategy and operations executive who built the strategic infrastructure for a multi-site "
            "organization from zero, scaling it from 3 to 70 employees across 32 locations and directing "
            "a $17M acquisition. Combines board-level strategic thinking with hands-on financial modelling, "
            "M&A execution, and cross-functional leadership. Equally comfortable leading an ELT strategy "
            "session, building a valuation model, or aligning diverse teams around a shared plan.", config)
    else:
        add_body(doc,
            "Operations executive who built multi-site operational infrastructure from scratch, "
            "scaling from 3 to 70 employees across 32 locations, then directed a $17M acquisition. "
            "Combines strategic thinking with execution.", config)

    add_section_header(doc, "Core Competencies", config)
    if company == "Methanex":
        add_body(doc,
            "Corporate Strategy & Planning  |  Financial Modelling & Valuation  |  M&A Execution & Integration  |  "
            "Board & Executive Communication  |  Cross-Functional Leadership  |  OKR & Performance Systems  |  "
            "Capital Allocation  |  Strategic Growth Initiatives", config, size=Pt(9.5))
    else:
        add_body(doc,
            "M&A Integration  |  Cross-Functional Program Management  |  Operational Infrastructure  |  "
            "Strategic Planning & OKRs  |  P&L Management  |  Board Reporting  |  Multi-Site Operations", config, size=Pt(9.5))

    add_section_header(doc, "Professional Experience", config)

    # SkyflyMD
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.space_before = Pt(4)
    run = p.add_run("SkyflyMD")
    run.font.name = config["font"]
    run.font.size = config["size"]
    run.bold = True
    run2 = p.add_run("  |  Director of Operations  |  Phoenix, AZ / Vancouver, BC  |  2017 – 2025")
    run2.font.name = config["font"]
    run2.font.size = config["size"]

    if company == "Methanex":
        add_body(doc,
            "Led strategy and operations for a multi-site healthcare group. Built the strategic planning "
            "process, financial infrastructure, and operational systems from zero.", config, italic=True, size=Pt(9.5))
        add_bullet(doc,
            " — built company-wide strategic planning framework across 5 annual cycles: board-level strategy "
            "sessions, departmental OKR cascades, quarterly performance reviews with executive leadership",
            config, bold_prefix="Strategic Planning & Execution")
        add_bullet(doc,
            " — multi-scenario P&L models, capital allocation frameworks, departmental budgets across "
            "12 departments, board-ready reporting templates",
            config, bold_prefix="Financial Modelling")
        add_bullet(doc,
            " — directed end-to-end $17M acquisition: 8 due diligence workstreams, Day 1 readiness, "
            "100% key talent retention, 90-day systems consolidation",
            config, bold_prefix="M&A & Integration")
        add_bullet(doc,
            " — organizational infrastructure for 70 employees across 5 clinic groups, 32 locations — "
            "hiring frameworks, training, quality standards, cross-border coordination",
            config, bold_prefix="Organizational Leadership")
    else:
        add_body(doc,
            "Directed end-to-end operations for a multi-site healthcare group. Served as the primary "
            "bridge between executive leadership and all operational teams.", config, italic=True, size=Pt(9.5))
        add_bullet(doc,
            " — 8 concurrent due diligence workstreams, integration playbook, Day 1/100 milestones, "
            "100% key talent retention through $17M transition",
            config, bold_prefix="Full-Cycle Acquisition Execution")

    # Earlier
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.space_before = Pt(6)
    run = p.add_run("Earlier Career")
    run.font.name = config["font"]
    run.font.size = config["size"]
    run.bold = True
    add_bullet(doc, "Digital Strategy Manager (2016–2018) — led digital strategy, campaign analytics, ROI measurement", config)
    add_bullet(doc, "Client Services Representative (2014–2016) — client escalations, complex issue resolution", config)

    # Education
    add_section_header(doc, "Education", config)
    add_body(doc, "Master of Business Administration (MBA)", config, bold=True, space_after=0)
    add_body(doc, "Post-Baccalaureate Diploma in Business Management — KPU, Surrey, BC", config, size=Pt(9), space_after=0)
    add_body(doc, "Bachelor of Science, Information Technology", config, size=Pt(9), space_after=0)

    # Technical Proficiency
    add_section_header(doc, "Technical Proficiency", config)
    if company == "Methanex":
        add_body(doc,
            "Financial Modelling & Analysis  |  Microsoft Excel (Advanced)  |  Google Workspace  |  "
            "OKR Frameworks  |  ERP Systems  |  CRM Platforms  |  Jira / Confluence  |  Data Visualization",
            config, size=Pt(9))
    else:
        add_body(doc,
            "Athenahealth  |  eClinicalWorks  |  CRM Platforms  |  Google Workspace  |  "
            "Financial Modeling  |  OKR Frameworks  |  Jira / Confluence",
            config, size=Pt(9))

    respath = os.path.join(folder, f"Aman_Kumar_{company}_Director_Strategy.docx" if company == "Methanex" else f"Aman_Kumar_{company}_SrMgr_Integration.docx")
    try:
        doc.save(respath)
    except PermissionError:
        respath = os.path.join(lfolder, os.path.basename(respath))
        doc.save(respath)
    doc.save(os.path.join(lfolder, os.path.basename(respath)))
    print(f"Resume: {respath}")

    # --- COVER LETTER ---
    doc = Document()
    set_margins(doc, config["margins"])

    add_body(doc, NAME, config, bold=True, space_after=0)
    add_body(doc, f"{PHONE} | {EMAIL} | {LINKEDIN}", config, size=Pt(9), space_after=0)
    add_body(doc, LOCATION, config, size=Pt(9), space_after=4)
    add_body(doc, "June 21, 2026", config, space_after=8)

    if company == "Methanex":
        add_body(doc, "Methanex Corporation", config, space_after=0)
        add_body(doc, "1800 Waterfront Centre, 200 Burrard Street", config, space_after=0)
        add_body(doc, "Vancouver, BC V6C 3M1", config, space_after=8)
        add_body(doc, "Re: Director, Strategy", config, bold=True, space_after=8)

        body = (
            "Dear Hiring Manager,\n\n"
            "Methanex is the world's largest methanol producer, navigating volatile commodity markets, "
            "the integration of a $2.05B acquisition, and a strategic shift toward low-carbon solutions. "
            "The Director, Strategy role sits at the center of these dynamics. This is exactly where I deliver the most value.\n\n"
            "I spent eight years building the strategic infrastructure of a multi-site organization from scratch. "
            "When I joined, there were 3 people and no playbook. When I left, it was 70 people across 32 locations "
            "with a $17M acquisition that I directed end-to-end. The strategic planning system I designed — annual "
            "strategy sessions cascading through quarterly OKRs with board-level reporting — gave executive leadership "
            "real-time visibility into execution across every location. The financial models I built governed resource "
            "allocation across 12 departments. The acquisition I directed involved 8 workstreams, diligence across "
            "finance, legal, and operations, and an integration that retained 100% of our key talent.\n\n"
            "What made this possible was not a pre-existing framework. I built it — the strategy cycle, the governance "
            "rhythms, the valuation models, the integration playbook — all from zero. I learned that strategy is not "
            "a document you produce once a year. It is a living process that must connect the Board room to the front "
            "line, and it requires someone who can operate at both altitudes without losing coherence.\n\n"
            "I understand Methanex operates in a different industry. But strategy is fractal — the core problems are "
            "the same: Where do we allocate capital? How do we grow? What risks do we manage? How do we align a global "
            "organization around a shared plan? I have solved these problems in my domain, and I am ready to solve them in yours.\n\n"
            "I would welcome the opportunity to discuss how my experience building strategic and financial infrastructure "
            "can support Methanex's next phase of global leadership.\n\n"
            "Best regards,\n"
            f"{NAME}\n{PHONE}\n{EMAIL}"
        )
    else:
        add_body(doc, "Indeed", config, space_after=0)
        add_body(doc, "Vancouver, BC", config, space_after=8)
        add_body(doc, "Re: Sr. Manager, Integration & Business Acceleration — Reference ID: 47053", config, bold=True, space_after=8)

        body = (
            "Dear Hiring Manager,\n\n"
            "Your mission is to help people get jobs. Mine is to build the operational infrastructure "
            "that makes organizations scalable, efficient, and ready for their next phase of growth.\n\n"
            "I joined SkyflyMD when it was 3 people in a single location. When I left, it was 70 people "
            "across 32 locations, operating with systems I designed from scratch. The defining moment of "
            "that journey was directing our $17M acquisition — structuring 8 concurrent due diligence "
            "workstreams across finance, legal, operations, and provider contracts. I built the integration "
            "playbook, tracked Day 1 readiness and Day 100 milestones, consolidated 8 separate operational "
            "systems into one unified platform, and retained 100% of our key talent through the transition.\n\n"
            "What made that possible was not a pre-existing framework. There was no playbook. I created it — "
            "the governance rhythms, the reporting cadences, the escalation paths, the decision-making "
            "frameworks — all from scratch, across 5 clinic groups operating under different state regulations.\n\n"
            "What drew me to Indeed is that you are data-driven without being jargon-heavy, and mission-focused "
            "without being sentimental. That is how I operate. Your 'job seeker first' value resonates because "
            "it mirrors how I have always made operational decisions — starting with the end-user and working backward.\n\n"
            "I am not looking for a role that requires a playbook to exist before I start. I am looking for "
            "one that needs a playbook written.\n\n"
            "I would welcome the opportunity to discuss how my experience building and integrating multi-site "
            "operations can support Indeed's continued growth through M&A. Thank you for your time and consideration.\n\n"
            "Best regards,\n"
            f"{NAME}\n{PHONE}\n{EMAIL}"
        )

    add_body(doc, body, config, space_after=0)

    clpath = os.path.join(folder, f"Cover_Letter_{company}_Director_Strategy.docx" if company == "Methanex" else f"Cover_Letter_{company}_SrMgr_Integration.docx")
    try:
        doc.save(clpath)
    except PermissionError:
        clpath = os.path.join(lfolder, os.path.basename(clpath))
        doc.save(clpath)
    doc.save(os.path.join(lfolder, os.path.basename(clpath)))
    print(f"Cover:   {clpath}")

    # --- CASE (Semantic Narrative) ---
    doc = Document()
    set_margins(doc, config["margins"])

    if company == "Methanex":
        # Title
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run("CASE — Aman Kumar × Methanex")
        run.font.name = config["font"]
        run.font.size = Pt(18)
        run.bold = True

        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run("The Strategist Who Built From Zero")
        run.font.name = config["font"]
        run.font.size = Pt(13)
        run.font.color.rgb = RGBColor(100, 100, 100)

        add_body(doc, "", config, space_after=4)

        # Section: The Situation
        add_section_header(doc, "The Situation", config)
        add_body(doc, (
            "Methanex is the world's largest methanol producer — 10.4M tonnes annually, approximately 20% of the "
            "internationally traded market — operating at the intersection of global commodity volatility, post-merger "
            "integration, and a generational energy transition. The $2.05B acquisition of OCI Global's international "
            "methanol business closed in June 2025, fundamentally reshaping Methanex's geographic and operational "
            "footprint. Low-carbon methanol — M100 as marine fuel, renewable methanol from circular sources, the "
            "Atlas joint venture on the US Gulf Coast — is no longer a long-dated possibility. It is a present-tense "
            "strategic imperative.\n\n"
            "This is the context in which the Director, Strategy operates. Not as a planner. As a navigator."
        ), config, size=Pt(10.5))

        # Section: The Candidate
        add_section_header(doc, "The Candidate", config)
        add_body(doc, (
            "Aman Kumar spent eight years doing exactly what Methanex needs now: building the strategic infrastructure "
            "of a complex, multi-site organization from zero — and then navigating it through a transformative acquisition.\n\n"
            "He did not inherit a strategic planning process. He designed one. He did not take over an existing financial "
            "model. He built it. He did not merely participate in an M&A transaction. He directed it — from first-day "
            "diligence through Day 1 readiness through 100-day integration, retaining 100% of key talent across five "
            "clinic groups and 32 locations."
        ), config, size=Pt(10.5))

        # Section: The Alignment
        add_section_header(doc, "The Alignment", config)
        add_bullet(doc,
            " — built the strategy cycle from scratch: annual ELT sessions, quarterly OKR cascades, board-ready reporting across 32 locations, 5 consecutive cycles", config,
            bold_prefix="Global Strategy Process")
        add_bullet(doc,
            " — multi-scenario P&L models across 12 departments, capital allocation frameworks, DCF and valuation analysis, board-level financial reporting", config,
            bold_prefix="Valuation & Financial Analysis")
        add_bullet(doc,
            " — directed full-cycle $17M acquisition: 8 diligence workstreams, Day 1/100 milestones, 8-system consolidation in 90 days, 100% talent retention", config,
            bold_prefix="M&A Execution")
        add_bullet(doc,
            " — coordinated 12 departments, 5 clinic groups, 32 locations — building governance rhythms, escalation protocols, decision-making frameworks", config,
            bold_prefix="Cross-Functional Leadership")
        add_bullet(doc,
            " — created board-level reporting, investor materials, executive presentations from zero — presented with the rigor Methanex's Board expects", config,
            bold_prefix="Board-Level Communication")

        # Section: The Semantic Fit
        add_section_header(doc, "The Semantic Fit", config)
        add_body(doc, (
            "Methanex operates on a strategic framework: Leadership, Low Cost, Operational Excellence. "
            "The culture is defined by The Power of Agility. The value system is Integrity, Trust, Respect, "
            "Professionalism — underwritten by Responsible Care.\n\n"
            "Aman's career is a case study in this exact operating model:"
        ), config, size=Pt(10.5))
        add_bullet(doc,
            "Built the strategic system that governed 70 people across 32 locations. Did not inherit leadership — created it.", config, bold_prefix="Leadership")
        add_bullet(doc,
            "Managed P&L across 12 departments. Built the financial models that optimized resource allocation. Every dollar had a decision behind it.", config, bold_prefix="Low Cost")
        add_bullet(doc,
            "Designed governance rhythms, hiring frameworks, training programs, quality standards. Built the machine that ran without him.", config, bold_prefix="Operational Excellence")
        add_bullet(doc,
            "Navigated a 3-person startup through growth to a $17M exit. When the acquisition hit, structured 8 workstreams in days.", config, bold_prefix="Power of Agility")
        add_bullet(doc,
            "Coordinated 5 clinic groups, 12 departments, 32 locations — many operating independently before his systems brought them together.", config, bold_prefix="One Team")

        # Section: The Opportunity
        add_section_header(doc, "The Opportunity", config)
        add_body(doc, (
            "Methanex is 1,700 people globally, approximately 150 in Vancouver. The Director, Strategy sits in "
            "that Vancouver HQ, serving as the connective tissue between the Board of Directors, the Executive "
            "Leadership Team, and the operational reality of a global methanol business navigating integration, "
            "volatility, and transition.\n\n"
            "Aman has done exactly this — at smaller scale, in a different industry — with a clarity and rigor "
            "that suggest something deeper than domain experience. He is not a strategist who needs to learn "
            "execution. He is an executive who happens to call himself a strategist because that is where the "
            "intellectual challenge lives.\n\n"
            "Strategy is fractal. The questions are the same at every scale: Where do we allocate capital? How "
            "do we grow? What risks do we need to manage? How do we align a global organization around a shared "
            "plan? Aman has answered these questions in the arena. He is ready to answer them at Methanex's scale."
        ), config, size=Pt(10.5))

        # Footer
        add_body(doc, "", config, space_after=4)
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run("—")
        run.font.name = config["font"]
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(150, 150, 150)
        add_body(doc, (
            "This document is not a resume. A resume is a record of what you have done. "
            "This is a case for who you are, and why that identity was built for this moment at this company."
        ), config, italic=True, size=Pt(9), space_after=0)

    casepath = os.path.join(folder, f"Case_{company}_Director_Strategy.docx" if company == "Methanex" else f"Case_{company}_SrMgr_Integration.docx")
    try:
        doc.save(casepath)
    except PermissionError:
        casepath = os.path.join(lfolder, os.path.basename(casepath))
        doc.save(casepath)
    doc.save(os.path.join(lfolder, os.path.basename(casepath)))
    print(f"Case:    {casepath}")
    print("Done.")

if __name__ == "__main__":
    company = sys.argv[1] if len(sys.argv) > 1 else "Methanex"
    generate(company)
