import streamlit as st
from PyPDF2 import PdfReader

def load_pdf(file):
    try:
        reader = PdfReader(file)
        text = " ".join(page.extract_text() for page in reader.pages if page.extract_text())
        if not text.strip():
            raise ValueError("No text extracted from the PDF!")
        return text
    except Exception as e:
        st.error(f"Oops! PDF loading failed: {e}")
        return None