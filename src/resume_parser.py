import pdfplumber
import docx

# Function to read PDF resumes
def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"
    return text.strip()

# Function to read DOCX resumes
def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    return "\n".join([p.text for p in doc.paragraphs if p.text]).strip()

