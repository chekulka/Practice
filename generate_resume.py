#!/usr/bin/env python3
"""
Resume generator for Lead Data Analyst position using reportlab.
Tailored for startup AI/ML roles.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT


def create_resume():
    doc = SimpleDocTemplate(
        "/home/user/Practice/New-Resume.pdf",
        pagesize=letter,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=16,
        alignment=TA_CENTER,
        spaceAfter=2,
        fontName='Helvetica-Bold'
    )

    contact_style = ParagraphStyle(
        'Contact',
        parent=styles['Normal'],
        fontSize=9,
        alignment=TA_CENTER,
        spaceAfter=10
    )

    section_style = ParagraphStyle(
        'Section',
        parent=styles['Heading2'],
        fontSize=10,
        fontName='Helvetica-Bold',
        spaceBefore=8,
        spaceAfter=4,
        underline=True,
        textColor=colors.black
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=9,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
        leading=12
    )

    job_title_style = ParagraphStyle(
        'JobTitle',
        parent=styles['Normal'],
        fontSize=9,
        fontName='Helvetica-Bold',
        spaceAfter=1
    )

    job_role_style = ParagraphStyle(
        'JobRole',
        parent=styles['Normal'],
        fontSize=9,
        fontName='Helvetica-Oblique',
        spaceAfter=3
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontSize=9,
        leftIndent=15,
        spaceAfter=3,
        leading=11
    )

    skill_style = ParagraphStyle(
        'Skill',
        parent=styles['Normal'],
        fontSize=9,
        spaceAfter=2,
        leading=11
    )

    elements = []

    # Header
    elements.append(Paragraph("CHETAN KULKARNI", title_style))
    elements.append(Paragraph(
        "Dallas, TX (Open to Remote) | chetanmkulkarni@gmail.com | 617-331-9347 | LinkedIn",
        contact_style
    ))

    # Executive Summary
    elements.append(Paragraph("<u>EXECUTIVE SUMMARY</u>", section_style))
    elements.append(Paragraph(
        "Results-driven Lead Data Analyst with 5+ years of expertise in experimentation, causal inference, "
        "and growth analytics. Proven track record of leading 25+ A/B experiments with measurable business impact, "
        "including 3-5% conversion improvements and 19K account growth. Skilled in building experimentation frameworks, "
        "statistical modeling, and data-driven decision systems. Passionate about leveraging data science to drive "
        "product growth at fast-paced, innovative startups.",
        body_style
    ))

    # Professional Experience
    elements.append(Paragraph("<u>PROFESSIONAL EXPERIENCE</u>", section_style))

    # Vanguard
    elements.append(Paragraph(
        "<b>Vanguard Group, Inc,</b> Dallas, TX, USA&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<i>Sep 2023 - Present</i>",
        job_title_style
    ))
    elements.append(Paragraph("<i>Lead Data Analyst</i>", job_role_style))

    bullets_vanguard = [
        "Spearheaded experimentation program running 20+ A/B tests with rigorous pre/post analysis, "
        "achieving 25% success rate and driving 3-5% decrease in call rate and 2-3% lift in Journey Completes.",

        "Led Cash growth initiative through 5 strategic experiments across cross-functional teams, "
        "directly resulting in 19K new accounts (0.5% portfolio growth) within a single month.",

        "Architected advanced KPI frameworks and experimentation infrastructure enabling real-time "
        "performance monitoring and data-driven product decisions.",

        "Built interactive Tableau dashboards delivering actionable insights to executives, "
        "utilizing statistical analysis to identify growth opportunities and optimization levers."
    ]
    for bullet in bullets_vanguard:
        elements.append(Paragraph(f"• {bullet}", bullet_style))

    elements.append(Spacer(1, 6))

    # Deloitte
    elements.append(Paragraph(
        "<b>Deloitte Consulting,</b> San Diego, CA, USA&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<i>Jul 2021 - Sep 2023</i>",
        job_title_style
    ))
    elements.append(Paragraph("<i>Senior Consultant</i>", job_role_style))

    bullets_deloitte = [
        "Designed staged rollout strategy using non-inferiority testing with 5% traffic exposure, "
        "scaling to 20% intervals with data-driven validation at each phase, ensuring zero negative impact.",

        "Conducted causal inference analysis including A/B experiments and quasi-experimental methods "
        "to measure UI/UX design impact on user behavior and conversion metrics.",

        "Engineered automated ETL pipelines using Apache Airflow for client's financial data workflows, "
        "reducing manual processing time by 60%."
    ]
    for bullet in bullets_deloitte:
        elements.append(Paragraph(f"• {bullet}", bullet_style))

    elements.append(Spacer(1, 6))

    # Genentech
    elements.append(Paragraph(
        "<b>Genentech, Inc,</b> South San Francisco, CA, USA&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<i>Jan 2020 - Jul 2021</i>",
        job_title_style
    ))
    elements.append(Paragraph("<i>Informatics Data Analyst (Intern to Full-Time)</i>", job_role_style))

    bullets_genentech = [
        "Developed ML-powered quality control tool using Local Binary Pattern (LBP) for image artifact "
        "detection, reducing computational overhead while maintaining diagnostic accuracy.",

        "Executed tiling experiments at 10x, 20x, 40x magnifications on multi-CPU environment, "
        "identifying digitization artifacts across 1000+ pathology slides.",

        "Built end-to-end deployment pipeline utilizing Multi-GPU infrastructure and Apache Airflow, "
        "with interactive Tableau heat map visualizations for pathologist review."
    ]
    for bullet in bullets_genentech:
        elements.append(Paragraph(f"• {bullet}", bullet_style))

    # Education
    elements.append(Paragraph("<u>EDUCATION</u>", section_style))
    elements.append(Paragraph(
        "<b>Master of Science in Data Analytics</b> | Northeastern University, Boston, MA, USA",
        skill_style
    ))
    elements.append(Paragraph(
        "<b>Bachelor of Engineering in Information Science and Engineering</b> | VTU, Belgaum, KA, India",
        skill_style
    ))

    # Technical Publications
    elements.append(Paragraph("<u>TECHNICAL PUBLICATIONS</u>", section_style))
    elements.append(Paragraph(
        "<b>Title: Image Quality Analysis for Artifact Detection in Pathology Slide Images</b> <i>(Genentech, Inc)</i>",
        skill_style
    ))
    elements.append(Paragraph(
        "<i>US Patent Application No.</i> <b>US2022/0318979 A1</b>, <i>Published March 2022</i> - "
        "Novel method for detecting imaging artifacts in digital pathology slides to enhance diagnostic accuracy.",
        bullet_style
    ))

    # Technical Skills
    elements.append(Paragraph("<u>TECHNICAL SKILLS</u>", section_style))

    skills_data = [
        ("<b>Programming:</b>", "Python (Pandas, NumPy, SciPy, Scikit-learn), SQL, R"),
        ("<b>Visualization:</b>", "Tableau, Looker, Power BI, Matplotlib, Plotly"),
        ("<b>Experimentation:</b>", "A/B Testing, Causal Inference, Bayesian Analysis, Statistical Modeling"),
        ("<b>Data Pipeline:</b>", "Apache Airflow, dbt, ETL/ELT, Data Modeling"),
        ("<b>Cloud & Tools:</b>", "Snowflake, AWS, Git, Adobe Analytics, Adobe Target, Amplitude"),
        ("<b>ML Techniques:</b>", "Regression, Clustering, Classification, Deep Learning, NLP, Text Analysis")
    ]

    for label, value in skills_data:
        elements.append(Paragraph(f"{label} {value}", skill_style))

    doc.build(elements)
    print("Resume saved to New-Resume.pdf")


if __name__ == "__main__":
    create_resume()
