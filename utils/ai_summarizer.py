import numpy as np
import random
import re
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer


@st.cache_data(ttl=3600, max_entries=5)
def summarize_text(text, number_of_sentences=8):

    # Split text into individual sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)

    sentences = [
        sentence.strip()
        for sentence in sentences
        if len(sentence.strip().split()) > 4
    ]

    if not sentences:
        return "Not enough text to generate a summary."

    if len(sentences) <= number_of_sentences:
        return "\n\n".join(sentences)

    # Calculate sentence importance using TF-IDF
    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    try:
        tfidf_matrix = vectorizer.fit_transform(sentences)
    except ValueError:
        return "Unable to summarize this text."

    # Calculate importance score for each sentence
    
    
# Convert the TF-IDF sparse matrix into a normal NumPy array
    dense_matrix = tfidf_matrix.toarray()  # type: ignore[attr-defined]

# Calculate the score of each sentence
    sentence_scores = np.sum(dense_matrix, axis=1)
   

    # Select the most important sentences
    ranked_sentences = sorted(
        enumerate(sentence_scores),
        key=lambda item: item[1],
        reverse=True
    )

    selected_indices = sorted(
        index for index, score in ranked_sentences[:number_of_sentences]
    )

    summary = [
        sentences[index]
        for index in selected_indices
    ]

    return "\n\n".join(summary)



def generate_quiz(study_text, number_of_questions=5):
    sentences = re.split(r'(?<=[.!?])\s+', study_text)

    sentences = [
        sentence.strip()
        for sentence in sentences
        if len(sentence.strip().split()) >= 6
    ]

    if not sentences:
        return []

    # Extract meaningful words from the study material
    stop_words = {
        "which", "where", "when", "what", "this", "that",
        "with", "from", "have", "their", "there", "these",
        "those", "about", "into", "also", "such", "than",
        "then", "them", "they", "were", "been", "being",
        "will", "would", "could", "should", "does", "used"
    }

    important_words = []

    for sentence in sentences:
        for word in re.findall(r'\b[A-Za-z][A-Za-z-]*\b', sentence):
            clean_word = word.strip(".,!?;:()[]{}")

            if (
                len(clean_word) > 4
                and clean_word.lower() not in stop_words
                and clean_word.lower() not in [
                    w.lower() for w in important_words
                ]
            ):
                important_words.append(clean_word)

    if not important_words:
        return []

    questions = []
    used_sentences = set()

    for sentence in sentences:

        # Stop after reaching the requested number of questions
        if len(questions) >= number_of_questions:
            break

        # Avoid duplicate questions
        if sentence.lower() in used_sentences:
            continue

        used_sentences.add(sentence.lower())

        words = re.findall(r'\b[A-Za-z][A-Za-z-]*\b', sentence)

        answer = next(
            (
                word for word in words
                if word in important_words
            ),
            None
        )

        if not answer:
            continue

        distractors = [
            word for word in important_words
            if word.lower() != answer.lower()
        ][:3]

        options = [answer] + distractors
        options = list(dict.fromkeys(options))

        if len(options) < 2:
            continue

        random.shuffle(options)

        questions.append({
            "question": (
                f"Which term correctly completes this statement?\n\n"
                f"{sentence.replace(answer, '__________', 1)}"
            ),
            "options": options,
            "answer": answer,
            "explanation": sentence
        })

    return questions
