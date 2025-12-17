import pandas as pd
import os

OUTPUT_FILE = "Course_Outlines.xlsx"

if os.path.exists(OUTPUT_FILE):
    df = pd.read_excel(OUTPUT_FILE)
    print("--- Detailed Verification ---")
    if not df.empty:
        row = df.iloc[0]
        print(f"Course Description (len={len(str(row['Course Description']))}): '{str(row['Course Description'])[:100]}...'")
        print(f"Learning Outcomes (len={len(str(row['Learning Outcomes']))}): '{str(row['Learning Outcomes'])[:100]}...'")
        print(f"Project / Assignment Details (len={len(str(row['Project / Assignment Details']))}): '{str(row['Project / Assignment Details'])}'")
    else:
        print("DataFrame is empty.")
else:
    print("File not found.")
