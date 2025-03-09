import pdfplumber
import docx
from io import BytesIO

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def extract_text_from_resume(uploaded_file):
    file_extension = uploaded_file.name.split(".")[-1].lower()

    if file_extension == "pdf":
        return extract_text_from_pdf(BytesIO(uploaded_file.read()))
    elif file_extension == "docx":
        return extract_text_from_docx(BytesIO(uploaded_file.read()))
    else:
        return None
