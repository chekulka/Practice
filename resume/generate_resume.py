"""
ATS-Optimized Resume Generator for Chetan Kulkarni
Targeted for Lead Data Analyst roles at Chime and NerdWallet
Uses reportlab for PDF generation
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT


def build_styles():
    """Create all paragraph styles for the resume."""
    dark = HexColor("#1a1a2e")
    accent = HexColor("#0f3460")
    gray = HexColor("#373737")
    light_gray = HexColor("#505050")
    mid_gray = HexColor("#646464")

    styles = {
        "name": ParagraphStyle(
            "Name", fontName="Helvetica-Bold", fontSize=18,
            textColor=dark, alignment=TA_CENTER, spaceAfter=2, leading=22,
        ),
        "contact": ParagraphStyle(
            "Contact", fontName="Helvetica", fontSize=9,
            textColor=mid_gray, alignment=TA_CENTER, spaceAfter=10, leading=12,
        ),
        "section_header": ParagraphStyle(
            "SectionHeader", fontName="Helvetica-Bold", fontSize=11,
            textColor=dark, spaceBefore=8, spaceAfter=2, leading=14,
        ),
        "summary": ParagraphStyle(
            "Summary", fontName="Helvetica", fontSize=9.5,
            textColor=light_gray, spaceAfter=4, leading=13.5,
        ),
        "job_company": ParagraphStyle(
            "JobCompany", fontName="Helvetica-Bold", fontSize=10,
            textColor=gray, spaceAfter=0, leading=13,
        ),
        "job_role": ParagraphStyle(
            "JobRole", fontName="Helvetica-Oblique", fontSize=9.5,
            textColor=accent, spaceAfter=2, leading=12,
        ),
        "bullet": ParagraphStyle(
            "Bullet", fontName="Helvetica", fontSize=9,
            textColor=light_gray, leftIndent=14, firstLineIndent=-14,
            spaceAfter=3, leading=12.5,
        ),
        "skill_line": ParagraphStyle(
            "SkillLine", fontName="Helvetica", fontSize=9,
            textColor=light_gray, spaceAfter=2, leading=12.5,
        ),
        "edu_title": ParagraphStyle(
            "EduTitle", fontName="Helvetica-Bold", fontSize=9.5,
            textColor=gray, spaceAfter=0, leading=12,
        ),
        "edu_school": ParagraphStyle(
            "EduSchool", fontName="Helvetica", fontSize=9,
            textColor=mid_gray, spaceAfter=4, leading=12,
        ),
        "patent_title": ParagraphStyle(
            "PatentTitle", fontName="Helvetica-Bold", fontSize=9.5,
            textColor=gray, spaceAfter=1, leading=12,
        ),
        "patent_meta": ParagraphStyle(
            "PatentMeta", fontName="Helvetica", fontSize=9,
            textColor=mid_gray, spaceAfter=2, leading=12,
        ),
        "patent_desc": ParagraphStyle(
            "PatentDesc", fontName="Helvetica", fontSize=9,
            textColor=light_gray, spaceAfter=2, leading=12,
        ),
    }
    return styles


def section_divider():
    """Return a horizontal rule for section separation."""
    return HRFlowable(
        width="100%", thickness=0.8,
        color=HexColor("#0f3460"), spaceAfter=6, spaceBefore=1,
    )


def bullet_text(style, text):
    """Create a bullet point paragraph."""
    return Paragraph(f"\u2022  {text}", style)


def skill_row(style, category, skills):
    """Create a skill line with bold category."""
    return Paragraph(
        f"<b>{category}:</b>  {skills}", style
    )


def generate_resume():
    output_path = "/home/user/Practice/resume/Chetan_Kulkarni_Lead_Data_Analyst_Resume.pdf"

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=0.65 * inch,
        rightMargin=0.65 * inch,
        topMargin=0.5 * inch,
        bottomMargin=0.5 * inch,
    )

    s = build_styles()
    story = []

    # ── NAME & CONTACT ──
    story.append(Paragraph("CHETAN KULKARNI", s["name"]))
    story.append(Paragraph(
        "Dallas, TX  |  617-331-9347  |  chetanmkulkarni@gmail.com  |  "
        "linkedin.com/in/chetanmkulkarni",
        s["contact"]
    ))

    # ── PROFESSIONAL SUMMARY ──
    story.append(Paragraph("PROFESSIONAL SUMMARY", s["section_header"]))
    story.append(section_divider())
    story.append(Paragraph(
        "Lead Data Analyst with 6+ years of experience driving forecasting, analytics architecture, "
        "and data-driven decision-making in financial services and fintech. Expert in building scalable "
        "analytics solutions, KPI frameworks, and measurement strategies that shape business outcomes. "
        "Proven track record of leading 25+ A/B experiments with measurable revenue and engagement impact. "
        "Adept at building forecasting infrastructure, designing semantic models, and partnering with "
        "cross-functional teams including Finance, Product, Marketing, and Engineering. Proficient in "
        "SQL, Python, R, Looker, and Tableau with deep expertise in statistical modeling, causal inference, "
        "and executive-level communication of insights and uncertainty.",
        s["summary"]
    ))
    story.append(Spacer(1, 4))

    # ── PROFESSIONAL EXPERIENCE ──
    story.append(Paragraph("PROFESSIONAL EXPERIENCE", s["section_header"]))
    story.append(section_divider())

    # --- Vanguard ---
    story.append(Paragraph(
        "Vanguard Group, Inc <font size=9 color='#646464'>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "Sep 2023 - Present</font>",
        s["job_company"]
    ))
    story.append(Paragraph("Lead Data Analyst  |  Dallas, TX", s["job_role"]))
    story.append(bullet_text(s["bullet"],
        "Architected and owned the experimentation framework, designing and executing 20+ A/B tests "
        "and pre-post analyses with a 25% success rate, driving a 3-5% reduction in call rate and "
        "2-3% increase in Journey Completes across digital channels."
    ))
    story.append(bullet_text(s["bullet"],
        "Built forecasting models and measurement strategies for key financial KPIs and unit economics, "
        "enabling predictable member funnel growth and data-driven investment decisions across product "
        "and marketing initiatives."
    ))
    story.append(bullet_text(s["bullet"],
        "Spearheaded the Cash growth initiative by designing 5 targeted experiments and coordinating "
        "with cross-functional teams (Product, Marketing, Finance, Operations), resulting in 19,000 "
        "new cash accounts in a single month (0.5% of total accounts)."
    ))
    story.append(bullet_text(s["bullet"],
        "Designed scalable KPI frameworks and interactive dashboards in Looker and Tableau, delivering "
        "actionable performance monitoring and proactive insights to executives and senior stakeholders."
    ))
    story.append(bullet_text(s["bullet"],
        "Served as analytics advisor to leadership, translating complex statistical findings and "
        "communicating uncertainty to facilitate strategic business decisions and resource allocation."
    ))
    story.append(Spacer(1, 5))

    # --- Deloitte ---
    story.append(Paragraph(
        "Deloitte Consulting <font size=9 color='#646464'>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "Jul 2021 - Sep 2023</font>",
        s["job_company"]
    ))
    story.append(Paragraph("Senior Consultant  |  San Diego, CA", s["job_role"]))
    story.append(bullet_text(s["bullet"],
        "Led end-to-end analytics for a large-scale website modernization initiative, architecting "
        "a staged rollout strategy with non-inferiority testing from 5% to 100% traffic exposure, "
        "ensuring data-driven validation at each deployment phase."
    ))
    story.append(bullet_text(s["bullet"],
        "Designed and executed statistical analyses including A/B experiments, causal inference methods, "
        "and regression modeling to measure UI/UX impact on web performance, conversion rates, and "
        "user behavior metrics."
    ))
    story.append(bullet_text(s["bullet"],
        "Built and automated scalable ETL data pipelines using SQL and Apache Airflow, enabling "
        "reproducible financial data workflows and reducing manual reporting effort by 60%."
    ))
    story.append(bullet_text(s["bullet"],
        "Partnered with cross-functional stakeholders across Engineering, Product, and Business teams "
        "to drive analytics-informed decision-making, measurement alignment, and OKR development."
    ))
    story.append(Spacer(1, 5))

    # --- Genentech ---
    story.append(Paragraph(
        "Genentech, Inc <font size=9 color='#646464'>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "Jan 2020 - Jul 2021</font>",
        s["job_company"]
    ))
    story.append(Paragraph("Informatics Data Analyst  |  South San Francisco, CA", s["job_role"]))
    story.append(bullet_text(s["bullet"],
        "Developed an automated Quality Control tool using Python and Local Binary Pattern (LBP) image "
        "processing, reducing computational overhead for artifact detection in digital pathology slides."
    ))
    story.append(bullet_text(s["bullet"],
        "Architected scalable data processing pipelines across multi-CPU/GPU environments, executing "
        "tiling experiments at 10x, 20x, and 40x magnifications for whole-slide image analysis."
    ))
    story.append(bullet_text(s["bullet"],
        "Built interactive Tableau dashboards with statistical metrics (contrast, entropy) and blur "
        "heat maps, enabling pathologists to make data-driven quality assessments."
    ))
    story.append(bullet_text(s["bullet"],
        "Designed the deployment pipeline using Apache Airflow for end-to-end task orchestration, "
        "ensuring reproducible and automated analysis workflows."
    ))
    story.append(Spacer(1, 6))

    # ── TECHNICAL SKILLS ──
    story.append(Paragraph("TECHNICAL SKILLS", s["section_header"]))
    story.append(section_divider())
    story.append(skill_row(s["skill_line"],
        "Languages", "SQL (Expert), Python (Expert), R"))
    story.append(skill_row(s["skill_line"],
        "Visualization &amp; BI", "Looker, Tableau, Data Studio"))
    story.append(skill_row(s["skill_line"],
        "Analytics &amp; Modeling",
        "A/B Testing, Statistical Modeling, Forecasting, Causal Inference, Regression, "
        "Clustering, Machine Learning, Deep Learning, EDA, Text Analysis"))
    story.append(skill_row(s["skill_line"],
        "Data Engineering",
        "Apache Airflow, dbt, ETL Pipeline Design, Data Pipeline Architecture, Semantic Models"))
    story.append(skill_row(s["skill_line"],
        "Frameworks &amp; Strategy",
        "KPI Frameworks, Measurement Strategy, Analytics Architecture, OKR Development"))
    story.append(skill_row(s["skill_line"],
        "Tools &amp; Platforms", "Adobe Analytics, Adobe Target, Git, Jupyter, BigQuery"))
    story.append(Spacer(1, 6))

    # ── EDUCATION ──
    story.append(Paragraph("EDUCATION", s["section_header"]))
    story.append(section_divider())
    story.append(Paragraph("Master of Science in Data Analytics", s["edu_title"]))
    story.append(Paragraph("Northeastern University, Boston, MA", s["edu_school"]))
    story.append(Paragraph(
        "Bachelor of Engineering in Information Science and Engineering", s["edu_title"]))
    story.append(Paragraph(
        "Visvesvaraya Technological University (VTU), Belgaum, India", s["edu_school"]))
    story.append(Spacer(1, 6))

    # ── PATENT ──
    story.append(Paragraph("PATENT", s["section_header"]))
    story.append(section_divider())
    story.append(Paragraph(
        "Image Quality Analysis for Artifact Detection in Pathology Slide Images",
        s["patent_title"]
    ))
    story.append(Paragraph(
        "US Patent Application No. US2022/0318979 A1  |  Published March 2022  |  Genentech, Inc",
        s["patent_meta"]
    ))
    story.append(Paragraph(
        "Developed a patented method for detecting imaging artifacts in digital pathology slides, "
        "applying automated image processing techniques to identify and flag quality issues in "
        "whole-slide images used for clinical diagnosis.",
        s["patent_desc"]
    ))

    doc.build(story)
    print(f"Resume generated successfully: {output_path}")
    return output_path


if __name__ == "__main__":
    generate_resume()
