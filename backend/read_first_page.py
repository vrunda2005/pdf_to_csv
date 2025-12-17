import pdfplumber

pdf_path = "/home/vrunda/Projects/Education_Network/outline_pdf_csv/View_Print Course Outline.pdf"

with pdfplumber.open(pdf_path) as pdf:
    print(pdf.pages[0].extract_text())
