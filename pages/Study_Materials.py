import streamlit as st
from utils.Pdf_read import extract_text_from_pdf
from utils.ai_summarizer import summarize_text

st.title("Personal AI Study Assistant")
st.header("Study Materials Manager")

st.write("Upload your PDF and generate an AI-powered summary.")

uploaded_file = st.file_uploader(
   "Upload your study PDF (Maximum 50 MB)",
    type=["pdf"]
)

if uploaded_file is not None:

    extracted_text = extract_text_from_pdf(uploaded_file)
    st.session_state["study_text"] = extracted_text

    if extracted_text.strip():

        st.success("PDF uploaded and text extracted successfully!")

        with st.expander("View Extracted Text"):
            st.text_area(
                "PDF Content",
                extracted_text,
                height=300
            )

        if st.button("Generate AI Summary"):

            with st.spinner("Gemini is summarizing your study material..."):

                try:
                    summary = summarize_text(extracted_text)

                    st.subheader("AI-Generated Summary")
                    st.write(summary)

                except Exception as e:
                    error_message = str(e)

                    if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
                           st.warning(
                                   "Gemini API quota exceeded. "
                                  "Please wait a minute before trying again."
                                    )

                    else:
                            st.error(f"Something went wrong: {e}")