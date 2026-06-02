"""
Cover Letter Generator for Chetan Kulkarni
Customizable template — replace [COMPANY], [ROLE], and [HOOK] before generating.
Uses reportlab for PDF generation.
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import sys
from datetime import date


def build_styles():
    dark = HexColor("#1a1a2e")
    gray = HexColor("#373737")
    light_gray = HexColor("#505050")
    mid_gray = HexColor("#646464")

    return {
        "name": ParagraphStyle(
            "Name", fontName="Helvetica-Bold", fontSize=16,
            textColor=dark, alignment=TA_CENTER, spaceAfter=1, leading=20,
        ),
        "contact": ParagraphStyle(
            "Contact", fontName="Helvetica", fontSize=9,
            textColor=mid_gray, alignment=TA_CENTER, spaceAfter=20, leading=12,
        ),
        "date": ParagraphStyle(
            "Date", fontName="Helvetica", fontSize=10,
            textColor=gray, spaceAfter=12, leading=13,
        ),
        "greeting": ParagraphStyle(
            "Greeting", fontName="Helvetica-Bold", fontSize=10.5,
            textColor=dark, spaceAfter=10, leading=14,
        ),
        "body": ParagraphStyle(
            "Body", fontName="Helvetica", fontSize=10,
            textColor=light_gray, spaceAfter=10, leading=14.5,
        ),
        "closing": ParagraphStyle(
            "Closing", fontName="Helvetica", fontSize=10,
            textColor=gray, spaceAfter=4, leading=14,
        ),
        "signature": ParagraphStyle(
            "Signature", fontName="Helvetica-Bold", fontSize=10.5,
            textColor=dark, spaceAfter=0, leading=14,
        ),
    }


def generate_cover_letter(company="[COMPANY]", role="[ROLE]", hook="[HOOK]"):
    output_path = "/home/user/Practice/resume/Chetan_Kulkarni_Cover_Letter.pdf"

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=0.85 * inch,
        rightMargin=0.85 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.7 * inch,
    )

    s = build_styles()
    story = []

    # Header
    story.append(Paragraph("CHETAN KULKARNI", s["name"]))
    story.append(Paragraph(
        "chetanmkulkarni@gmail.com  |  617-331-9347  |  "
        "linkedin.com/in/chetanmkulkarni  |  Open to Remote &amp; California",
        s["contact"]
    ))

    # Date
    today = date.today().strftime("%B %d, %Y")
    story.append(Paragraph(today, s["date"]))

    # Greeting
    story.append(Paragraph(f"Dear {company} Hiring Team,", s["greeting"]))

    # Paragraph 1 — Hook (customize per company)
    story.append(Paragraph(
        f"{hook}",
        s["body"]
    ))

    # Paragraph 2 — What I bring (constant)
    story.append(Paragraph(
        f"As a Lead Product Data Analyst / Data Scientist at Vanguard, I architected the "
        f"experimentation framework from scratch — designing and executing 20+ A/B tests using "
        f"power analysis, staggered difference-in-differences, and propensity score matching. "
        f"One initiative alone generated 19,000 new accounts in a single month (~$665M in new "
        f"deposits, est. $10M+ annualized revenue). I also built the KPI frameworks and self-serve "
        f"Looker/Tableau dashboards that leadership now uses for quarterly goal-setting — replacing "
        f"ad-hoc requests with scalable measurement infrastructure.",
        s["body"]
    ))

    # Paragraph 3 — Breadth of experience (constant)
    story.append(Paragraph(
        f"Before Vanguard, I spent 2+ years at Deloitte Consulting leading causal inference and "
        f"A/B testing for large-scale product rollouts — including non-inferiority experiments "
        f"for a financial web platform redesign. At Genentech, I built ML pipelines and developed "
        f"a CNN-based image quality system that became a US patent (approved 2025). Across 8+ years "
        f"and four companies, I've consistently operated at the intersection of experimentation, "
        f"product strategy, and cross-functional leadership.",
        s["body"]
    ))

    # Paragraph 4 — Why this role (customize per company)
    story.append(Paragraph(
        f"I'm drawn to the {role} role at {company} because it combines the strategic "
        f"problem-solving and analytical depth I thrive in with a product and mission I believe in. "
        f"I'm looking for a place where experimentation rigor and data literacy aren't afterthoughts "
        f"but core to how decisions get made — and {company} clearly fits that bar.",
        s["body"]
    ))

    # Close
    story.append(Paragraph(
        "I'd welcome the chance to discuss how my experience can contribute to your team.",
        s["body"]
    ))

    story.append(Spacer(1, 8))
    story.append(Paragraph("Best regards,", s["closing"]))
    story.append(Paragraph("Chetan Kulkarni", s["signature"]))

    doc.build(story)
    print(f"Cover letter generated: {output_path}")
    return output_path


# --- EXAMPLES ---
# To generate a generic template:
#   python3 generate_cover_letter.py
#
# To generate for a specific company:
#   python3 generate_cover_letter.py "Faire" "Strategy & Analytics Senior Lead" "Faire's mission..."
#
# Customize the 'hook' argument per company. This is the opening paragraph
# that shows you researched them. Keep it 2-3 sentences. Examples:
#
# FAIRE:
#   "Faire is building the infrastructure that powers the shop-local movement —
#    and I want to help you measure what's working. As someone who's spent 8+ years
#    turning ambiguous product questions into structured experiments and measurable
#    outcomes, I see a direct fit with the Strategy & Analytics Senior Lead role."
#
# CHIME:
#   "Chime is rethinking consumer banking from the member's perspective — and
#    measurement is how you know it's working. I've spent the last 2+ years building
#    exactly this kind of analytics infrastructure at Vanguard, another company where
#    getting the member experience right is everything."
#
# META:
#   "Meta's product analytics team works at a scale and rigor that few places match.
#    I want to bring my experimentation and causal inference expertise to a team where
#    A/B testing isn't a checkbox but the foundation of every product decision."
#
# HEADSPACE:
#   "Transforming mental healthcare requires knowing what actually helps — and that's
#    a measurement problem. I've spent 8+ years building experimentation and analytics
#    frameworks that turn ambiguous questions into evidence-based product decisions."

if __name__ == "__main__":
    if len(sys.argv) >= 4:
        generate_cover_letter(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        generate_cover_letter()
