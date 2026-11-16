
import streamlit as st
import csv
import os
from utils.ai_summarizer import generate_quiz


# CSV file location
HISTORY_FILE = os.path.join("data", "quiz_history.csv")

# Create data folder if it doesn't exist
os.makedirs("data", exist_ok=True)


# Load previous quiz attempts
def load_quiz_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            history = []

            for row in reader:
                history.append({
                    "attempt": int(row["attempt"]),
                    "score": int(row["score"]),
                    "total": int(row["total"]),
                    "percentage": float(row["percentage"])
                })

            return history

    return []

# Save quiz history to CSV
def save_quiz_history(history):
    with open(HISTORY_FILE, "w", newline="", encoding="utf-8") as file:
        fieldnames = ["attempt", "score", "total", "percentage"]

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(history)

st.title("AI Quiz Generator")

# Initialize quiz history
if "quiz_history" not in st.session_state:
    st.session_state["quiz_history"] = load_quiz_history()

st.write("Test your knowledge with multiple-choice questions.")
st.divider()

study_text = st.session_state.get("study_text", "")

if not study_text:
    st.warning("Please upload a PDF first in Study Materials.")

else:
    st.success("Study material found!")

    # Initialize quiz attempt ID
    if "quiz_attempt_id" not in st.session_state:
        st.session_state["quiz_attempt_id"] = 0

    # Generate Quiz
    if st.button("Generate AI Quiz", key="generate_quiz"):
        with st.spinner("Generating questions from your study material..."):
            try:
                questions = generate_quiz(
                    study_text,
                    number_of_questions=5
                )

                st.session_state["quiz_questions"] = questions
                st.session_state["quiz_submitted"] = False
                st.session_state["quiz_attempt_id"] += 1

            except Exception as error:
                st.error(f"Quiz generation failed: {error}")

    # Display Quiz
    questions = st.session_state.get("quiz_questions", [])

    if questions:
        st.subheader("Practice Quiz")

        user_answers = {}
        attempt_id = st.session_state["quiz_attempt_id"]

        # Display questions
        for i, question in enumerate(questions):
            question_text = question["question"].replace("**", "")
            st.write(f"Q{i + 1}. {question_text}")

            user_answers[i] = st.radio(
                "Choose your answer:",
                question["options"],
                index=None,
                key=f"quiz_{attempt_id}_{i}",
                disabled=st.session_state.get("quiz_submitted", False)
            )

        
        # Submit Quiz
        if not st.session_state.get("quiz_submitted", False):
            if st.button("Submit Quiz", key="submit_quiz"):

                if any(answer is None for answer in user_answers.values()):
                    st.warning("Please answer all questions before submitting.")

                else:
                    score = sum(
                        1 for i, question in enumerate(questions)
                        if user_answers[i] == question["answer"]
                    )

                    total = len(questions)
                    percentage = (score / total) * 100

                    st.session_state["quiz_submitted"] = True

                    # Create new attempt
                    new_attempt = {
                        "attempt": len(st.session_state["quiz_history"]) + 1,
                        "score": score,
                        "total": total,
                        "percentage": percentage
                    }

                    # Add attempt to history
                    st.session_state["quiz_history"].append(new_attempt)

                    # Save history permanently
                    save_quiz_history(st.session_state["quiz_history"])

                    # Update latest score
                    st.session_state["latest_quiz_score"] = score
                    st.session_state["latest_quiz_total"] = total
                    st.session_state["latest_quiz_percentage"] = percentage

                    st.rerun()

        # Display Results
        if st.session_state.get("quiz_submitted", False):

            score = st.session_state["latest_quiz_score"]
            percentage = st.session_state["latest_quiz_percentage"]

            st.divider()
            st.subheader("Your Results")

            st.write(f"Your score: {score}/{len(questions)}")
            st.progress(percentage / 100)

            if percentage >= 80:
                st.success("Excellent work!")
            elif percentage >= 50:
                st.info("Good effort! Keep practising.")
            else:
                st.warning("Keep studying and try again.")

            st.subheader("Answer Review")

            for i, question in enumerate(questions):
                question_text = question["question"].replace("**", "")
                st.write(f"Q{i + 1}. {question_text}")

                if user_answers[i] == question["answer"]:
                    st.success("Correct answer!")
                else:
                    st.error(
                        f"Incorrect. Correct answer: {question['answer']}"
                    )

                st.write(f"Explanation: {question['explanation']}")

            # Retake Quiz
            if st.button("Retake Quiz", key="retake_quiz"):
                st.session_state["quiz_attempt_id"] += 1
                st.session_state["quiz_submitted"] = False
                st.rerun()
