import pandas as pd
import os

OUTPUT_FILE = "Course_Outlines.xlsx"

if os.path.exists(OUTPUT_FILE):
    df = pd.read_excel(OUTPUT_FILE)
    print("--- Extracted Data Verification ---")
    if not df.empty:
        row = df.iloc[0]
        print(f"Course: '{row['Course']}'")
        print(f"Semester: '{row['Semester']}'")
        print(f"Course Description: '{str(row['Course Description'])[:100]}...'")
        print(f"Course Objectives: '{str(row['Course Objectives'])[:100]}...'")
        print(f"Course Material: '{str(row['Course Material'])[:100]}...'")
    else:
        print("DataFrame is empty.")
else:
    print("File not found.")
