from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import shutil
import os
import uuid
import json
from typing import List
import pandas as pd
import extractor

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
DATA_DIR = os.path.join(BASE_DIR, "data")
MASTER_DATA_FILE = os.path.join(DATA_DIR, "master_data.json")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

def load_master_data():
    if os.path.exists(MASTER_DATA_FILE):
        try:
            with open(MASTER_DATA_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save_master_data(data):
    with open(MASTER_DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.get("/api/data")
async def get_all_data():
    data = load_master_data()
    return {"data": data}

@app.post("/api/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    extracted_data_list = []
    
    for file in files:
        if not file.filename.endswith('.pdf'):
            continue
            
        # Save file temporarily
        file_id = str(uuid.uuid4())
        file_ext = os.path.splitext(file.filename)[1]
        file_path = os.path.join(UPLOAD_DIR, f"{file_id}{file_ext}")
        
        # Ensure directory exists (in case it was deleted while server was running)
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Extract data
        try:
            data = extractor.extract_data_from_pdf(file_path)
            if data:
                # Add filename for reference
                data['Source File'] = file.filename
                # Add timestamp or upload ID if needed, but keeping it simple
                extracted_data_list.append(data)
        except Exception as e:
            print(f"Error processing {file.filename}: {e}")
        finally:
            # Clean up uploaded file
            if os.path.exists(file_path):
                os.remove(file_path)

    if not extracted_data_list:
        raise HTTPException(status_code=400, detail="No valid data extracted from uploaded files.")

    # Update Master Data
    os.makedirs(DATA_DIR, exist_ok=True)
    current_master_data = load_master_data()
    current_master_data.extend(extracted_data_list)
    save_master_data(current_master_data)

    # Append to the main Excel file
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_filename = "Course_Outlines.xlsx"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    
    extractor.append_to_excel(extracted_data_list, output_path)
    
    # Convert to JSON for frontend display
    df = pd.DataFrame(extracted_data_list)
    df = df.fillna("")
    json_data = df.to_dict(orient="records")
    
    return {
        "message": "Extraction complete",
        "data": json_data,
        "download_url": f"/api/download/{output_filename}"
    }

@app.get("/api/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path, 
        filename="Course_Outlines.xlsx", 
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

if __name__ == "__main__":
    import uvicorn
    from dotenv import load_dotenv
    
    load_dotenv()
    
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    uvicorn.run(app, host=host, port=port)
