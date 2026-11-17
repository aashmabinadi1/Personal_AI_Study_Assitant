
import streamlit as st
import json
import os
import uuid

from utils.Pdf_read import extract_text_from_pdf
from utils.ai_summarizer import summarize_text


# --------------------------------------------------
# Storage configuration
# --------------------------------------------------

os.makedirs("data", exist_ok=True)

MATERIALS_FILE = os.path.join("data", "study_materials.json")
BACKUP_FILE = os.path.join("data", "study_materials_backup.json")


# --------------------------------------------------
# Save and load materials
# --------------------------------------------------

def save_library(materials):
    with open(MATERIALS_FILE, "w", encoding="utf-8") as file:
        json.dump(materials, file, ensure_ascii=False, indent=4)


def load_library():
    if os.path.exists(MATERIALS_FILE):
        try:
            with open(MATERIALS_FILE, "r", encoding="utf-8") as file:
                materials = json.load(file)

            if isinstance(materials, list):
                return materials

        except (json.JSONDecodeError, OSError):
            return []

    # Migrate previously saved material
    if os.path.exists(BACKUP_FILE):
        try:
            with open(BACKUP_FILE, "r", encoding="utf-8") as file:
                old_data = json.load(file)

            if old_data.get("study_text"):
                materials = [{
                    "id": str(uuid.uuid4()),
                    "title": "Previously Saved Study Material",
                    "study_text": old_data.get("study_text", ""),
                    "summary": old_data.get("study_summary", "")
                }]

                save_library(materials)
                return materials

        except (json.JSONDecodeError, OSError):
            return []

    return []


# --------------------------------------------------
# Initialize session state
# --------------------------------------------------

if "study_library" not in st.session_state:
    st.session_state["study_library"] = load_library()

if "study_text" not in st.session_state:
    st.session_state["study_text"] = ""

if "study_summary" not in st.session_state:
    st.session_state["study_summary"] = ""


# --------------------------------------------------
# Page heading
# --------------------------------------------------

st.title("Personal AI Study Assistant")
st.header("Study Materials Manager")

st.write(
    "Upload, organize, and summarize your study materials."
)

st.divider()


# --------------------------------------------------
# Upload new PDF
# --------------------------------------------------

st.subheader("Add New Study Material")

uploaded_file = st.file_uploader(
    "Upload your study PDF",
    type=["pdf"],
    key="study_pdf"
)

if uploaded_file is not None:

    if st.button("Add PDF to Library", type="primary"):

        try:
            with st.spinner("Extracting PDF text..."):

                extracted_text = extract_text_from_pdf(uploaded_file)

            if extracted_text and extracted_text.strip():

                new_material = {
                    "id": str(uuid.uuid4()),
                    "title": os.path.splitext(uploaded_file.name)[0],
                    "study_text": extracted_text,
                    "summary": ""
                }

                st.session_state["study_library"].append(new_material)

                save_library(st.session_state["study_library"])

                st.session_state["selected_material_id"] = new_material["id"]
                st.session_state["study_text"] = extracted_text
                st.session_state["study_summary"] = ""

                st.success("PDF added to your Study Materials Library!")

                st.rerun()

            else:
                st.warning(
                    "No readable text was found. "
                    "Please upload a text-based PDF."
                )

        except Exception as e:
            st.error(f"PDF extraction failed: {e}")


st.divider()


# --------------------------------------------------
# Saved materials library
# --------------------------------------------------

st.subheader("Your Saved Study Materials")

materials = st.session_state["study_library"]

if materials:

    material_ids = [material["id"] for material in materials]

    if (
        st.session_state.get("selected_material_id")
        not in material_ids
    ):
        st.session_state["selected_material_id"] = material_ids[0]

    selected_id = st.selectbox(
        "Select a study material",
        options=material_ids,
        format_func=lambda material_id: next(
            material["title"]
            for material in materials
            if material["id"] == material_id
        ),
        key="material_selector"
    )

    selected_material = next(
        material for material in materials
        if material["id"] == selected_id
    )

    st.session_state["selected_material_id"] = selected_id
    st.session_state["study_text"] = selected_material["study_text"]
    st.session_state["selected_material_id"] = selected_id
    st.session_state["study_summary"] = selected_material["summary"]

    st.success("Study material loaded successfully!")

    # View extracted text
    with st.expander("View Extracted Text"):

        st.text_area(
            "PDF Content",
            selected_material["study_text"],
            height=300,
            key=f"text_{selected_id}"
        )

    st.divider()

    # Generate summary
    if st.button("Generate AI Summary", type="primary"):

        try:
            with st.spinner("Generating your summary..."):

                summary = summarize_text(
                    selected_material["study_text"]
                )

            selected_material["summary"] = summary

            st.session_state["study_summary"] = summary

            save_library(materials)

            st.success("Summary generated and saved successfully!")

        except Exception as e:
            st.error(f"Summary generation failed: {e}")

    # Display saved summary
    if selected_material["summary"]:

        st.subheader("Study Summary")
        st.write(selected_material["summary"])

    st.divider()

        # Delete material
    st.subheader("Manage Study Materials")

    confirm_delete = st.checkbox(
        "I confirm that I want to delete this study material.",
        key=f"confirm_delete_{selected_id}"
    )

    if st.button(
        "Delete Selected Material",
        type="secondary",
        disabled=not confirm_delete
    ):

        materials = [
            material for material in materials
            if material["id"] != selected_id
        ]

        st.session_state["study_library"] = materials
        save_library(materials)

        st.session_state["study_text"] = ""
        st.session_state["study_summary"] = ""
        st.session_state["selected_material_id"] = None

        st.session_state.pop("material_selector", None)

        st.success("Study material deleted successfully!")

        st.rerun()

else:

    st.info(
        "Your library is empty. Upload a PDF above "
        "to get started."
    )
