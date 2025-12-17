import os
import shutil
import extractor
import uuid

# Setup paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Source PDF
SOURCE_PDF = "/home/vrunda/Projects/Education_Network/outline_pdf_csv/View_Print Course Outline.pdf"

# Simulate upload
file_id = str(uuid.uuid4())
file_path = os.path.join(UPLOAD_DIR, f"{file_id}.pdf")
shutil.copy(SOURCE_PDF, file_path)

print(f"Testing extraction on {file_path}...")

try:
    data = extractor.extract_data_from_pdf(file_path)
    if data:
        print("Extraction SUCCESS")
        print("Keys:", data.keys())
    else:
        print("Extraction FAILED (returned None)")
except Exception as e:
    print(f"Extraction CRASHED: {e}")

# Cleanup
if os.path.exists(file_path):
    os.remove(file_path)
