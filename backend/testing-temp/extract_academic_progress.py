import re
import json
import pdfplumber
from datetime import datetime

def extract_section(text, section_name, end_marker=None):
    if end_marker:
        pattern = fr'{section_name}(.*?)(?:{end_marker})'
    else:
        pattern = fr'{section_name}(.*?)(?=\n\n|$)'
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else ""

def extract_key_value(text, key, value_pattern=r'(.*?)(?:\n|$)'):
    pattern = rf'{key}\s*:\s*{value_pattern}'
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else ""

def extract_credits(text):
    pattern = r'Credits:\s*(\d+\.\d+)\s*required,\s*(\d+\.\d+)\s*earned,\s*(\d+\.\d+)\s*in progress,\s*(\d+\.\d+)\s*needed'
    match = re.search(pattern, text)
    if match:
        return {
            "required": float(match.group(1)),
            "earned": float(match.group(2)),
            "inProgress": float(match.group(3)),
            "needed": float(match.group(4))
        }
    return {}

def extract_gpa(text):
    pattern = r'GPA:\s*(\d+\.\d+)\s*required,\s*(\d+\.\d+)\s*completed'
    match = re.search(pattern, text)
    return float(match.group(2)) if match else 0

def extract_courses(text):
    courses = re.findall(r'(\w+)\s+(\d+)\s+(.*?)\s+(\w+)\s+(\d+\.\d+)\s+(\w+)', text)
    return [
        {
            "code": f"{course[0]} {course[1]}",
            "name": course[2],
            "credits": float(course[4]),
            "grade": course[3],
            "type": course[5]
        } for course in courses
    ]

def extract_academic_progress(text):
    data = {
        "studentInfo": {
            "name": extract_key_value(text, "Name"),
            "id": extract_key_value(text, "ID"),
            "expectedGradTerm": extract_key_value(text, "Exp Grad Term"),
            "catalogYear": extract_key_value(text, "Catalog Year"),
            "plans": [plan.strip() for plan in extract_key_value(text, "Plan\(s\)").split(',')]
        },
        "academicSummary": {
            "totalCredits": extract_credits(extract_section(text, "GENERAL INFORMATION")),
            "cumulativeGPA": extract_gpa(extract_section(text, "Cumulative GPA")),
            "institutionalGPA": extract_gpa(extract_section(text, "Institutional GPA"))
        },
        "graduationRequirements": {
            "overallStatus": extract_key_value(extract_section(text, "GRADUATION REQUIREMENTS"), "Overall Requirement"),
            "degreeCredit": extract_credits(extract_section(text, "Degree credit")),
            "upperDivisionCredits": extract_credits(extract_section(text, "Upper Division"))
        },
        "generalEducation": {
            "overallStatus": extract_key_value(extract_section(text, "GENERAL EDUCATION REQUIREMENTS"), "Overall Requirement"),
            "categories": []
        },
        "major": {
            "name": extract_key_value(text, "MAJOR IN"),
            "overallStatus": extract_key_value(extract_section(text, "MAJOR IN"), "Overall Requirement"),
            "gpa": extract_gpa(extract_section(text, "Major GPA")),
            "requirements": []
        },
        "minor": {
            "name": extract_key_value(text, "MINOR IN"),
            "overallStatus": extract_key_value(extract_section(text, "MINOR IN"), "Overall Requirement"),
            "gpa": extract_gpa(extract_section(text, "Minor GPA")),
            "requirements": []
        },
        "courseHistory": extract_courses(extract_section(text, "IN PROGRESS COURSES"))
    }

    # Extract GE categories
    ge_section = extract_section(text, "GENERAL EDUCATION REQUIREMENTS")
    ge_categories = re.findall(r'(\w+) Inquiry \((.*?)\)(.*?)Credits:\s*(\d+\.\d+)\s*required,\s*(\d+\.\d+)\s*earned', ge_section, re.DOTALL)
    data["generalEducation"]["categories"] = [
        {
            "name": f"{cat[0]} Inquiry ({cat[1]})",
            "status": cat[2].strip(),
            "requiredCredits": float(cat[3]),
            "completedCredits": float(cat[4])
        } for cat in ge_categories
    ]

    # Extract major and minor requirements
    for program in ["major", "minor"]:
        program_section = extract_section(text, f"{program.upper()} IN")
        requirements = re.findall(r'(\w+.*?)\n(.*?)\n', program_section, re.DOTALL)
        data[program]["requirements"] = [
            {
                "name": req[0],
                "status": req[1].strip(),
                "courses": extract_courses(extract_section(program_section, req[0]))
            } for req in requirements
        ]

    return data

if __name__ == "__main__":
    import sys
    import os
    
    if len(sys.argv) != 2:
        print("Usage: python extract_academic_progress.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # Extract text from PDF
    text = ""
    with pdfplumber.open(input_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Ensure the output directory exists
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save raw extracted text to a .txt file
    txt_filename = f"extracted_text_{timestamp}.txt"
    txt_path = os.path.join(output_dir, txt_filename)
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(text)
    
    print(f"Extracted text saved to {txt_path}")
    
    # Process the extracted text
    data = extract_academic_progress(text)
    
    # Save processed data to a JSON file
    json_filename = f"academic_progress_{timestamp}.json"
    json_path = os.path.join(output_dir, json_filename)
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    
    print(f"Processed data saved to {json_path}")
    
    # Optionally, still print the processed data to console
    print(json.dumps(data, indent=2))