import pdfplumber  # Alternative to PyMuPDF
from fpdf import FPDF  # Alternative to ReportLab
import tempfile


# Alternative PDF text extraction using pdfplumber
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
    return text


# Alternative PDF generation using FPDF
def generate_pdf(summary_text):
    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, "Document Summary", ln=True, align="C")
    pdf.ln(10)

    for line in summary_text.split("\n"):
        pdf.multi_cell(0, 10, line)

    pdf.output(temp_pdf.name)
    return temp_pdf.name
