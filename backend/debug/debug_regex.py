import re

# Load the dumped text
with open("full_text_dump.txt", "r") as f:
    full_text = f.read()

def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

def extract_block_debug(start_marker, end_markers):
    # OLD BROKEN REGEX (Simulated)
    # pattern = re.escape(start_marker) + r"\s*[:\-]?\s*(.*?)\s*(?=" + "|".join(map(re.escape, end_markers)) + r")"
    
    # NEW PROPOSED REGEX: Enforce newline before end marker
    # We also need to handle the start marker being flexible
    
    # Escape start marker but allow flexible whitespace
    escaped_start = re.escape(start_marker).replace(r"\ ", r"\s+")
    
    # End markers should be at the start of a line
    # (?=\n\s*(?:Marker1|Marker2|...))
    end_pattern = r"(?=\n\s*(?:" + "|".join(map(re.escape, end_markers)) + r"))"
    
    pattern = escaped_start + r"\s*[:\-]?\s*(.*?)\s*" + end_pattern
    
    print(f"--- Extracting '{start_marker}' ---")
    # print(f"Pattern: {pattern}")
    
    match = re.search(pattern, full_text, re.DOTALL | re.IGNORECASE)
    if match:
        val = clean_text(match.group(1))
        print(f"MATCH: {val[:100]}...")
        return val
    else:
        print("NO MATCH")
        return None

all_headers = [
    "Course", "Semester", "Faculty Name(s)", "Contact", "School", "Credits",
    "GER Category", "Teaching Pedagogy Enable", "P/NP Course", "Schedule",
    "Prerequisite", "Antirequisite", "Corequisite", "Course Description",
    "Course Objectives", "Learning Outcomes", "Assessment/Evaluation",
    "Attendance Policy", "Project / Assignment Details", "Course Material",
    "Additional Information", "Session Plan", "Pedagogy", "Expectation From Students",
    "Project / Assignment" # Added for testing
]

# Test 1: Course Description (Was truncated at 'course')
extract_block_debug("Course Description", all_headers)

# Test 2: Learning Outcomes (Was truncated at 'this')
extract_block_debug("Learning Outcomes", all_headers)

# Test 3: Project / Assignment Details (Was empty)
# The text in dump is: "Project / Assignment Quizzes (2): 30%\nDetails Mid semester examination: 30%"
# The header "Project / Assignment Details" doesn't exist contiguously.
extract_block_debug("Project / Assignment Details", all_headers)
extract_block_debug("Project / Assignment", all_headers)
