
import streamlit as st
import csv
import os

st.set_page_config(
    page_title="Personal AI Study Assistant",
    page_icon="📚",
    layout="wide"
)

# Custom styling
st.markdown("""
<style>
    .stApp {
        background-color: #f7f9fc;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .hero {
        background: linear-gradient(120deg, #172b4d, #254b75);
        padding: 42px 38px;
        border-radius: 16px;
        color: white;
        margin-bottom: 30px;
    }

    .hero h1 {
        color: white;
        font-size: 36px;
        font-weight: 700;
        margin-bottom: 12px;
    }

    .hero p {
        color: #dce6f2;
        font-size: 17px;
        margin-bottom: 0;
    }

    .feature-card {
        background: white;
        padding: 25px;
        border: 1px solid #e3eaf2;
        border-radius: 14px;
        min-height: 165px;
        box-shadow: 0 2px 8px rgba(20, 40, 70, 0.04);
    }

    .feature-card h3 {
        color: #1e3557;
        font-size: 20px;
        margin-bottom: 12px;
    }

    .feature-card p {
        color: #64748b;
        font-size: 15px;
        line-height: 1.6;
    }

    .section-title {
        color: #1e3557;
        font-size: 23px;
        font-weight: 650;
        margin-bottom: 8px;
    }

    .tip-card {
        background: #eaf2fb;
        border-left: 4px solid #3975b9;
        padding: 18px 22px;
        border-radius: 8px;
        color: #294766;
    }
</style>
""", unsafe_allow_html=True)

# Hero section
st.markdown("""
<div class="hero">
    <h1>Personal AI Study Assistant</h1>
    <p>
        Your intelligent learning companion to organize study materials,
        practice quizzes, manage tasks, and monitor academic progress.
    </p>
</div>
""", unsafe_allow_html=True)

# Welcome section
st.markdown(
    '<div class="section-title">Welcome to Your Learning Dashboard</div>',
    unsafe_allow_html=True
)

st.write(
    "Everything you need to make your learning process "
    "more organized and productive."
)


st.divider()

# Quick Overview
st.markdown(
    '<div class="section-title">Your Study Overview</div>',
    unsafe_allow_html=True
)

def load_csv_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", newline="", encoding="utf-8") as file:
            return list(csv.DictReader(file))
    return []

tasks = load_csv_data("data/study_tasks.csv")
quiz_history = load_csv_data("data/quiz_history.csv")

total_tasks = len(tasks)

completed_tasks = sum(
    1 for task in tasks
    if task.get("completed", "").lower() == "true"
)

total_quizzes = len(quiz_history)

latest_score = (
    f"{float(quiz_history[-1]['percentage']):.1f}%"
    if quiz_history else "—"
)

metric1, metric2, metric3, metric4 = st.columns(4)

metric1.metric("Total Tasks", total_tasks)
metric2.metric("Completed Tasks", completed_tasks)
metric3.metric("Quiz Attempts", total_quizzes)
metric4.metric("Latest Quiz Score", latest_score)

st.divider()



# Feature cards
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>Study Materials</h3>
        <p>
            Upload PDF documents, extract their content,
            and generate concise study summaries.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.page_link(
        "pages/Study_Materials.py",
        label="Open Study Materials",
        icon=":material/menu_book:"
    )

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>Quiz Generator</h3>
        <p>
            Generate practice multiple-choice questions
            from your study materials and evaluate your knowledge.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.page_link(
        "pages/AI_QUIZ_generator.py",
        label="Open Quiz Generator",
        icon=":material/quiz:"
    )

st.write("")

col3, col4 = st.columns(2, gap="large")

with col3:
    st.markdown("""
    <div class="feature-card">
        <h3>Study Planner</h3>
        <p>
            Organize study tasks, set deadlines,
            and keep track of your daily learning goals.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.page_link(
        "pages/Study_Planner.py",
        label="Open Study Planner",
        icon=":material/calendar_month:"
    )

with col4:
    st.markdown("""
    <div class="feature-card">
        <h3>Progress Dashboard</h3>
        <p>
            Monitor quiz performance, study streaks,
            and subject-wise learning progress.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.page_link(
        "pages/Progress_Dashboard.py",
        label="Open Progress Dashboard",
        icon=":material/analytics:"
    )


# Study tip
st.markdown(
    '<div class="section-title">Study Tip</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="tip-card">
    Consistent learning and small daily goals can help build
    effective study habits over time.
</div>
""", unsafe_allow_html=True)

st.write("")
st.caption(
    "Personal AI Study Assistant | Developed with Python and Streamlit"
)
