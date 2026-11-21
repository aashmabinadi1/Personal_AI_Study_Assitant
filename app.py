
import streamlit as st
import csv
import os
from textwrap import dedent

st.set_page_config(
    page_title="Personal AI Study Assistant",
    page_icon="📚",
    layout="wide"
)

# --------------------------------------------------
# Custom CSS
# --------------------------------------------------

st.markdown(dedent("""
<style>

    .stApp {
        background-color: #f5f7fb;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #101d35;
    }

    [data-testid="stSidebar"] * {
        color: #ffffff;
    }

    /* Hero section */
    .hero {
        background: linear-gradient(120deg, #101d35, #254b75);
        padding: 42px 40px;
        border-radius: 18px;
        margin-bottom: 32px;
    }

    .hero-label {
        color: #a9c9ef;
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 2px;
        margin-bottom: 12px;
    }

    .hero h1 {
        color: #ffffff;
        font-size: 36px;
        font-weight: 750;
        margin-bottom: 12px;
    }

    .hero p {
        color: #d5e1f0;
        font-size: 16px;
        line-height: 1.7;
        max-width: 700px;
        margin-bottom: 0;
    }

    /* Section headings */
    .section-heading {
        color: #172b4d;
        font-size: 23px;
        font-weight: 700;
        margin-top: 12px;
        margin-bottom: 5px;
    }

    .section-description {
        color: #718096;
        font-size: 14px;
        margin-bottom: 20px;
    }

    /* Feature cards */
    .feature-card {
        background-color: #ffffff;
        border: 1px solid #e5eaf2;
        border-radius: 15px;
        padding: 24px;
        min-height: 185px;
        margin-bottom: 10px;
        box-shadow: 0 3px 12px rgba(20, 40, 70, 0.035);
        transition: all 0.2s ease;
    }

    .feature-card:hover {
        border-color: #8baed8;
        box-shadow: 0 6px 18px rgba(20, 40, 70, 0.08);
        transform: translateY(-2px);
    }

    .feature-icon {
        font-size: 25px;
        margin-bottom: 12px;
    }

    .feature-card h3 {
        color: #1e3557;
        font-size: 19px;
        font-weight: 650;
        margin-bottom: 9px;
    }

    .feature-card p {
        color: #718096;
        font-size: 14px;
        line-height: 1.65;
        margin-bottom: 0;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e5eaf2;
        border-radius: 13px;
        padding: 17px 18px;
        box-shadow: 0 2px 8px rgba(20, 40, 70, 0.03);
    }

    [data-testid="stMetricLabel"] {
        color: #718096;
    }

    [data-testid="stMetricValue"] {
        color: #172b4d;
        font-weight: 700;
    }

    /* Navigation links */
[data-testid="stPageLink"] {
    background-color: #ffffff;
    border: 1px solid #dce5f0;
    border-radius: 9px;
    padding: 8px 12px;
}

[data-testid="stPageLink"] a,
[data-testid="stPageLink"] a p,
[data-testid="stPageLink"] a span {
    color: #1e3557 !important;
}

[data-testid="stPageLink"] a svg {
    color: #1e3557 !important;
    fill: #1e3557 !important;
}
    }

    /* Study tip */
    .tip-card {
        background-color: #eaf2fb;
        border-left: 4px solid #3975b9;
        border-radius: 9px;
        padding: 19px 22px;
        color: #294766;
        font-size: 15px;
        line-height: 1.7;
    }

</style>
"""), unsafe_allow_html=True)


# --------------------------------------------------
# Load dashboard data
# --------------------------------------------------

def load_csv_data(file_path):

    if os.path.exists(file_path):

        try:
            with open(
                file_path,
                "r",
                newline="",
                encoding="utf-8"
            ) as file:

                return list(csv.DictReader(file))

        except (OSError, csv.Error):
            return []

    return []


tasks = load_csv_data("data/study_tasks.csv")
quiz_history = load_csv_data("data/quiz_history.csv")

total_tasks = len(tasks)

completed_tasks = sum(
    1 for task in tasks
    if task.get("completed", "").lower() == "true"
)

total_quizzes = len(quiz_history)

latest_score = "—"

if quiz_history:

    try:
        latest_score = (
            f"{float(quiz_history[-1]['percentage']):.1f}%"
        )

    except (ValueError, KeyError, TypeError):
        latest_score = "—"


# --------------------------------------------------
# Hero section
# --------------------------------------------------

st.html("""
<div class="hero">

    <div class="hero-label">
        YOUR PERSONAL LEARNING SPACE
    </div>

    <h1>Welcome to Your Study Dashboard</h1>

    <p>
        Organize your study materials, practice with AI-generated
        quizzes, plan your learning schedule, and track your
        academic progress — all in one place.
    </p>

</div>
""")


# --------------------------------------------------
# Study overview
# --------------------------------------------------

st.markdown(
    '<div class="section-heading">Your Study Overview</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'A quick look at your learning activity.'
    '</div>',
    unsafe_allow_html=True
)

metric1, metric2, metric3, metric4 = st.columns(4)

metric1.metric("Total Tasks", total_tasks)
metric2.metric("Completed Tasks", completed_tasks)
metric3.metric("Quiz Attempts", total_quizzes)
metric4.metric("Latest Quiz Score", latest_score)


st.write("")
st.divider()



# --------------------------------------------------
# Learning features
# --------------------------------------------------

st.markdown(
    '<div class="section-heading">Explore Your Learning Tools</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Choose a tool to continue your learning journey.'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# First row of feature cards
# --------------------------------------------------

col1, col2 = st.columns(2, gap="large")

with col1:

    st.html("""
    <div class="feature-card">
        <div class="feature-icon"></div>
        <h3>Study Materials</h3>
        <p>
            Upload and organize PDF documents, extract
            their content, and generate concise study summaries.
        </p>
    </div>
    """)

    st.page_link(
        "pages/Study_Materials.py",
        label="Explore Study Materials",
        icon=":material/menu_book:",
        use_container_width=True
    )


with col2:

    st.html("""
    <div class="feature-card">
        <div class="feature-icon"></div>
        <h3>Automatically generated quizzes</h3>
        <p>
            Generate multiple-choice questions from your
            study materials and evaluate your knowledge.
        </p>
    </div>
    """)

    st.page_link(
        "pages/AI_QUIZ_generator.py",
        label="Practice with Quizzes",
        icon=":material/quiz:",
        use_container_width=True
    )


st.write("")


# --------------------------------------------------
# Second row of feature cards
# --------------------------------------------------

col3, col4 = st.columns(2, gap="large")

with col3:

    st.html("""
    <div class="feature-card">
        <div class="feature-icon"></div>
        <h3>Study Planner</h3>
        <p>
            Organize study tasks, set deadlines, manage priorities,
            and keep track of your daily learning goals.
        </p>
    </div>
    """)

    st.page_link(
        "pages/Study_Planner.py",
        label="Plan Your Studies",
        icon=":material/calendar_month:",
        use_container_width=True
    )


with col4:

    st.html("""
    <div class="feature-card">
        <div class="feature-icon"></div>
        <h3>Progress Dashboard</h3>
        <p>
            Monitor quiz performance, study streaks,
            completed tasks, and subject-wise progress.
        </p>
    </div>
    """)

    st.page_link(
        "pages/Progress_Dashboard.py",
        label="View Your Progress",
        icon=":material/analytics:",
        use_container_width=True
    )


# --------------------------------------------------
# Study tip
# --------------------------------------------------

st.write("")
st.divider()

st.markdown(
    '<div class="section-heading">A Little Study Motivation</div>',
    unsafe_allow_html=True
)

st.html("""
<div class="tip-card">

    <strong>Consistency is more important than intensity.</strong>

    <br>

    Set small daily goals, stay organized, and make steady
    progress toward your learning objectives.

</div>
""")


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.write("")

st.markdown(
    "<center style='color:#8794a8; font-size:13px;'>"
    "Personal AI Study Assistant | Built with Python and Streamlit"
    "</center>",
    unsafe_allow_html=True
)
