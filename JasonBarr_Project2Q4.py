import streamlit as st
from bs4 import BeautifulSoup
import pymupdf as fitz
import docx2txt
import tempfile
import google.generativeai as genai

# Gemini API Key
API_KEY = "YOUR_API_KEY_HERE" 

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(
    "gemini-3.8-flash"
)

st.title("Project 2 - Web-Based LLM App (Gemini Version)")

st.markdown("""
### Question 4

Upload a document and ask a question.

Supported file types:

- TXT
- PDF
- DOCX
- HTML
""")

question = st.text_input("Enter your question")

file = st.file_uploader(
    "Upload a document",
    type=["txt", "pdf", "docx", "html"]
)

if st.button("Submit"):

    if question == "":
        st.write("Please enter a question.")

    else:

        text = ""

        # TXT Files
        if file is not None and file.name.endswith(".txt"):

            text = file.read().decode("utf-8")

        # HTML Files
        elif file is not None and (
            file.name.endswith(".html")
            or file.name.endswith(".htm")
        ):

            html = file.read().decode("utf-8")

            soup = BeautifulSoup(
                html,
                "html.parser"
            )

            text = soup.get_text()

        # PDF Files
        elif file is not None and file.name.endswith(".pdf"):

            pdf = fitz.open(
                stream=file.read(),
                filetype="pdf"
            )

            for page in pdf:
                text += page.get_text()

        # DOCX Files
        elif file is not None and file.name.endswith(".docx"):

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".docx"
            ) as tmp:

                tmp.write(file.read())

                temp_name = tmp.name

            text = docx2txt.process(temp_name)

        # Build Prompt

        if text != "":

            prompt = f"""
Use the document below to answer the question.

Document:
{text}

Question:
{question}
"""

        else:

            prompt = question

        # Gemini Response

        response = model.generate_content(
            prompt
        )

        st.subheader("Answer")

        st.write(
            response.text
        )