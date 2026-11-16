
import streamlit as st
import csv
import os
from datetime import date, timedelta

st.title("Progress Dashboard")

st.write("Track your study progress and performance.")

st.divider()

# Get study tasks
tasks = st.session_state.get("study_tasks", [])

# Calculate task statistics
total_tasks = len(tasks)

completed_tasks = sum(
    1 for task in tasks if task["completed"]
)

pending_tasks = total_tasks - completed_tasks

progress = (
    completed_tasks / total_tasks
    if total_tasks > 0 else 0
)

# Display statistics
st.subheader("Study Task Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Tasks", total_tasks)
col2.metric("Completed", completed_tasks)
col3.metric("Pending", pending_tasks)

st.subheader("Overall Study Progress")

st.progress(progress)

st.write(f"Completion: {progress * 100:.1f}%")

st.divider()

st.subheader("Task Completion Chart")

if total_tasks > 0:
    chart_data = {
        "Status": ["Completed", "Pending"],
        "Tasks": [completed_tasks, pending_tasks]
    }

    st.bar_chart(
        chart_data,
        x="Status",
        y="Tasks"
    )
else:
    st.info("Add study tasks in the Study Planner to see your chart.")

st.divider()

st.subheader("AI Quiz Performance")

quiz_score = st.session_state.get("latest_quiz_score")
quiz_total = st.session_state.get("latest_quiz_total")
quiz_percentage = st.session_state.get("latest_quiz_percentage")

if (
    quiz_score is not None
    and quiz_total is not None
    and quiz_percentage is not None
):

    st.metric(
        "Quiz Percentage",
        f"{quiz_percentage:.1f}%"
    )

    st.progress(quiz_percentage / 100)
else:
    st.info("Complete an AI quiz to see your quiz performance here.")

st.divider()
st.subheader("Quiz Attempt History")

quiz_history = st.session_state.get("quiz_history", [])

if quiz_history:
    for attempt in quiz_history:
        st.write(
            f"Attempt {attempt['attempt']}: "
            f"{attempt['score']}/{attempt['total']} "
            f"({attempt['percentage']:.1f}%)"
        )
else:
    st.info("No quiz attempts recorded yet.")

# ==================================
# STUDY STREAK TRACKING
# ==================================

st.divider()
st.subheader("🔥 Study Streak Tracking")

ACTIVITY_FILE = os.path.join("data", "study_activity.csv")

# Load study activity dates
activity_dates = []

if os.path.exists(ACTIVITY_FILE):
    with open(ACTIVITY_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            activity_dates.append(
                date.fromisoformat(row["date"])
            )

# Remove duplicate dates
unique_dates = sorted(set(activity_dates))

today = date.today()

# Calculate current streak
current_streak = 0

if unique_dates:
    latest_activity = unique_dates[-1]

    if latest_activity >= today - timedelta(days=1):
        check_date = latest_activity

        while check_date in unique_dates:
            current_streak += 1
            check_date -= timedelta(days=1)

# Calculate longest streak
longest_streak = 0
streak = 0
previous_date = None

for activity_date in unique_dates:

    if (
        previous_date is not None
        and activity_date == previous_date + timedelta(days=1)
    ):
        streak += 1
    else:
        streak = 1

    longest_streak = max(longest_streak, streak)
    previous_date = activity_date

# Display streak statistics
col1, col2, col3 = st.columns(3)

col1.metric("Current Streak", f"{current_streak} days")
col2.metric("Longest Streak", f"{longest_streak} days")
col3.metric("Total Study Days", len(unique_dates))

# Activity calendar
st.subheader("Study Activity Calendar")
st.caption("🟩 Completed tasks  ⬜ No recorded activity")

# Display the last 35 days
calendar_dates: list[date | None] = [
    today - timedelta(days=i)
    for i in range(34, -1, -1)
]

# Pad calendar to start on Monday
while (
    calendar_dates[0] is not None
    and calendar_dates[0].weekday() != 0
):
    calendar_dates.insert(0, None)

# Pad calendar to finish on Sunday
while len(calendar_dates) % 7 != 0:
    calendar_dates.append(None)

day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

header_cols = st.columns(7)

for col, day_name in zip(header_cols, day_names):
    col.markdown(f"**{day_name}**")

for week_start in range(0, len(calendar_dates), 7):

    week = calendar_dates[week_start:week_start + 7]
    cols = st.columns(7)

    for col, calendar_day in zip(cols, week):

        if calendar_day is None or calendar_day > today:
            col.write(" ")
        elif calendar_day in unique_dates:
            col.markdown(f"🟩 **{calendar_day.day}**")
        else:
            col.markdown(f"⬜ {calendar_day.day}")

if not unique_dates:
    st.info("Complete a study task to start your study streak!")

# ==================================
# SUBJECT-WISE PROGRESS ANALYTICS
# ==================================

st.divider()
st.subheader("📚 Subject-wise Progress Analytics")

tasks = st.session_state.get("study_tasks", [])

if tasks:

    subject_stats = {}

    # Calculate task statistics for each subject
    for task in tasks:

        subject = task["subject"].strip()

        if not subject:
            subject = "Uncategorized"

        if subject not in subject_stats:
            subject_stats[subject] = {
                "Total": 0,
                "Completed": 0,
                "Pending": 0
            }

        subject_stats[subject]["Total"] += 1

        if task["completed"]:
            subject_stats[subject]["Completed"] += 1
        else:
            subject_stats[subject]["Pending"] += 1

    # Prepare chart data
    subjects = list(subject_stats.keys())

    completed_data = [
        subject_stats[subject]["Completed"]
        for subject in subjects
    ]

    pending_data = [
        subject_stats[subject]["Pending"]
        for subject in subjects
    ]

    # Display subject-wise statistics
    st.write("### Subject Performance")

    for subject, stats in subject_stats.items():

        st.write(f"**{subject}**")

        st.write(
            f"Completed: {stats['Completed']} / "
            f"{stats['Total']}"
        )

        subject_progress = (
            stats["Completed"] / stats["Total"]
        )

        st.progress(subject_progress)

        st.caption(
            f"Pending: {stats['Pending']} tasks"
        )

    # Display comparison chart
    st.write("### Subject Comparison")

    chart_data = {
        "Subject": subjects,
        "Completed": completed_data,
        "Pending": pending_data
    }

    st.bar_chart(
        chart_data,
        x="Subject",
        y=["Completed", "Pending"]
    )

else:
    st.info("Add study tasks to see subject-wise analytics.")
