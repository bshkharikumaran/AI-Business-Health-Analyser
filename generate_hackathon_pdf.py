"""
Script to generate an Executive-Grade, High-Aesthetic Hackathon Presentation Overview PDF
for Vyapaar Pulse AI (AI-Powered Business Health Analyser & Autonomous MSME Co-Pilot).
"""
import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

PDF_OUTPUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Vyapaar_Pulse_AI_Hackathon_Overview.pdf")


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas for adding running headers and 'Page X of Y' footers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Header (pages 2+)
        if self._pageNumber > 1:
            self.drawString(40, 762, "VYAPAAR PULSE AI — Executive Hackathon Overview & Solution Architecture")
            self.drawRightString(572, 762, "CONFIDENTIAL & PROPRIETARY")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.75)
            self.line(40, 756, 572, 756)

        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.75)
        self.line(40, 42, 572, 42)
        self.drawString(40, 30, "Vyapaar Pulse AI | Autonomous Multilingual Co-Pilot for Indian MSMEs")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(572, 30, page_str)
        self.restoreState()


def build_pdf():
    doc = SimpleDocTemplate(
        PDF_OUTPUT_PATH,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=48,
        bottomMargin=52
    )

    styles = getSampleStyleSheet()

    # Custom Color Palette
    PRIMARY = colors.HexColor("#0F172A")       # Slate 900
    ACCENT_GREEN = colors.HexColor("#059669")  # Emerald 600
    ACCENT_BLUE = colors.HexColor("#2563EB")   # Blue 600
    ACCENT_PURPLE = colors.HexColor("#7C3AED") # Purple 600
    ACCENT_AMBER = colors.HexColor("#D97706")  # Amber 600
    TEXT_DARK = colors.HexColor("#1E293B")     # Slate 800
    TEXT_MUTED = colors.HexColor("#64748B")    # Slate 500
    BG_LIGHT = colors.HexColor("#F8FAFC")      # Slate 50
    BORDER_LIGHT = colors.HexColor("#E2E8F0")  # Slate 200

    # Custom Typography Styles
    styles.add(ParagraphStyle(
        "CoverTag",
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=11,
        textColor=ACCENT_GREEN,
        spaceAfter=4,
        textTransform="uppercase"
    ))

    styles.add(ParagraphStyle(
        "CoverTitle",
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=28,
        textColor=PRIMARY,
        spaceAfter=6
    ))

    styles.add(ParagraphStyle(
        "CoverSubtitle",
        fontName="Helvetica",
        fontSize=12,
        leading=16,
        textColor=TEXT_MUTED,
        spaceAfter=14
    ))

    styles.add(ParagraphStyle(
        "SectionHeading",
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=PRIMARY,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        "SubSectionHeading",
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=14,
        textColor=ACCENT_BLUE,
        spaceBefore=6,
        spaceAfter=4,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        "BodyDark",
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=TEXT_DARK,
        spaceAfter=5
    ))

    styles.add(ParagraphStyle(
        "BodyDarkBold",
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=13,
        textColor=TEXT_DARK
    ))

    styles.add(ParagraphStyle(
        "CalloutText",
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=TEXT_DARK
    ))

    styles.add(ParagraphStyle(
        "TableHead",
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    ))

    styles.add(ParagraphStyle(
        "TableCell",
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        textColor=TEXT_DARK
    ))

    styles.add(ParagraphStyle(
        "TableCellBold",
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=11,
        textColor=TEXT_DARK
    ))

    styles.add(ParagraphStyle(
        "PillBadge",
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=9,
        textColor=ACCENT_GREEN
    ))

    story = []

    # =========================================================================
    # PAGE 1: TITLE, EXECUTIVE SUMMARY & THE 4 INNOVATION PILLARS
    # =========================================================================
    story.append(Paragraph("★ HACKATHON PRESENTATION WHITEPAPER & ARCHITECTURE", styles["CoverTag"]))
    story.append(Paragraph("Vyapaar Pulse AI: Autonomous MSME Co-Pilot", styles["CoverTitle"]))
    story.append(Paragraph(
        "An Intelligent Multilingual Voice Assistant, Real-Time WhatsApp Operations Engine, "
        "and Government Subsidy Matcher designed for 63+ Million Indian Enterprises.",
        styles["CoverSubtitle"]
    ))

    # Meta Info Bar Table
    meta_data = [
        [
            Paragraph("<b>Target Audience:</b> Micro, Small & Medium Enterprises (MSMEs)", styles["TableCell"]),
            Paragraph("<b>Stack:</b> Python Flask · Voice AI · Firebase · Vanilla JS", styles["TableCell"]),
            Paragraph("<b>Languages:</b> Tamil, Hindi, Telugu, Kannada, Mal, Eng", styles["TableCell"])
        ]
    ]
    meta_table = Table(meta_data, colWidths=[180, 180, 172])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BG_LIGHT),
        ('BOX', (0, 0), (-1, -1), 1, BORDER_LIGHT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # Executive Summary Box
    exec_summary_text = (
        "<b>Executive Summary:</b> Indian MSMEs contribute 30% to GDP and 45% to exports, yet <b>over 80% struggle "
        "with operational blind spots</b> — complicated analytics software, language barriers, critical stockouts, "
        "unpaid invoices, and a lack of awareness of government subsidies (e.g., PMEGP 35% margin money, CGTMSE collateral-free "
        "loans, Tamil Nadu NEEDS). <b>Vyapaar Pulse AI</b> transforms enterprise decision-making into natural conversational voice "
        "in Indian regional languages, dispatches automated operational alerts directly to WhatsApp, and auto-matches business "
        "parameters with central and state subsidy programs to unlock massive non-repayable capital."
    )
    exec_box = Table([[Paragraph(exec_summary_text, styles["CalloutText"])]], colWidths=[532])
    exec_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EFF6FF")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#BFDBFE")),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(exec_box)
    story.append(Spacer(1, 10))

    # The 4 Core Innovation Pillars
    story.append(Paragraph("The Four Core Innovation Pillars", styles["SectionHeading"]))

    pillars_data = [
        [
            Paragraph("<b>1. Multilingual Voice AI Copilot</b>", styles["SubSectionHeading"]),
            Paragraph("<b>2. Automated WhatsApp Ops Center</b>", styles["SubSectionHeading"])
        ],
        [
            Paragraph(
                "• <b>Regional Speech In & Out:</b> Native Tamil, Hindi, Telugu, Kannada, Malayalam, and English audio synthesis.<br/>"
                "• <b>Fact-Based Intelligence:</b> Answers exact revenue, top margin products, low stock items, and customer churn from live DB.<br/>"
                "• <b>Hands-Free Operation:</b> Store owners can ask voice questions on the go without typing or reading dashboards.",
                styles["TableCell"]
            ),
            Paragraph(
                "• <b>Instant Threshold Triggers:</b> Stockout risk &gt;90%, customer sentiment drops, revenue milestones delivered instantly.<br/>"
                "• <b>Interactive 5G Phone Simulator:</b> Live interactive smartphone mockup rendering bidirectional chat simulations.<br/>"
                "• <b>AI Marketing Generator:</b> Generates festival promo copy in regional languages dispatched directly to buyers.",
                styles["TableCell"]
            )
        ],
        [
            Paragraph("<b>3. Govt Schemes Matcher & Comparator</b>", styles["SubSectionHeading"]),
            Paragraph("<b>4. Intelligent Predictive Business Engine</b>", styles["SubSectionHeading"])
        ],
        [
            Paragraph(
                "• <b>Multi-Factor Match Engine:</b> Compares category, turnover, state &amp; inclusivity against PMEGP, CGTMSE, NEEDS, MUDRA.<br/>"
                "• <b>Project Subsidy Simulator:</b> Calculates exact ₹ grant vs bank loan vs owner equity for capital expansion.<br/>"
                "• <b>Side-by-Side Matrix:</b> 1-click comparison of collateral, subsidies, and 1-click official WhatsApp scheme dispatch.",
                styles["TableCell"]
            ),
            Paragraph(
                "• <b>Working Capital &amp; Runway:</b> Tracks DSCR, debt ratio, and inventory reorder points (EOQ).<br/>"
                "• <b>Customer Churn Scoring:</b> Identifies high-risk customer accounts (e.g. CUST-903 with 74% risk) before they drop.<br/>"
                "• <b>Zero-Friction Ingestion:</b> Auto-imputes missing data, removes duplicates, and supports CSV/Excel datasets.",
                styles["TableCell"]
            )
        ]
    ]

    pillars_table = Table(pillars_data, colWidths=[261, 261])
    pillars_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 1), BG_LIGHT),
        ('BACKGROUND', (1, 0), (1, 1), BG_LIGHT),
        ('BACKGROUND', (0, 2), (0, 3), BG_LIGHT),
        ('BACKGROUND', (1, 2), (1, 3), BG_LIGHT),
        ('BOX', (0, 0), (0, 1), 1, BORDER_LIGHT),
        ('BOX', (1, 0), (1, 1), 1, BORDER_LIGHT),
        ('BOX', (0, 2), (0, 3), 1, BORDER_LIGHT),
        ('BOX', (1, 2), (1, 3), 1, BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(pillars_table)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: GOVERNMENT SCHEMES & SUBSIDY COMPARATOR DEEP DIVE
    # =========================================================================
    story.append(Paragraph("🏛️ Flagship Innovation: Government Schemes Matcher & Subsidy Comparator", styles["SectionHeading"]))
    story.append(Paragraph(
        "A game-changing capability that bridges the massive gap between government MSME subsidy funds and small business owners. "
        "The engine analyzes user turnover, category, state jurisdiction, and ownership attributes (e.g., Women/SC/ST/Rural) to rank "
        "eligible schemes and compute exact non-repayable grants.",
        styles["BodyDark"]
    ))
    story.append(Spacer(1, 4))

    # Schemes Comparison Matrix Table
    schemes_table_data = [
        [
            Paragraph("Scheme Name", styles["TableHead"]),
            Paragraph("Authority", styles["TableHead"]),
            Paragraph("Subsidy %", styles["TableHead"]),
            Paragraph("Max Cap", styles["TableHead"]),
            Paragraph("Collateral Req.", styles["TableHead"]),
            Paragraph("Key Enterprise Benefit", styles["TableHead"])
        ],
        [
            Paragraph("<b>PMEGP</b><br/>Prime Minister Employment Gen.", styles["TableCellBold"]),
            Paragraph("KVIC / MoMSME", styles["TableCell"]),
            Paragraph("<b>15% – 35%</b>", styles["TableCellBold"]),
            Paragraph("₹50.0 L", styles["TableCell"]),
            Paragraph("Zero Collateral", styles["TableCell"]),
            Paragraph("Up to 35% non-repayable capital subsidy for new projects &amp; machinery.", styles["TableCell"])
        ],
        [
            Paragraph("<b>CGTMSE</b><br/>Credit Guarantee Trust", styles["TableCellBold"]),
            Paragraph("SIDBI / MSME", styles["TableCell"]),
            Paragraph("Credit Cover", styles["TableCell"]),
            Paragraph("<b>₹5.00 Cr</b>", styles["TableCellBold"]),
            Paragraph("100% Free", styles["TableCell"]),
            Paragraph("85% sovereign bank loan guarantee with zero personal collateral.", styles["TableCell"])
        ],
        [
            Paragraph("<b>TN NEEDS</b><br/>New Entrepreneur Scheme", styles["TableCellBold"]),
            Paragraph("Govt of Tamil Nadu", styles["TableCell"]),
            Paragraph("<b>25% + 3%</b>", styles["TableCellBold"]),
            Paragraph("₹75.0 L", styles["TableCell"]),
            Paragraph("CGTMSE Cover", styles["TableCell"]),
            Paragraph("State capital grant of 25% plus 3% interest rebate on bank loans.", styles["TableCell"])
        ],
        [
            Paragraph("<b>PMMY MUDRA</b><br/>Shishu / Kishore / Tarun", styles["TableCellBold"]),
            Paragraph("Ministry of Finance", styles["TableCell"]),
            Paragraph("Micro Credit", styles["TableCell"]),
            Paragraph("₹10.0 L", styles["TableCell"]),
            Paragraph("Zero Collateral", styles["TableCell"]),
            Paragraph("Fast-track collateral-free working capital micro-loans.", styles["TableCell"])
        ],
        [
            Paragraph("<b>PM Vishwakarma</b><br/>Artisans &amp; Craftspeople", styles["TableCellBold"]),
            Paragraph("Ministry of MSME", styles["TableCell"]),
            Paragraph("₹15k + 5% Int", styles["TableCell"]),
            Paragraph("₹3.0 L", styles["TableCell"]),
            Paragraph("Zero Collateral", styles["TableCell"]),
            Paragraph("₹15,000 modern toolkit grant + 5% subsidized fixed interest rate.", styles["TableCell"])
        ],
        [
            Paragraph("<b>ZED Certification</b><br/>Zero Defect Zero Effect", styles["TableCellBold"]),
            Paragraph("QCI / MoMSME", styles["TableCell"]),
            Paragraph("<b>50% – 80%</b>", styles["TableCellBold"]),
            Paragraph("₹5.0 L", styles["TableCell"]),
            Paragraph("Direct Grant", styles["TableCell"]),
            Paragraph("80% direct subsidy on green certification &amp; clean tech audits.", styles["TableCell"])
        ],
        [
            Paragraph("<b>TReDS Platform</b><br/>Invoice Discounting", styles["TableCellBold"]),
            Paragraph("Reserve Bank of India", styles["TableCell"]),
            Paragraph("Cash Advance", styles["TableCell"]),
            Paragraph("₹2.50 Cr", styles["TableCell"]),
            Paragraph("Non-Recourse", styles["TableCell"]),
            Paragraph("Liquidates unpaid 60–90 day corporate buyer invoices within 48h.", styles["TableCell"])
        ]
    ]

    schemes_table = Table(schemes_table_data, colWidths=[90, 80, 58, 52, 70, 182])
    schemes_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(schemes_table)
    story.append(Spacer(1, 10))

    # Project Subsidy Simulation Example Card
    story.append(Paragraph("Simulated Project Subsidy Breakdown (Example: ₹25 Lakhs Expansion Project)", styles["SubSectionHeading"]))

    sim_data = [
        [
            Paragraph("<b>Component</b>", styles["TableHead"]),
            Paragraph("<b>Percentage Share</b>", styles["TableHead"]),
            Paragraph("<b>Amount (₹ Lakhs)</b>", styles["TableHead"]),
            Paragraph("<b>Financial Significance</b>", styles["TableHead"])
        ],
        [
            Paragraph("<b>🟢 Direct Government Subsidy</b>", styles["TableCellBold"]),
            Paragraph("<b>35.0%</b>", styles["TableCellBold"]),
            Paragraph("<b>₹8.75 Lakhs</b>", styles["TableCellBold"]),
            Paragraph("Non-repayable direct margin money capital grant from KVIC/MoMSME.", styles["TableCell"])
        ],
        [
            Paragraph("<b>🔵 Bank Term Loan (CGTMSE)</b>", styles["TableCellBold"]),
            Paragraph("60.0%", styles["TableCell"]),
            Paragraph("₹15.00 Lakhs", styles["TableCell"]),
            Paragraph("Low-interest term loan with zero personal collateral requirement.", styles["TableCell"])
        ],
        [
            Paragraph("<b>🟡 Owner Equity Margin</b>", styles["TableCellBold"]),
            Paragraph("5.0%", styles["TableCell"]),
            Paragraph("₹1.25 Lakhs", styles["TableCell"]),
            Paragraph("Minimal initial capital commitment required from entrepreneur.", styles["TableCell"])
        ],
        [
            Paragraph("<b>✨ Annual Bank Interest Saved</b>", styles["TableCellBold"]),
            Paragraph("9.5% Bank Rate", styles["TableCell"]),
            Paragraph("<b>~₹83,125 / year</b>", styles["TableCellBold"]),
            Paragraph("Compound recurring cash flow savings directly boosting profitability.", styles["TableCell"])
        ]
    ]

    sim_table = Table(sim_data, colWidths=[130, 90, 95, 217])
    sim_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), ACCENT_GREEN),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(sim_table)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: TECHNICAL ARCHITECTURE & FULL PLATFORM WORKFLOW
    # =========================================================================
    story.append(Paragraph("⚙️ System Architecture & Technology Stack", styles["SectionHeading"]))
    story.append(Paragraph(
        "Vyapaar Pulse AI is engineered with a modular, lightweight, high-performance architecture "
        "designed to run seamlessly on both desktop workstations and mobile browsers.",
        styles["BodyDark"]
    ))
    story.append(Spacer(1, 4))

    arch_data = [
        [
            Paragraph("<b>Layer</b>", styles["TableHead"]),
            Paragraph("<b>Technology</b>", styles["TableHead"]),
            Paragraph("<b>Core Role & Capabilities</b>", styles["TableHead"])
        ],
        [
            Paragraph("<b>Frontend UI / UX</b>", styles["TableCellBold"]),
            Paragraph("HTML5 · Modern CSS (Glassmorphism) · Vanilla JavaScript", styles["TableCell"]),
            Paragraph("Zero-framework overhead, ultra-fast &lt;100ms render speeds, responsive 5G smartphone simulator, dark/light theme engine.", styles["TableCell"])
        ],
        [
            Paragraph("<b>Application Server</b>", styles["TableCellBold"]),
            Paragraph("Python 3.13 · Flask Framework · REST APIs", styles["TableCell"]),
            Paragraph("Handles authenticated user sessions, telemetry computation, scheme matching logic, and multi-channel API routing.", styles["TableCell"])
        ],
        [
            Paragraph("<b>AI & Speech Layer</b>", styles["TableCellBold"]),
            Paragraph("Multilingual Semantic Intent Engine + Google Gemini 2.5 + Edge TTS", styles["TableCell"]),
            Paragraph("Speech recognition and audio generation in Tamil, Hindi, Telugu, Kannada, Malayalam, English with direct fact-grounded DB retrieval.", styles["TableCell"])
        ],
        [
            Paragraph("<b>Data & Storage</b>", styles["TableCellBold"]),
            Paragraph("Firebase Realtime DB + Local JSON + Mock Mode Toggle", styles["TableCell"]),
            Paragraph("Synchronous cloud persistence, instant mock-to-uploaded custom dataset toggle, and historical WhatsApp alert logging.", styles["TableCell"])
        ],
        [
            Paragraph("<b>Analytics Engine</b>", styles["TableCellBold"]),
            Paragraph("Predictive Analytics + Scikit-Learn + Chart.js Visuals", styles["TableCell"]),
            Paragraph("Computes ARR growth, cash runway, customer churn risk %, EOQ inventory reorder points, and automated data remediation.", styles["TableCell"])
        ]
    ]

    arch_table = Table(arch_data, colWidths=[95, 130, 307])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(arch_table)
    story.append(Spacer(1, 10))

    # Architecture Flow Box
    story.append(Paragraph("End-to-End Operational Pipeline", styles["SubSectionHeading"]))
    flow_steps = [
        [
            Paragraph("<b>1. Input Ingestion</b>", styles["TableCellBold"]),
            Paragraph("Voice Speech / Text Prompt / CSV File Upload / Profile Setup", styles["TableCell"])
        ],
        [
            Paragraph("<b>2. AI Intent & Extraction</b>", styles["TableCellBold"]),
            Paragraph("Language detection (ta, hi, te, kn, ml, en) -> Semantic slot extraction", styles["TableCell"])
        ],
        [
            Paragraph("<b>3. Analytics & Matching</b>", styles["TableCellBold"]),
            Paragraph("DB query -> Churn score calculation / 9-scheme multi-factor evaluation", styles["TableCell"])
        ],
        [
            Paragraph("<b>4. Multi-Channel Output</b>", styles["TableCellBold"]),
            Paragraph("Native Voice Audio + UI View Navigation + WhatsApp Immediate Dispatch", styles["TableCell"])
        ]
    ]
    flow_table = Table(flow_steps, colWidths=[140, 392])
    flow_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BG_LIGHT),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(flow_table)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: BUSINESS IMPACT, MARKET OPPORTUNITY & HACKATHON DEMO GUIDE
    # =========================================================================
    story.append(Paragraph("🚀 Market Opportunity & 3-Minute Hackathon Demo Script", styles["SectionHeading"]))
    story.append(Paragraph(
        "Structured talking points and demonstration sequences designed for presenting Vyapaar Pulse AI "
        "to hackathon judges and domain experts.",
        styles["BodyDark"]
    ))
    story.append(Spacer(1, 4))

    # Business Impact Grid
    impact_data = [
        [
            Paragraph("<b>Market Size</b><br/><font size=11 color='#059669'><b>63.3 Million MSMEs</b></font><br/>Contributing $1.6T to India's GDP", styles["TableCell"]),
            Paragraph("<b>Time Saved</b><br/><font size=11 color='#2563EB'><b>85% Faster Insights</b></font><br/>Voice Q&A replaces hours of spreadsheet analysis", styles["TableCell"]),
            Paragraph("<b>Capital Unlocked</b><br/><font size=11 color='#D97706'><b>₹12.5L+ Per Unit</b></font><br/>Direct capital grants matched automatically", styles["TableCell"])
        ]
    ]
    impact_table = Table(impact_data, colWidths=[177, 177, 178])
    impact_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BG_LIGHT),
        ('BOX', (0, 0), (-1, -1), 1, BORDER_LIGHT),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(impact_table)
    story.append(Spacer(1, 10))

    # 3-Minute Presentation Demo Walkthrough for Judges
    story.append(Paragraph("Step-by-Step 3-Minute Pitch Walkthrough", styles["SubSectionHeading"]))

    demo_steps_data = [
        [
            Paragraph("Time", styles["TableHead"]),
            Paragraph("Demo Action", styles["TableHead"]),
            Paragraph("Live Screen / Feature", styles["TableHead"]),
            Paragraph("Judge Impact & Value Proposition", styles["TableHead"])
        ],
        [
            Paragraph("<b>0:00 – 0:45</b>", styles["TableCellBold"]),
            Paragraph("<b>1. Authentication & Onboarding</b><br/>Sign in as Chinnu (Store Owner) -> Update Category, Sector (Textiles), Turnover (₹68L) in Salem, TN.", styles["TableCell"]),
            Paragraph("Glassmorphic Login Modal + 3-Step Wizard", styles["TableCell"]),
            Paragraph("Demonstrates effortless onboarding capturing critical parameters for financial subsidies.", styles["TableCell"])
        ],
        [
            Paragraph("<b>0:45 – 1:30</b>", styles["TableCellBold"]),
            Paragraph("<b>2. Regional Voice AI Assistant</b><br/>Ask in Tamil: <i>'நம்மளோட பிசினஸ் எந்த ரீஜியன்ல பெர்பார்மன்ஸ் அதிகமா இருக்கு?'</i> or ask for top margin products.", styles["TableCell"]),
            Paragraph("Floating AI Voice Panel + Waveform Audio", styles["TableCell"]),
            Paragraph("Shows autonomous multi-dialect NLP answering real database facts with native speech audio.", styles["TableCell"])
        ],
        [
            Paragraph("<b>1:30 – 2:15</b>", styles["TableCellBold"]),
            Paragraph("<b>3. WhatsApp Automation Center</b><br/>Show instant trigger of Critical Stockout Alert (Silk Sarees) on the 5G Phone Simulator.", styles["TableCell"]),
            Paragraph("Smartphone Mockup + Dynamic Chat Log", styles["TableCell"]),
            Paragraph("Eliminates operational latency by delivering actionable alerts to the app merchants already use daily.", styles["TableCell"])
        ],
        [
            Paragraph("<b>2:15 – 3:00</b>", styles["TableCellBold"]),
            Paragraph("<b>4. Govt Schemes Hub & Calculator</b><br/>Show ₹32.5L unlocked subsidies, side-by-side PMEGP vs TN NEEDS matrix, and 1-click WhatsApp dispatch.", styles["TableCell"]),
            Paragraph("Govt Schemes Hub + Project Simulator", styles["TableCell"]),
            Paragraph("Delivers unmatched tangible financial value by putting government grant money directly into MSME hands.", styles["TableCell"])
        ]
    ]

    demo_table = Table(demo_steps_data, colWidths=[55, 160, 110, 207])
    demo_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(demo_table)
    story.append(Spacer(1, 10))

    # Conclusion Badge
    conclusion_text = (
        "<b>Conclusion:</b> Vyapaar Pulse AI democratizes enterprise-grade intelligence, bridging AI innovation "
        "with grassroots Indian commerce. Built with passion for Indian MSMEs."
    )
    concl_box = Table([[Paragraph(conclusion_text, styles["CalloutText"])]], colWidths=[532])
    concl_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#ECFDF5")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#A7F3D0")),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(concl_box)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] Generated Hackathon Overview PDF successfully: {PDF_OUTPUT_PATH}")


if __name__ == "__main__":
    build_pdf()
