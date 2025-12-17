import pdfplumber
import pandas as pd
import re
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Output file
OUTPUT_FILE = "Course_Outlines.xlsx"

# Fields to extract
METADATA_FIELDS = [
    "Course", "Semester", "Faculty Name(s)", "Contact", "School", "Credits",
    "Pedagogy", "Teaching Pedagogy Enable/NP", "Schedule", "Prerequisite",
    "Antirequisite", "Corequisite", "GER Category", "Course Description",
    "Course Objectives", "Learning Outcomes", "Assessment/Evaluation",
    "Attendance Policy", "Project / Assignment Details", "Course Material",
    "Additional Information"
]

def clean_text(text):
    """Cleans extracted text."""
    if pd.isna(text) or not text:
        return ""
    text = str(text).strip()
    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text)
    return text

def extract_session_table(pdf_path):
    """Extracts the session plan table using pdfplumber."""
    session_data = []
    headers_map = {}
    table_started = False
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            
            for table in tables:
                if not table: continue
                
                # Check if this table has the header
                # We assume the first row is the header if it contains keywords
                header_row = [str(cell).lower().replace('\n', ' ') for cell in table[0] if cell]
                header_str = " ".join(header_row)
                
                is_new_header = "topic" in header_str and ("reading" in header_str or "activity" in header_str)
                
                start_row_idx = 0
                
                if is_new_header:
                    table_started = True
                    headers_map = {} # Reset map for new table definition
                    # Map columns
                    for idx, col_name in enumerate(table[0]):
                        if not col_name: continue
                        c_name = col_name.lower().replace('\n', ' ')
                        if "topic" in c_name and "title" in c_name: headers_map[idx] = "TOPIC TITLE"
                        elif "subtopic" in c_name: headers_map[idx] = "TOPIC & SUBTOPIC DETAILS"
                        elif "reading" in c_name: headers_map[idx] = "READINGS, CASES, ETC."
                        elif "activit" in c_name: headers_map[idx] = "ACTIVITIES"
                        elif "date" in c_name: headers_map[idx] = "IMPORTANT DATES"
                    
                    start_row_idx = 1 # Skip header
                
                # If we haven't found a header yet, and this doesn't look like one, skip
                if not table_started:
                    continue
                    
                # Process rows
                for row in table[start_row_idx:]:
                    # Check if it's a valid session row (starts with a number)
                    if not row or not row[0]: continue
                    
                    session_num_str = str(row[0]).strip()
                    # Remove trailing .0 if present
                    if session_num_str.endswith('.0'): session_num_str = session_num_str[:-2]
                    
                    if not re.match(r'^\d+$', session_num_str):
                        continue
                        
                    session_num = int(session_num_str)
                    row_details = []
                    
                    for idx, cell in enumerate(row):
                        if idx == 0: continue # Skip number
                        if idx in headers_map and cell:
                            clean_val = clean_text(cell)
                            if clean_val and clean_val.lower() != 'nan' and clean_val.lower() != 'n/a':
                                row_details.append(f"{headers_map[idx]}: {clean_val}")
                    
                    if row_details:
                        session_data.append({
                            "Session": session_num,
                            "Details": "\n".join(row_details)
                        })
    return session_data

def extract_data_from_pdf(pdf_path):
    """
    Extracts all data from a PDF (metadata + sessions) using robust full-text regex.
    """
    data = {field: "" for field in METADATA_FIELDS}
    
    try:
        # 1. Get Full Text
        full_text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                full_text += page.extract_text() + "\n"
        
        # 2. Extract Header Fields (Line-based)
        # We split by lines for the top section to handle the "Course ... Semester" layout accurately
        lines = full_text.split('\n')
        
        # Helper to find line index
        def find_line_startswith(prefix):
            for i, line in enumerate(lines):
                if line.strip().lower().startswith(prefix.lower()):
                    return i, line
            return -1, None

        # --- Course & Semester ---
        c_idx, c_line = find_line_startswith("Course")
        if c_idx != -1:
            # Regex to split Course and Semester on the same line
            match = re.search(r'Course\s+(.*?)\s+Semester\s+(.*)', c_line, re.IGNORECASE)
            if match:
                data['Course'] = match.group(1).strip()
                data['Semester'] = match.group(2).strip()
                
                # Check next line for Course continuation
                # If next line is NOT "Faculty", "School", etc., append it to Course
                if c_idx + 1 < len(lines):
                    next_line = lines[c_idx + 1].strip()
                    # List of keywords that would start a NEW field
                    keywords = ["Faculty", "School", "Contact", "Credits", "GER", "Pedagogy", "Schedule"]
                    if next_line and not any(next_line.startswith(k) for k in keywords):
                        data['Course'] += " " + next_line
            else:
                # Fallback if Semester is not on same line
                data['Course'] = c_line.replace("Course", "").strip()

        # --- Faculty & Contact ---
        f_idx, f_line = find_line_startswith("Faculty Name(s)")
        if f_idx != -1:
            match = re.search(r'Faculty Name\(s\)\s+(.*?)\s+Contact\s+(.*)', f_line, re.IGNORECASE)
            if match:
                data['Faculty Name(s)'] = match.group(1).strip()
                data['Contact'] = match.group(2).strip()
            else:
                data['Faculty Name(s)'] = f_line.replace("Faculty Name(s)", "").strip()

        # --- School & Credits ---
        s_idx, s_line = find_line_startswith("School")
        if s_idx != -1:
            match = re.search(r'School\s+(.*?)\s+Credits\s+(.*)', s_line, re.IGNORECASE)
            if match:
                data['School'] = match.group(1).strip()
                data['Credits'] = match.group(2).strip()
            else:
                data['School'] = s_line.replace("School", "").strip()

        # 3. Extract Block Fields (Regex DOTALL)
        # We use the full_text for this to handle multi-line blocks easily
        
        def extract_block(start_marker, end_markers):
            # Escape start marker
            escaped_start = re.escape(start_marker)
            
            # End markers should be at the start of a line (preceded by \n)
            # This prevents matching words inside the text (e.g. "course" in description)
            end_pattern = r"(?=\n\s*(?:" + "|".join(map(re.escape, end_markers)) + r"))"
            
            pattern = escaped_start + r"\s*[:\-]?\s*(.*?)\s*" + end_pattern
            match = re.search(pattern, full_text, re.DOTALL | re.IGNORECASE)
            if match:
                return clean_text(match.group(1))
            return ""

        # Define the order of fields to help with "end markers"
        # We'll use a list of all potential next headers as end markers
        all_headers = [
            "Course", "Semester", "Faculty Name(s)", "Contact", "School", "Credits",
            "GER Category", "Teaching Pedagogy Enable", "P/NP Course", "Schedule",
            "Prerequisite", "Antirequisite", "Corequisite", "Course Description",
            "Course Objectives", "Learning Outcomes", "Assessment/Evaluation",
            "Attendance Policy", "Project / Assignment Details", "Course Material",
            "Additional Information", "Session Plan", 
            # Add other headers found in text dump to be safe terminators
            "Pedagogy", "Expectation From Students", "Project / Assignment", "Details"
        ]
        
        # Map fields to their start markers
        field_markers = {
            "GER Category": "GER Category",
            "Teaching Pedagogy Enable/NP": "Teaching Pedagogy Enable", # Also check P/NP
            "Schedule": "Schedule",
            "Prerequisite": "Prerequisite",
            "Antirequisite": "Antirequisite",
            "Corequisite": "Corequisite",
            "Course Description": "Course Description",
            "Course Objectives": "Course Objectives",
            "Learning Outcomes": "Learning Outcomes",
            "Assessment/Evaluation": "Assessment/Evaluation", # Also check Assessment
            "Attendance Policy": "Attendance Policy",
            "Project / Assignment Details": "Project / Assignment Details", # Also Project Details
            "Course Material": "Course Material",
            "Additional Information": "Additional Information"
        }

        for field, marker in field_markers.items():
            val = None
            
            # Special handling for variants
            if field == "Teaching Pedagogy Enable/NP":
                val = extract_block("Teaching Pedagogy Enable", all_headers)
                if not val: val = extract_block("P/NP Course", all_headers)
                
            elif field == "Assessment/Evaluation":
                val = extract_block("Assessment/Evaluation", all_headers)
                if not val: val = extract_block("Assessment", all_headers)
                if not val: val = extract_block("Evaluation", all_headers)
                
            elif field == "Project / Assignment Details":
                # Try full header first
                val = extract_block("Project / Assignment Details", all_headers)
                # Try split header (just "Project / Assignment")
                if not val: val = extract_block("Project / Assignment", all_headers)
                if not val: val = extract_block("Project Details", all_headers)
                if not val: val = extract_block("Assignment Details", all_headers)
                
            else:
                val = extract_block(marker, all_headers)
            
            if val:
                data[field] = val

        # --- Specific Formatting for Course Material ---
        # The user wants this organized.
        cm_text = data['Course Material']
        if cm_text:
            formatted_cm = ""
            
            # Helper to extract section
            def get_section(key, stop_keys):
                pattern = re.escape(key) + r"\s*[:\-]?\s*(.*?)\s*(?=" + "|".join(map(re.escape, stop_keys)) + r"|$)"
                m = re.search(pattern, cm_text, re.IGNORECASE | re.DOTALL)
                return m.group(1).strip() if m else None

            # 1. Text Books
            tb = get_section("Text Book(s)", ["Reference Book", "Other Course Material"])
            if not tb: tb = get_section("Text Book", ["Reference Book", "Other Course Material"])
            
            if tb:
                formatted_cm += f"Text Book(s):\n{tb}\n\n"
            
            # 2. Reference Books
            rb = get_section("Reference Book(s)", ["Text Book", "Other Course Material"])
            if not rb: rb = get_section("Reference Book", ["Text Book", "Other Course Material"])
            
            if rb:
                formatted_cm += f"Reference Book(s):\n{rb}\n\n"
                
            # 3. Other Course Material
            other = get_section("Other Course Material", ["Text Book", "Reference Book"])
            
            if other:
                formatted_cm += f"Other Course Material:\n{other}\n\n"
                
            # If regex split failed but we have text, just use the cleaned text
            if not formatted_cm:
                formatted_cm = cm_text
                
            data['Course Material'] = formatted_cm.strip()

        # 4. Extract Sessions
        sessions = extract_session_table(pdf_path)
        
        # Flatten session data
        max_session = 0
        for s in sessions:
            s_num = s['Session']
            s_details = s['Details']
            data[f'Session {s_num}'] = s_details
            max_session = max(max_session, s_num)
        
        data['Max_Session'] = max_session
        
        return data

    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        import traceback
        traceback.print_exc()
        return None

def append_to_excel(new_data_list, output_file):
    """
    Appends a list of data dictionaries to an Excel file.
    Dynamically adds session columns as needed.
    """
    if not new_data_list:
        return

    # Create DataFrame from new data
    df = pd.DataFrame(new_data_list)
    
    # 1. Determine max session in NEW data
    new_max_session = 0
    if 'Max_Session' in df.columns:
        new_max_session = df['Max_Session'].max()
        df = df.drop(columns=['Max_Session'])
    
    # Also check actual columns in new data just in case
    new_session_cols = [c for c in df.columns if c.startswith("Session ")]
    if new_session_cols:
        nums = [int(c.split(' ')[1]) for c in new_session_cols if c.split(' ')[1].isdigit()]
        if nums:
            new_max_session = max(new_max_session, max(nums))

    # 2. Determine max session in EXISTING data (if file exists)
    existing_max_session = 0
    existing_df = pd.DataFrame()
    
    if os.path.exists(output_file):
        try:
            existing_df = pd.read_excel(output_file)
            existing_session_cols = [c for c in existing_df.columns if c.startswith("Session ")]
            if existing_session_cols:
                nums = [int(c.split(' ')[1]) for c in existing_session_cols if c.split(' ')[1].isdigit()]
                if nums:
                    existing_max_session = max(nums)
        except Exception as e:
            print(f"Warning: Could not read existing Excel: {e}")

    # 3. Determine global max session
    global_max_session = max(new_max_session, existing_max_session)

    # 4. Construct final column list
    final_cols = METADATA_FIELDS.copy()
    for i in range(1, int(global_max_session) + 1):
        final_cols.append(f'Session {i}')
    
    # 5. Reindex and Concatenate
    # Ensure new df has all columns
    for col in final_cols:
        if col not in df.columns:
            df[col] = ""
    df = df.reindex(columns=final_cols)
    
    if not existing_df.empty:
        # Ensure existing df has all columns
        for col in final_cols:
            if col not in existing_df.columns:
                existing_df[col] = ""
        existing_df = existing_df.reindex(columns=final_cols)
        
        # Append
        final_df = pd.concat([existing_df, df], ignore_index=True)
    else:
        final_df = df

    # Save
    try:
        final_df.to_excel(output_file, index=False)
    except Exception as e:
        print(f"Error saving Excel: {e}")

def main():
    # Find PDF files
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pdf_files = []
    
    for f in os.listdir('.'):
        if f.lower().endswith('.pdf'):
            pdf_files.append(os.path.abspath(f))
            
    for f in os.listdir(root_dir):
        if f.lower().endswith('.pdf'):
            pdf_files.append(os.path.join(root_dir, f))
            
    pdf_files = list(set(pdf_files))
    
    if not pdf_files:
        print("No PDF files found.")
        return

    all_data = []
    for pdf_path in pdf_files:
        print(f"Processing {os.path.basename(pdf_path)}...")
        data = extract_data_from_pdf(pdf_path)
        if data:
            all_data.append(data)

    if all_data:
        append_to_excel(all_data, OUTPUT_FILE)
        print(f"Saved extracted data to {OUTPUT_FILE}")
    else:
        print("No data extracted.")

if __name__ == "__main__":
    main()
