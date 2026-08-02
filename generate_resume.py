#!/usr/bin/env python3
"""Generate resume PDFs for different target audiences."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Try to register a font for better rendering
try:
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
    FONT = 'DejaVuSans'
except:
    FONT = 'Helvetica'

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 15 * mm

# Style definitions
styles = {
    'name': ParagraphStyle('name', fontName=FONT, fontSize=24, leading=28,
                           spaceAfter=2, textColor=colors.HexColor('#1a1a2e'),
                           alignment=TA_CENTER),
    'title': ParagraphStyle('title', fontName=FONT, fontSize=11, leading=16,
                            spaceAfter=0, textColor=colors.HexColor('#4a4a6a'),
                            alignment=TA_CENTER),
    'section': ParagraphStyle('section', fontName=FONT, fontSize=14, leading=18,
                              spaceBefore=10, spaceAfter=6,
                              textColor=colors.HexColor('#1a1a2e'),
                              backColor=colors.HexColor('#f0f0f8'),
                              leftIndent=0, rightIndent=0,
                              borderWidth=0, borderColor=colors.HexColor('#1a1a2e'),
                              borderPadding=(3, 3, 3, 3)),
    'label': ParagraphStyle('label', fontName=FONT, fontSize=11, leading=15,
                            spaceBefore=3, spaceAfter=2,
                            textColor=colors.HexColor('#2c2c4a'), alignment=TA_LEFT),
    'body': ParagraphStyle('body', fontName=FONT, fontSize=10, leading=14,
                           spaceAfter=6, textColor=colors.HexColor('#4a4a6a'),
                           alignment=TA_LEFT, leftIndent=4),
    'small': ParagraphStyle('small', fontName=FONT, fontSize=9, leading=12,
                            textColor=colors.HexColor('#6a6a8a'), alignment=TA_LEFT),
    'skill_label': ParagraphStyle('skill_label', fontName=FONT, fontSize=9,
                                   textColor=colors.HexColor('#2c2c4a'),
                                   alignment=TA_LEFT, spaceBefore=2, spaceAfter=2),
}


def build_pdf(path, sections):
    doc = SimpleDocTemplate(
        path, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN,
    )
    story = []

    # Header
    story.append(Paragraph("Jiyanshu Singh", styles['name']))
    story.append(Paragraph("B.Tech Biotechnology student at NIT Rourkela | Building ML systems", styles['title']))
    story.append(Spacer(1, 6))

    story.append(Spacer(1, 8))

    story.append(Paragraph("Contact", styles['section']))
    story.append(Paragraph("📧 jiyanshusingh1@gmail.com &nbsp;|&nbsp; 📱 +91 8218608077 &nbsp;|&nbsp; "
                          "🔗 github.com/jiyanshusingh &nbsp;|&nbsp; 🔗 linkedin.com/in/jiyanshusingh", styles['body']))
    story.append(Spacer(1, 8))

    story.append(Spacer(1, 4))

    for heading, items in sections:
        story.append(Paragraph(heading, styles['section']))
        for line in items:
            story.append(Paragraph(line, styles['body']))
        story.append(Spacer(1, 8))

    doc.build(story)


# ---- Resume content ----

contact_block = "📧 jiyanshusingh1@gmail.com &nbsp;|&nbsp; 📱 +91 8218608077 &nbsp;|&nbsp; 🔗 github.com/jiyanshusingh &nbsp;|&nbsp; 🔗 linkedin.com/in/jiyanshusingh"

education = [
    "<b>B.Tech Biotechnology</b> · National Institute of Technology, Rourkela",
    "Expected 2027 · CGPA: 7.09/10 · Relevant coursework: Data Structures & Algorithms, Statistics, Mathematics for Engineers",
]

experience_analytics = [
    "<b>AI Intern</b> · Digitaaztrans Technologies (Remote) &nbsp;<i>Jan 2025 – Present</i>",
    "<b>MLEngineering:</b> Designed, deployed, and operated an ML-filtered multi-strategy trading engine on Google Cloud Platform serving live market data.",
    "<b>Deployment:</b> Containerized the system with Docker; orchestrated 6 parallel strategies on GCP with PostgreSQL logging of 38,500+ labeled trades.",
    "<b>Validation:</b> Applied walk-forward testing across 3 disjoint bull/bear market windows to ensure out-of-sample robustness.",
    "<b>Performance:</b> The ML trade filter improved simulated portfolio from a -₹225,000 drawdown to +₹93,000 profit.",
]

experience_freelance = [
    "<b>Freelance Data Scientist / ML Engineer</b> &nbsp;<i>Dec 2023 – Present</i>",
    "<b>End-to-end delivery:</b> Built and deployed 4 production web applications (A/B Testing Dashboard, Sales CRM, Invoice Generator, Hydrogel Portal) — all with Dockerized FastAPI/Flask backends on Render/GitHub.",
    "<b>Statistical consulting:</b> Delivered A/B test analysis (p-values, Bayesian Monte Carlo, power analysis) for small clients.",
]

projects_analytics = [
    "<b>AI Trading Engine</b> &nbsp;<a href='https://github.com/jiyanshusingh/trading-engine'>[Code]</a>",
    "<b>Problem:</b> A naive strategy lost ₹225k; an XGBoost ML filter that labels 38,500+ trades as net-profitable-after-costs turned it into +₹93k profit.",
    "<b>Key results</b> (OOS-validated): 95% reduction in false signals; walk-forward validated across 3 market regimes (bear → consolidation → rally).",
    "<b>Tech stack:</b> Python, XGBoost, FastAPI, Docker, GCP (Compute Engine + Cloud SQL), PostgreSQL, walk-forward backtesting framework.",
    "<b>A/B Testing Dashboard</b> &nbsp;<a href='https://github.com/jiyanshusingh/ab-testing-dashboard'>[Code]</a>",
    "<b>Purpose:</b> Multi-page statistical analysis app that analyzes experiment data and recommends Launch / Iterate / Kill using p-values, Bayesian Monte Carlo, power analysis, and sample size calculations.",
    "<b>Impact:</b> Generates consulting-grade PDF reports for stakeholders — deployed at <a href='https://ab-testing-dashboard.onrender.com'>https://ab-testing-dashboard.onrender.com</a>.",
    "<b>Tech stack:</b> FastAPI, Bootstrap 5, SciPy, Docker, Render.",
]

projects_biotech = [
    "<b>Peptide Hydrogel Prediction</b> &nbsp;<a href='https://github.com/jiyanshusingh/hydrogel_project'>[Code]</a>",
    "<b>Purpose:</b> Machine-learning models predicting hydrogel formation of short peptides from amino-acid sequence and terminal modifications.",
    "<b>Key results:</b> ROC-AUC 0.888 (amyloid classification), 0.720 (hydrogel); SHAP-based interpretability; strict leakage prevention on 364-sample benchmark; external-transfer validation on 14 literature entries.",
    "<b>Web portal:</b> Multi-page Flask app with researcher auth, dataset browsing, live training jobs, and de-novo peptide design scoring.",
    "<b>Tech stack:</b> Python, RandomForest/XGBoost/ESM2, SHAP, Flask, Docker, Render.",
]

projects_software = [
    "<b>Sales CRM Dashboard</b> &nbsp;<a href='https://github.com/jiyanshusingh/sales_dashboard'>[Code]</a>",
    "<b>Purpose:</b> Full-stack CRM for managing sales leads with KPI dashboard, funnel analysis, revenue charts, CSV export, and basic auth.",
    "<b>Tech stack:</b> FastAPI, Bootstrap 5, Plotly.js, SQLAlchemy, Plotly Dash, Docker, Render.",
    "<b>Invoice Generator</b> &nbsp;<a href='https://github.com/jiyanshusingh/invoice-generator'>[Code]</a>",
    "<b>Purpose:</b> SaaS-ready invoice generation service with PDF export, SQLAlchemy backend, template-based rendering, and Docker deployment.",
    "<b>Tech stack:</b> FastAPI, SQLAlchemy, ReportLab (PDF), Docker, Render.",
]

skills_analytics = [
    "<b>Languages:</b> Python (expert), SQL, JavaScript",
    "<b>ML/AI:</b> XGBoost, scikit-learn, walk-forward validation, Bayesian inference, statistical testing (SciPy), hypothesis testing, power analysis",
    "<b>Data:</b> pandas, NumPy, PostgreSQL, FastAPI, Docker, GCP, REST APIs, Git",
]

skills_biotech = [
    "<b>Languages:</b> Python (expert), SQL",
    "<b>ML/AI:</b> scikit-learn, XGBoost, RandomForest, protein language models (ESM2), SHAP, feature engineering",
    "<b>Biotech tools:</b> Biopython, peptide representation, A/B testing for bioassays, statistical analysis",
    "<b>Deployment:</b> Flask, Docker, Render, data visualization",
]

skills_software = [
    "<b>Languages:</b> Python, JavaScript, SQL",
    "<b>Backend:</b> FastAPI, Flask, SQLAlchemy, Pydantic, ReportLab (PDF generation)",
    "<b>Frontend:</b> Bootstrap 5, Plotly.js, JINJA2 templates",
    "<b>DevOps:</b> Docker, Docker Compose, Render, GCP, PostgreSQL, Git, REST APIs",
]

achievements = [
    "🏆 Deployed 5 production web applications (FastAPI/Flask + Docker + Render/GCP).",
    "📊 Labeled 38,500+ trades for ML filter; 95% false-signal reduction; walk-forward OOS validated across 3 market windows.",
    "🧬 350-sample peptide benchmark with leakage prevention; amyloid ROC-AUC 0.888.",
    "<b>Skills I'm learning:</b> XGBoost, walk-forward testing, Bayesian A/B testing, biotech ML.",
]


def make_analytics_resume():
    sections = [
        ("Education", education),
        ("Experience", experience_analytics + experience_freelance),
        ("Projects", projects_analytics),
        ("Skills", skills_analytics),
        ("Achievements", achievements),
    ]
    path = os.path.join(os.path.dirname(__file__), "assets/resume/resume_analytics_finance.pdf")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    build_pdf(path, sections)
    print(f"✓ Analytics & Finance resume → {path}")


def make_biotech_resume():
    sections = [
        ("Education", education),
        ("Experience", experience_freelance),
        ("Projects", projects_analytics + projects_biotech + projects_software),
        ("Skills", skills_biotech),
        ("Achievements", achievements),
    ]
    path = os.path.join(os.path.dirname(__file__), "assets/resume/resume_biotech_core.pdf")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    build_pdf(path, sections)
    print(f"✓ Biotech/Core resume → {path}")


def make_software_resume():
    sections = [
        ("Education", education),
        ("Experience", experience_analytics + experience_freelance),
        ("Projects", projects_software),
        ("Skills", skills_software),
        ("Achievements", achievements),
    ]
    path = os.path.join(os.path.dirname(__file__), "assets/resume/resume_software.pdf")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    build_pdf(path, sections)
    print(f"✓ Software resume → {path}")


def make_freelance_resume():
    sections = [
        ("Education", education),
        ("Experience", experience_freelance),
        ("Projects", projects_analytics + projects_biotech + projects_software),
        ("Skills", skills_analytics),
        ("Achievements", achievements),
    ]
    path = os.path.join(os.path.dirname(__file__), "assets/resume/resume_freelance.pdf")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    build_pdf(path, sections)
    print(f"✓ Freelance resume → {path}")


if __name__ == "__main__":
    make_analytics_resume()
    make_biotech_resume()
    make_software_resume()
    make_freelance_resume()
