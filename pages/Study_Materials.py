import streamlit as st

from utils.Pdf_read import extract_text_from_pdf

st.title("Study Materials Manager")

st.write("Upload your study PDF and extract its text.")

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"]
)

if uploaded_file is not None:

    extracted_text = extract_text_from_pdf(uploaded_file)

    if extracted_text.strip():
        st.success("PDF uploaded successfully!")
        st.subheader("Extracted Content")
        st.text_area(
            "PDF Text",
            extracted_text,
            height=400
        )
    else:
        st.warning("No readable text found in this PDF.")