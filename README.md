# Personal AI Study Assistant 

A Python-based study assistant built with Streamlit that helps students organize study materials, generate quizzes, manage study tasks, and monitor their learning progress.

## Features

### 1. Study Materials
- Upload PDF study materials.
- Extract text from PDF files.
- Generate summaries using TF-IDF-based extractive summarization.

### 2. Offline Quiz Generator
- Generate multiple-choice questions from uploaded study materials.
- Randomize answer options.
- Submit answers and view results.
- Review correct answers and explanations.

### 3. Study Planner
- Add study tasks with subjects and deadlines.
- Assign task priorities (High, Medium, Low).
- Mark tasks as completed.
- Delete tasks.
- Save tasks using CSV file storage.

### 4. Progress Dashboard
- View total, completed, and pending tasks.
- Monitor overall study progress.
- Track quiz scores and attempt history.
- Calculate current and longest study streaks.
- View a study activity calendar.
- Analyze progress by subject.

##  Technologies Used

- **Programming Language:** Python
- **Frontend:** Streamlit
- **Data Processing:** Pandas, NumPy
- **Machine Learning / NLP:** Scikit-learn (TF-IDF)
- **PDF Processing:** pypdf
- **Data Storage:** CSV
- **Version Control:** Git and GitHub

##  Project Structure

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

##  Installation and Setup

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

Windows:

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

The application will open in your browser.

##  Data Storage

The application uses CSV files to store:
- Study tasks
- Quiz attempt history
- Study activity records

These files are generated locally when the application is used.

##  Project Objective

The main objective of this project is to provide students with a simple and accessible platform for managing study materials, practicing through quizzes, organizing tasks, and tracking academic progress.

##  Author

**Computer Engineering Student**

##  Future Improvements

- Enhanced quiz generation and question quality.
- More detailed learning analytics.
- Improved user interface.
- Additional study productivity features.