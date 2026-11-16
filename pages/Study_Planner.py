
import streamlit as st
import csv
import os
from datetime import date

st.title("Study Planner")

st.write("Organize your subjects, tasks, and study deadlines.")
st.divider()

# CSV file locations
TASK_FILE = os.path.join("data", "study_tasks.csv")
ACTIVITY_FILE = os.path.join("data", "study_activity.csv")

# Create data folder
os.makedirs("data", exist_ok=True)


# Load saved tasks
def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            tasks = []

            for row in reader:
                tasks.append({
                    "task_name": row["task_name"],
                    "subject": row["subject"],
                    "due_date": date.fromisoformat(row["due_date"]),
                    "priority": row["priority"],
                    "completed": row["completed"].lower() == "true"
                })

            return tasks

    return []


# Save tasks to CSV
def save_tasks(tasks):
    with open(TASK_FILE, "w", newline="", encoding="utf-8") as file:
        fieldnames = [
            "task_name",
            "subject",
            "due_date",
            "priority",
            "completed"
        ]

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for task in tasks:
            writer.writerow({
                "task_name": task["task_name"],
                "subject": task["subject"],
                "due_date": task["due_date"].isoformat(),
                "priority": task["priority"],
                "completed": task["completed"]
            })


# Record a completed task in the activity history
def record_activity(task_name):
    today = date.today().isoformat()

    # Avoid recording the same task twice on the same day
    if os.path.exists(ACTIVITY_FILE):
        with open(ACTIVITY_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                if (
                    row["date"] == today
                    and row["task_name"] == task_name
                ):
                    return

    file_exists = os.path.exists(ACTIVITY_FILE)

    with open(ACTIVITY_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["date", "task_name"]
        )

        if not file_exists or os.path.getsize(ACTIVITY_FILE) == 0:
            writer.writeheader()

        writer.writerow({
            "date": today,
            "task_name": task_name
        })


# Initialize task storage
if "study_tasks" not in st.session_state:
    st.session_state["study_tasks"] = load_tasks()


# Add a new task
st.subheader("Add a Study Task")

with st.form("study_task_form"):

    task_name = st.text_input("Task Name")
    subject = st.text_input("Subject")

    due_date = st.date_input(
        "Due Date",
        value=date.today()
    )

    priority = st.selectbox(
        "Priority",
        ["High", "Medium", "Low"]
    )

    submitted = st.form_submit_button("Add Task")

    if submitted:
        if task_name.strip() and subject.strip():

            task = {
                "task_name": task_name.strip(),
                "subject": subject.strip(),
                "due_date": due_date,
                "priority": priority,
                "completed": False
            }

            st.session_state["study_tasks"].append(task)

            save_tasks(st.session_state["study_tasks"])

            st.success("Study task added successfully!")

        else:
            st.error("Please enter both task name and subject.")


# Display tasks
st.divider()
st.subheader("My Study Tasks")

tasks = st.session_state["study_tasks"]

if tasks:

    completed_count = sum(
        1 for task in tasks if task["completed"]
    )

    total_tasks = len(tasks)

    st.write(f"Completed: {completed_count}/{total_tasks}")

    st.progress(completed_count / total_tasks)

    for i, task in enumerate(tasks):

        st.write(f"**Task {i + 1}: {task['task_name']}**")
        st.write(f"Subject: {task['subject']}")
        st.write(f"Due Date: {task['due_date']}")
        st.write(f"Priority: {task['priority']}")

        if not task["completed"]:
            if task["due_date"] < date.today():
                st.error("Overdue!")
            elif task["due_date"] == date.today():
                st.warning("Due Today!")
            else:
                st.info("Upcoming")

        # Completion checkbox
        is_completed = st.checkbox(
            "Mark as completed",
            value=task["completed"],
            key=f"task_completed_{i}"
        )

        # Save completion changes and record activity
        if is_completed != task["completed"]:

            if is_completed:
                record_activity(task["task_name"])

            task["completed"] = is_completed

            save_tasks(st.session_state["study_tasks"])

        # Delete task
        if st.button("Delete Task", key=f"delete_task_{i}"):

            st.session_state["study_tasks"].pop(i)

            save_tasks(st.session_state["study_tasks"])

            st.rerun()

        st.divider()

else:
    st.info("No study tasks added yet. Add your first task above!")
