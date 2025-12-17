import pdfplumber

pdf_path = "/home/vrunda/Projects/Education_Network/outline_pdf_csv/View_Print Course Outline.pdf"
full_text = ""
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        full_text += page.extract_text() + "\n"

with open("full_text_dump.txt", "w") as f:
    f.write(full_text)

print("Dumped full text.")
