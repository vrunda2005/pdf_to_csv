import pandas as pd
import os

OUTPUT_FILE = "Course_Outlines.xlsx"

if os.path.exists(OUTPUT_FILE):
    df = pd.read_excel(OUTPUT_FILE)
    print("--- Session Count Verification ---")
    if not df.empty:
        # Count columns starting with "Session "
        session_cols = [c for c in df.columns if c.startswith("Session ")]
        print(f"Total Session Columns: {len(session_cols)}")
        print(f"Max Session Number: {max([int(c.split(' ')[1]) for c in session_cols]) if session_cols else 0}")
        
        # Check specific sessions
        row = df.iloc[0]
        print(f"Session 1: {row.get('Session 1', 'N/A')}")
        print(f"Session 15: {row.get('Session 15', 'N/A')}")
        print(f"Session 30: {row.get('Session 30', 'N/A')}")
    else:
        print("DataFrame is empty.")
else:
    print("File not found.")
