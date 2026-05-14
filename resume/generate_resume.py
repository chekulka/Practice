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
            "Name", fontName="Helvetica-Bold", fontSize=16,
            textColor=dark, alignment=TA_CENTER, spaceAfter=1, leading=20,
        ),
        "contact": ParagraphStyle(
            "Contact", fontName="Helvetica", fontSize=8.5,
            textColor=mid_gray, alignment=TA_CENTER, spaceAfter=6, leading=11,
        ),
        "section_header": ParagraphStyle(
            "SectionHeader", fontName="Helvetica-Bold", fontSize=10,
            textColor=dark, spaceBefore=5, spaceAfter=1, leading=13,
        ),
        "summary": ParagraphStyle(
            "Summary", fontName="Helvetica", fontSize=9,
            textColor=light_gray, spaceAfter=2, leading=12.5,
        ),
        "job_company": ParagraphStyle(
            "JobCompany", fontName="Helvetica-Bold", fontSize=9.5,
            textColor=gray, spaceAfter=0, leading=12,
        ),
        "job_role": ParagraphStyle(
            "JobRole", fontName="Helvetica-Oblique", fontSize=9,
            textColor=accent, spaceAfter=1, leading=11,
        ),
        "bullet": ParagraphStyle(
            "Bullet", fontName="Helvetica", fontSize=8.5,
            textColor=light_gray, leftIndent=12, firstLineIndent=-12,
            spaceAfter=2, leading=11.5,
        ),
        "skill_line": ParagraphStyle(
            "SkillLine", fontName="Helvetica", fontSize=8.5,
            textColor=light_gray, spaceAfter=1, leading=11.5,
        ),
        "edu_title": ParagraphStyle(
            "EduTitle", fontName="Helvetica-Bold", fontSize=9,
            textColor=gray, spaceAfter=0, leading=11,
        ),
        "edu_school": ParagraphStyle(
            "EduSchool", fontName="Helvetica", fontSize=8.5,
            textColor=mid_gray, spaceAfter=3, leading=11,
        ),
        "patent_title": ParagraphStyle(
            "PatentTitle", fontName="Helvetica-Bold", fontSize=9,
            textColor=gray, spaceAfter=1, leading=11,
        ),
        "patent_meta": ParagraphStyle(
            "PatentMeta", fontName="Helvetica", fontSize=8.5,
            textColor=mid_gray, spaceAfter=1, leading=11,
        ),
        "patent_desc": ParagraphStyle(
            "PatentDesc", fontName="Helvetica", fontSize=8.5,
            textColor=light_gray, spaceAfter=1, leading=11,
        ),
    }
    return styles


def section_divider():
    """Return a horizontal rule for section separation."""
    return HRFlowable(
        width="100%", thickness=0.8,
        color=HexColor("#0f3460"), spaceAfter=3, spaceBefore=1,
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
        leftMargin=0.55 * inch,
        rightMargin=0.55 * inch,
        topMargin=0.4 * inch,
        bottomMargin=0.4 * inch,
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
    story.append(Spacer(1, 2))

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
        "Mentored junior analysts on A/B test design and causal inference; served as analytics advisor "
        "to leadership, communicating statistical uncertainty to inform resource allocation decisions."
    ))
    story.append(Spacer(1, 3))

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
    story.append(Spacer(1, 3))

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
    story.append(Spacer(1, 3))

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
        "Consultant (Data Analyst)  |  Bangalore, India",
        s["job_role"]
    ))
    story.append(bullet_text(s["bullet"],
        "Analyzed large-scale public sector healthcare insurance data using SQL and Python; designed anomaly "
        "detection pipelines and led business case definition across cross-functional enterprise analytics engagements."
    ))
    story.append(Spacer(1, 2))

    # ── TECHNICAL SKILLS ──
    story.append(Paragraph("TECHNICAL SKILLS", s["section_header"]))
    story.append(section_divider())
    story.append(skill_row(s["skill_line"],
        "Experimentation &amp; Causal Inference",
        "A/B Testing, Experiment Design, Power Analysis, Non-Inferiority Testing, "
        "Staggered DiD, Propensity Score Matching, Guardrail Metrics, Bayesian Methods"))
    story.append(skill_row(s["skill_line"],
        "Stats &amp; ML",
        "Statistical Modeling, Forecasting, Regression, Time Series, Hypothesis Testing, "
        "ML, Deep Learning, Clustering, Uplift Modeling"))
    story.append(skill_row(s["skill_line"],
        "Languages &amp; BI", "SQL (Expert), Python (Expert), R, Looker, Tableau, Data Studio"))
    story.append(skill_row(s["skill_line"],
        "Engineering &amp; Tools",
        "Apache Airflow, dbt, ETL Design, AWS (SageMaker, Athena), GCP, BigQuery, "
        "KPI Frameworks, Metrics Development, Measurement Strategy, Git"))
    story.append(skill_row(s["skill_line"],
        "Education",
        "M.S. Data Analytics, Northeastern University  |  B.E. Information Science, VTU India"))
    story.append(skill_row(s["skill_line"],
        "Patent",
        "US2022/0318979 A1 (Approved 2025) — Image Quality Analysis for Artifact Detection | Genentech"))

    doc.build(story)
    print(f"Resume generated successfully: {output_path}")
    return output_path


if __name__ == "__main__":
    generate_resume()
