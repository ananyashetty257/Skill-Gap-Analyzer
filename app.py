import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Page Config & Theme
st.set_page_config(page_title="Intelligent Skill Gap Analyzer", layout="wide")
st.markdown("""
<style>
    .stApp { background: #0f172a; color: #e2e8f0; }
    .header-container { display: flex; align-items: center; justify-content: space-between; padding: 1.5rem 3rem; background: #1e293b; border-radius: 20px; border: 1px solid #334155; margin-bottom: 2.5rem; }
    .title-text { font-weight: 800; font-size: 2.2rem; color: #38bdf8; }
    section[data-testid="stSidebar"] { background-color: #1e293b; border-right: 1px solid #334155; }
    .stSlider label, .stSelectbox label, .stTextInput label { color: #f1f5f9 !important; font-weight: 600 !important; }
    .stSlider > div > div > div > div { background-color: #38bdf8; }
    #MainMenu, footer {visibility: hidden;}
    .cert-link { display: block; background: #1e293b; color: #38bdf8 !important; padding: 0.8rem; border-radius: 10px; text-decoration: none; font-weight: 600; margin-bottom: 0.6rem; border: 1px solid #334155; text-align: center; transition: all 0.3s ease; }
    .cert-link:hover { background: #38bdf8; color: #0f172a !important; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(56, 189, 248, 0.2); }
</style>
""", unsafe_allow_html=True)

# Data Definition
ROLES = {
    "AI & Machine Learning Engineer": {"Python Programming": 9, "Mathematical Foundations": 8, "Deep Learning": 7, "Cloud Deployment": 6, "Data Engineering": 7, "Soft Skills": 8},
    "Full Stack Developer": {"JavaScript/React": 9, "Backend (Node/Python)": 8, "Database Design": 8, "UI/UX Design": 6, "DevOps": 5, "Soft Skills": 9},
    "Data Scientist": {"Statistics": 9, "R/Python": 9, "Machine Learning": 8, "Data Visualization": 8, "SQL": 7, "Business Acumen": 8},
    "Cyber Security Analyst": {"Network Security": 9, "Cryptography": 7, "Ethical Hacking": 8, "Compliance/Risk": 6, "Linux/Shell": 8, "Incident Response": 7}
}

CHRIST_COURSES = {
    "Mathematical Foundations": ["Discrete Mathematics", "Statistics for MCA", "Applied Mathematics Bridge Course", "Math Lab - Problem Solving Session"],
    "Python Programming": ["Advanced Python Programming", "CU Python Developers Club", "Industry-led Python Workshops", "Open Source Contribution Initiative"],
    "Machine Learning": ["Machine Learning Techniques", "Data Science Research Group (DSRG)", "Machine Learning Seminar Series", "AI/ML Capstone Project Track"],
    "Cloud Deployment": ["Cloud Computing", "AWS Academy CU Partnership Track", "Infrastructure as Code (IaC) Workshop", "Cloud Migration Group Project"],
    "Network Security": ["Cyber Security Operations", "Network Defense and Countermeasures", "CU Cyber Security Cell (CSC)", "Ethical Hacking Lab Sessions", "Cyber Security Awareness Program"],
    "Database Design": ["Database Management Systems", "Advanced Database Systems (Elective)", "NoSQL Data Modeling Session", "SQL Certification Preparation Track"],
    "Deep Learning": ["Deep Learning for Vision Systems (Elective)", "Neural Networks Lab (MCA Part 2)", "AI Research Internship - CU Labs", "HuggingFace Transformers Workshop"],
    "Data Engineering": ["Big Data Analytics", "Data Warehousing and Mining", "CU Spark & Hadoop Cluster Access", "ETL Pipeline Design Competition"],
    "Soft Skills": ["Professional Communication", "Corporate Readiness Program (CRP)", "Technical Seminar Presentations", "Placement Cell - Mock Interview Drills", "Soft Skill Improvement Workshop"],
    "UI/UX Design": ["Web Technologies (MCA Part 1)", "CU Design Thinking Workshop", "Front-End Architecture Seminar", "HCI Interface Design Projects"],
    "Statistics": ["Probability and Statistics", "R for Statistical Computing (CU Lab)", "Data Visualization with R Workshop", "Quantitative Aptitude Training"],
    "JavaScript/React": ["Advanced Web Development (Elective)", "CU Full-Stack Bootcamp", "React.js Developer Guild", "MERN Stack Capstone Project"]
}

CERT_LINKS = {
    "Python Programming": [{"name": "Python for Everybody (Coursera)", "url": "https://www.coursera.org/specializations/python"}, {"name": "Official Python Documentation", "url": "https://docs.python.org/3/"}, {"name": "Real Python Tutorials", "url": "https://realpython.com/"}, {"name": "Google IT Automation with Python", "url": "https://www.coursera.org/professional-certificates/google-it-automation"}, {"name": "FreeCodeCamp Python Certification", "url": "https://www.freecodecamp.org/learn/scientific-computing-with-python/"}],
    "Deep Learning": [{"name": "Deep Learning Specialization (DeepLearning.AI)", "url": "https://www.deeplearning.ai/program/deep-learning-specialization/"}, {"name": "Fast.ai Practical Deep Learning", "url": "https://www.fast.ai/"}, {"name": "TensorFlow Developer Certificate", "url": "https://www.tensorflow.org/certificate"}, {"name": "PyTorch Tutorials", "url": "https://pytorch.org/tutorials/"}, {"name": "Stanford CS231n: CNNs", "url": "http://cs231n.stanford.edu/"}],
    "Machine Learning": [{"name": "Machine Learning Specialization (Stanford)", "url": "https://www.coursera.org/learn/machine-learning"}, {"name": "Karnel: ML on Kaggle", "url": "https://www.kaggle.com/learn/intro-to-machine-learning"}, {"name": "MLOps Specialization", "url": "https://www.deeplearning.ai/program/machine-learning-engineering-for-production-mlops/"}, {"name": "Scikit-Learn Documentation", "url": "https://scikit-learn.org/stable/"}, {"name": "Machine Learning Mastery", "url": "https://machinelearningmastery.com/"}],
    "Cloud Deployment": [{"name": "AWS Cloud Practitioner", "url": "https://aws.amazon.com/training/digital/cloud-practitioner-essentials/"}, {"name": "Google Cloud Professional Architect", "url": "https://cloud.google.com/certification/cloud-architect"}, {"name": "Microsoft Azure Fundamentals", "url": "https://learn.microsoft.com/en-us/training/courses/az-900t00"}, {"name": "Docker & Kubernetes Training", "url": "https://www.docker.com/101-tutorial/"}, {"name": "HashiCorp Terraform Cert", "url": "https://www.hashicorp.com/certification/terraform-associate"}],
    "Network Security": [{"name": "Google Cybersecurity Professional", "url": "https://www.coursera.org/google-cybersecurity"}, {"name": "CompTIA Security+", "url": "https://www.comptia.org/certifications/security"}, {"name": "Cisco CCNA Training", "url": "https://www.cisco.com/c/en/us/training-events/training-certifications/certifications/associate/ccna.html"}, {"name": "TryHackMe: Networking", "url": "https://tryhackme.com/path/outline/networks"}, {"name": "OWASP Top 10 Guide", "url": "https://owasp.org/www-project-top-ten/"}],
    "Data Visualization": [{"name": "Tableau Desktop Specialist", "url": "https://www.tableau.com/learn/training"}, {"name": "Power BI Data Analyst Associate", "url": "https://learn.microsoft.com/en-us/credentials/certifications/power-bi-data-analyst-associate/"}, {"name": "D3.js Graph Gallery", "url": "https://d3-graph-gallery.com/"}, {"name": "Storytelling with Data", "url": "https://www.storytellingwithdata.com/"}, {"name": "Google Data Analytics Cert", "url": "https://grow.google/certificates/data-analytics/"}],
    "UI/UX Design": [{"name": "Google UX Design Professional", "url": "https://www.coursera.org/professional-certificates/google-ux-design"}, {"name": "Figma UI Design Course", "url": "https://www.figma.com/resource-library/design-basics/"}, {"name": "Interaction Design Foundation", "url": "https://www.interaction-design.org/"}, {"name": "Adobe XD Tutorials", "url": "https://letsxd.com/learn"}, {"name": "Nielsen Norman Group Articles", "url": "https://www.nngroup.com/articles/"}],
    "Database Design": [{"name": "SQL for Data Science", "url": "https://www.coursera.org/learn/sql-for-data-science"}, {"name": "MongoDB University", "url": "https://university.mongodb.com/"}, {"name": "Database Design - Stanford Online", "url": "https://online.stanford.edu/courses/soe-ydatabases-databases"}, {"name": "PostgreSQL Tutorial", "url": "https://www.postgresqltutorial.com/"}, {"name": "Prisma Data Modeling Guide", "url": "https://www.prisma.io/dataguide/"}],
    "Ethical Hacking": [{"name": "Certified Ethical Hacker (CEH)", "url": "https://www.eccouncil.org/programs/certified-ethical-hacker-ceh/"}, {"name": "Offensive Security (OSCP)", "url": "https://www.offsec.com/courses/pen-200/"}, {"name": "Hack The Box Academy", "url": "https://academy.hackthebox.com/"}, {"name": "PortSwigger Web Security Academy", "url": "https://portswigger.net/web-security"}, {"name": "Cybrary: Ethical Hacking", "url": "https://www.cybrary.it/course/ethical-hacking/"}],
    "Mathematical Foundations": [{"name": "Mathematics for Machine Learning", "url": "https://www.coursera.org/specializations/mathematics-machine-learning"}, {"name": "Khan Academy: Linear Algebra", "url": "https://www.khanacademy.org/math/linear-algebra"}, {"name": "MIT OpenCourseWare: Calculus", "url": "https://ocw.mit.edu/courses/mathematics/18-01-single-variable-calculus-fall-2006/"}, {"name": "3Blue1Brown Essential Videos", "url": "https://www.youtube.com/c/3blue1brown"}, {"name": "Statistics and Probability (Khan Academy)", "url": "https://www.khanacademy.org/math/statistics-probability"}],
    "Soft Skills": [{"name": "Public Speaking Specialization", "url": "https://www.coursera.org/specializations/public-speaking"}, {"name": "Project Management Foundations", "url": "https://www.pmi.org/certifications/project-management-pmp"}, {"name": "Agile & Scrum (Atlassian)", "url": "https://www.atlassian.com/agile/scrum"}, {"name": "Effective Communication on edX", "url": "https://www.edx.org/course/effective-communication-for-today"}, {"name": "Emotional Intelligence at Work", "url": "https://www.linkedin.com/learning/topics/emotional-intelligence"}],
    "Data Engineering": [{"name": "Data Engineering Specialization (IBM)", "url": "https://www.coursera.org/professional-certificates/ibm-data-engineer"}, {"name": "Google Cloud Data Engineer Professional", "url": "https://cloud.google.com/certification/data-engineer"}, {"name": "Apache Spark Documentation", "url": "https://spark.apache.org/docs/latest/"}, {"name": "Data Warehousing (edX)", "url": "https://www.edx.org/course/data-warehousing-for-business-intelligence"}, {"name": "Modern Data Stack Guide", "url": "https://www.getorchestra.io/blog/modern-data-stack-guide"}]
}

# Sidebar & Header
with st.sidebar:
    st.image("https://christuniversity.in/images/logo.png", width=220)
    st.markdown('<div style="background:rgba(56,189,248,0.1);padding:1rem;border-radius:10px;border:1px solid rgba(56,189,248,0.2);margin-bottom:1.5rem;"><div style="font-size:0.8rem;font-weight:700;color:#38bdf8;text-transform:uppercase;">Institution</div><div style="font-size:0.9rem;color:#f1f5f9;margin-bottom:0.8rem;">CHRIST (Deemed to be University)</div><div style="font-size:0.8rem;font-weight:700;color:#38bdf8;text-transform:uppercase;">Department</div><div style="font-size:0.9rem;color:#f1f5f9;">Dept of Computer Science</div></div>', unsafe_allow_html=True)
    user_name = st.text_input("Name", "Ananya Shetty")
    role = st.selectbox("Target Career Path", list(ROLES.keys()))
    seniority = st.select_slider("Seniority Target", ["Entry", "Junior", "Associate"])
    mult = {"Entry": 0.8, "Junior": 1.0, "Associate": 1.2}[seniority]
    st.info(f"Target: **{seniority}** level")

st.markdown('<div class="header-container"><div class="title-text">Skill Gap Analyzer</div><div style="text-align:right;"><div style="font-size:0.9rem;opacity:0.9;">Master of Computer Applications (MCA)</div><div style="font-size:1.1rem;font-weight:700;">CHRIST (Deemed to be University)</div></div></div>', unsafe_allow_html=True)

# Main Dashboard
benchmarks = {k: min(10, round(v * mult, 1)) for k, v in ROLES[role].items()}
c1, c2 = st.columns([0.8, 1.4], gap="large")
with c1:
    st.markdown(f"#### Assessment: {role}")
    u_skills = {s: st.slider(f"**{s}** (Target: {b})", 0.0, 10.0, 4.0, 0.5) for s, b in benchmarks.items()}

with c2:
    fig = go.Figure([go.Bar(x=list(benchmarks.keys()), y=list(benchmarks.values()), name='Industry Target', marker_color='rgba(56,189,248,0.3)', marker_line=dict(color='#38bdf8', width=2)), go.Bar(x=list(u_skills.keys()), y=list(u_skills.values()), name='Your Proficiency', marker_color='#ef4444', marker_line=dict(color='white', width=1))])
    fig.update_layout(barmode='group', xaxis=dict(tickangle=-45, gridcolor="#334155"), yaxis=dict(range=[0, 10.5], gridcolor="#334155"), showlegend=True, legend=dict(orientation="h", y=1.02, x=1), margin=dict(l=40,r=40,t=60,b=100), font=dict(family="Outfit, sans-serif", color="#f1f5f9"), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', bargap=0.2, height=600)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# Metrics & Roadmaps
st.divider()
score = (sum(u_skills.values()) / sum(benchmarks.values())) * 100
st.markdown(f"### Career Readiness: **{score:.1f}%**")
st.progress(score / 100)
gaps = sorted([(s, benchmarks[s]-v) for s,v in u_skills.items() if v < benchmarks[s]], key=lambda x: x[1], reverse=True)
m1, m2, m3, m4 = st.columns(4)
m1.metric("Top Strength", max(u_skills, key=u_skills.get))
m2.metric("Top Gap", gaps[0][0] if gaps else "Ready!", delta=f"-{gaps[0][1]:.1f}" if gaps else "0", delta_color="inverse")
m3.metric("Target Avg", f"{np.mean(list(benchmarks.values())):.1f}/10")
m4.metric("Areas to Study", len(gaps))

st.header("Personalized Skill Hub")
r1, r2 = st.columns(2, gap="large")
with r1:
    st.markdown("### CHRIST University Courses")
    for s, _ in gaps:
        if s in CHRIST_COURSES:
            st.info(f"**{s}** Track:\n" + "\n".join([f"- {c}" for c in CHRIST_COURSES[s]]))
with r2:
    st.markdown("### Industry Link Hub")
    for s, _ in gaps:
        if s in CERT_LINKS:
            with st.expander(f"{s} Resources"):
                for link in CERT_LINKS[s]:
                    st.markdown(f'<a href="{link["url"]}" target="_blank" class="cert-link">{link["name"]} ↗</a>', unsafe_allow_html=True)

# Footer
st.markdown("<br><br><div style='background:#1e293b;color:#f1f5f9;padding:2rem;border-radius:20px;border:1px solid #334155;text-align:center;'><div style='font-weight:700;font-size:1.2rem;margin-bottom:0.5rem;color:#38bdf8;'>Skill Gap & Competency Analyzer</div><div style='opacity:0.8;font-size:0.9rem;color:#94a3b8;'>Dept of Computer Science | CHRIST (Deemed to be University)<br>MCA Program Research Initiative</div></div>", unsafe_allow_html=True)
