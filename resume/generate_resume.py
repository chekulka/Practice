"""
ATS-Optimized Resume Generator for Chetan Kulkarni
Targeted for Product Data Scientist / Experimentation roles
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
    output_path = "/home/user/Practice/resume/Chetan_Kulkarni_Product_Data_Scientist_Resume.pdf"

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
        "Product &amp; Digital Analytics  |  Open to Remote &amp; California  |  "
        "617-331-9347  |  chetanmkulkarni@gmail.com  |  "
        "linkedin.com/in/chetanmkulkarni",
        s["contact"]
    ))

    # ── PROFESSIONAL SUMMARY ──
    story.append(Paragraph("SUMMARY", s["section_header"]))
    story.append(section_divider())
    story.append(Paragraph(
        "Product data scientist with 8+ years delivering action-oriented insights that drive product "
        "strategy at scale. Expert in A/B test design and execution (20+ experiments), causal inference "
        "methods (staggered DiD, propensity score matching, pre-post analysis) for consumer "
        "product decision-making, and statistical modeling. Proven track record translating complex "
        "quantitative findings into measurable outcomes — from $665M in new deposits to self-serve "
        "analytics tools that improve cross-functional data literacy. Proficient in SQL, Python, R, "
        "Looker, and Tableau. Comfortable with ambiguous, fast-paced environments.",
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
    story.append(Paragraph(
        "Lead Product Data Analyst / Data Scientist  |  Dallas, TX / San Diego, CA",
        s["job_role"]
    ))
    story.append(bullet_text(s["bullet"],
        "Developed action-oriented insights through observational causal analysis (staggered "
        "difference-in-differences, propensity score matching) to inform product strategy for "
        "Vanguard's digital consumer journeys, serving millions of members across web and mobile."
    ))
    story.append(bullet_text(s["bullet"],
        "Architected end-to-end experimentation framework; designed and executed 20+ A/B tests with "
        "power analysis and sample size estimation, driving a 5% reduction in support call rate "
        "(~$250K+ annual savings) and 2–3% improvement in product engagement completion rate."
    ))
    story.append(bullet_text(s["bullet"],
        "Spearheaded Cash growth initiative: designed 5 targeted experiments in coordination with "
        "cross-functional partners (Product, Marketing, Finance), generating 19,000 new accounts "
        "in a single month — ~$665M in new deposits and an estimated $10M+ in annualized net interest revenue."
    ))
    story.append(bullet_text(s["bullet"],
        "Designed KPI frameworks and quarterly goal-setting metrics for digital product and marketing "
        "initiatives, delivering Looker and Tableau dashboards that enabled self-serve performance "
        "monitoring for senior stakeholders."
    ))
    story.append(bullet_text(s["bullet"],
        "Mentored junior analysts on statistical methodology, A/B test design, and causal inference; "
        "improved cross-functional data literacy by leading measurement education sessions with "
        "product and engineering teams."
    ))
    story.append(bullet_text(s["bullet"],
        "Served as analytics advisor to leadership, communicating statistical uncertainty and "
        "translating findings into resource allocation and strategic investment decisions."
    ))
    story.append(Spacer(1, 5))

    # --- Deloitte (San Diego) ---
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
    story.append(Paragraph(
        "Senior Consultant - Analytics  |  San Diego, CA",
        s["job_role"]
    ))
    story.append(bullet_text(s["bullet"],
        "Applied causal inference and A/B testing — including non-inferiority experiments and "
        "staggered difference-in-differences — to measure impact of product design changes on "
        "user engagement and conversion for client financial web platforms."
    ))
    story.append(bullet_text(s["bullet"],
        "Built self-serve analytics tools and interactive dashboards in Tableau and Looker; improved "
        "cross-functional data literacy by enabling product and design teams to independently monitor "
        "key product metrics."
    ))
    story.append(bullet_text(s["bullet"],
        "Developed KPI frameworks and measurement strategies for digital products, aligning analytics "
        "output to quarterly OKRs and business goals."
    ))
    story.append(bullet_text(s["bullet"],
        "Built ETL pipelines and data infrastructure using Apache Airflow and AWS Athena, supporting "
        "analytics at scale for client product workflows."
    ))
    story.append(bullet_text(s["bullet"],
        "Led investigative analytics projects from problem definition through delivery, producing "
        "actionable insights that shaped client product roadmap decisions."
    ))
    story.append(Spacer(1, 5))

    # --- Genentech ---
    story.append(Paragraph(
        "Genentech, Inc (via Pro-Unlimited) <font size=9 color='#646464'>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;"
        "Jan 2020 - Jul 2021</font>",
        s["job_company"]
    ))
    story.append(Paragraph(
        "Informatics Data Analyst  |  South San Francisco, CA",
        s["job_role"]
    ))
    story.append(bullet_text(s["bullet"],
        "Developed a 5-layer CNN to classify image quality in clinical pathology slides and an "
        "LBP-based quality application — core invention in US Patent (US2022/0318979 A1, approved 2025)."
    ))
    story.append(bullet_text(s["bullet"],
        "Built production ML deployment pipeline with multi-GPU environment and Apache Airflow "
        "automation; computed statistical quality metrics integrated with Tableau dashboard for "
        "clinical review."
    ))
    story.append(bullet_text(s["bullet"],
        "Collaborated with cross-functional ML and pathology teams to translate model outputs into "
        "clinical workflow decisions."
    ))
    story.append(Spacer(1, 5))

    # --- Deloitte (India) ---
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
        "Feb 2015 - Apr 2018</font>",
        s["job_company"]
    ))
    story.append(Paragraph(
        "Senior Consultant  |  Bangalore, India",
        s["job_role"]
    ))
    story.append(bullet_text(s["bullet"],
        "Analyzed large-scale public sector healthcare insurance data using SQL and Python; designed "
        "anomaly detection pipelines and delivered data-driven insights for policy optimization."
    ))
    story.append(bullet_text(s["bullet"],
        "Led business case definition, scope planning, and data quality testing across "
        "cross-functional teams for enterprise analytics engagements."
    ))
    story.append(Spacer(1, 6))

    # ── TECHNICAL SKILLS ──
    story.append(Paragraph("TECHNICAL SKILLS", s["section_header"]))
    story.append(section_divider())
    story.append(skill_row(s["skill_line"],
        "Experimentation",
        "A/B Testing, Experiment Design, Power Analysis, Sample Size Estimation, "
        "Non-Inferiority Testing, Hypothesis Testing, Guardrail Metrics"))
    story.append(skill_row(s["skill_line"],
        "Causal Inference &amp; Stats",
        "Staggered DiD, Propensity Score Matching, Pre-Post Analysis, Regression, "
        "Statistical Modeling, Forecasting, Bayesian Methods, Time Series Analysis"))
    story.append(skill_row(s["skill_line"],
        "Languages", "SQL (Expert), Python (Expert), R"))
    story.append(skill_row(s["skill_line"],
        "ML &amp; Modeling",
        "Machine Learning, Deep Learning, Clustering, Uplift Modeling, CNN"))
    story.append(skill_row(s["skill_line"],
        "Visualization &amp; BI", "Looker, Tableau, Data Studio"))
    story.append(skill_row(s["skill_line"],
        "Data Engineering",
        "Apache Airflow, dbt, ETL Pipeline Design, AWS (SageMaker, Athena), GCP, BigQuery"))
    story.append(skill_row(s["skill_line"],
        "Frameworks",
        "KPI Frameworks, Metrics Development, Measurement Strategy, Analytics Architecture, OKR Development"))
    story.append(skill_row(s["skill_line"],
        "Tools", "Adobe Analytics, Adobe Target, Git, Jupyter"))
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
        "Image Quality Analysis for Artifact Detection in Pathology Slide Images (Approved 2025)",
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
