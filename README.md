# Personal AI Study Assistant

A Python-based study assistant built with Streamlit to help students manage study materials, generate practice quizzes, organize study tasks, and track learning progress.

## Features

### 1. Study Materials
- Upload and manage PDF study materials.
- Extract text from PDF documents.
- Generate concise summaries using TF-IDF-based extractive summarization.
- Maintain a personal study materials library.

### 2. Offline Quiz Generator
- Generate multiple-choice questions from selected study materials.
- Randomize answer options.
- Submit answers and view quiz scores.
- Review correct answers and explanations.
- Maintain quiz attempt history.

### 3. Study Planner
- Create study tasks with subjects and deadlines.
- Assign task priorities: High, Medium, and Low.
- Mark tasks as completed.
- Monitor pending and completed tasks.
- Store task information using CSV files.

### 4. Progress Dashboard
- View total, completed, and pending tasks.
- Monitor overall study progress.
- Track quiz scores and attempt history.
- Calculate current and longest study streaks.
- View a study activity calendar.
- Analyze progress by subject.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Web application framework |
| NumPy | Numerical operations |
| Scikit-learn | TF-IDF-based text summarization |
| pypdf | PDF text extraction |
| CSV and JSON | Local data storage |
| Git and GitHub | Version control |

## Project Structure

```text
Personal_AI_Study_Assistant/
│
├── app.py
├── pages/
│   ├── Study_Materials.py
│   ├── AI_QUIZ_generator.py
│   ├── Study_Planner.py
│   └── Progress_Dashboard.py
│
├── utils/
│   ├── Pdf_read.py
│   └── ai_summarizer.py
│
├── assets/
├── tests/
├── data/
├── .streamlit/
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/aashmabinadi1/Personal_AI_Study_Assitant.git
```

### 2. Navigate to the project folder

```bash
cd Personal_AI_Study_Assitant
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

**Windows:**

```bash
.venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
streamlit run app.py
```

The application will open in your web browser.

## Data Storage

The application uses local CSV and JSON files to store:
- Study tasks
- Quiz attempt history
- Study activity records
- Saved study materials and summaries

These files are generated locally while using the application.

## Project Objective

The objective of this project is to provide students with an accessible platform for managing learning resources, practicing through automatically generated quizzes, organizing study schedules, and monitoring academic progress.

## Future Improvements

- Enhance quiz generation and question quality.
- Introduce more detailed learning analytics.
- Improve the user interface and user experience.
- Add additional study productivity features.

## Author

**Aashma Binadi**  
Computer Engineering Student
