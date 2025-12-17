import pdfplumber
import re

pdf_path = "/home/vrunda/Projects/Education_Network/outline_pdf_csv/View_Print Course Outline.pdf"

print(f"--- Debugging {pdf_path} ---")

with pdfplumber.open(pdf_path) as pdf:
    full_text = ""
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        print(f"\n--- Page {i+1} Raw Text ---\n")
        print(text)
        full_text += text + "\n"

print("\n--- Regex Testing ---")

# Test Course Name
match = re.search(r'Course\s+(.*?)\s+Semester', full_text, re.IGNORECASE | re.DOTALL)
if match:
    print(f"Course Match: '{match.group(1)}'")
else:
    print("Course Match: FAILED")

# Test Description
match = re.search(r'Course Description\s*[:\-]?\s*(.*?)\s*(Course Objectives|Learning Outcomes)', full_text, re.IGNORECASE | re.DOTALL)
if match:
    print(f"Description Match: '{match.group(1)[:50]}...'")
else:
    print("Description Match: FAILED")
