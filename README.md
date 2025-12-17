# Course Outline Extractor

A modern web application that extracts structured data from course outline PDFs and converts it into Excel format. Built with React, Tailwind CSS, and Python (FastAPI).

## 🚀 Features

- **PDF Upload**: Drag and drop interface for uploading multiple course outline PDFs.
- **Automated Extraction**: Intelligent parsing of course details, schedules, and reading lists.
- **Excel Export**: Download extracted data as a formatted Excel file.
- **History**: View previously extracted data directly in the dashboard.
- **Responsive Design**: Beautiful, mobile-friendly UI built with Tailwind CSS.

## 🛠️ Tech Stack

### Frontend
- **React**: UI library for building the interface.
- **Vite**: Next-generation frontend tooling.
- **Tailwind CSS**: Utility-first CSS framework for styling.
- **Framer Motion**: Library for production-ready animations.
- **Lucide React**: Beautiful & consistent icons.
- **Axios**: Promise based HTTP client for the browser.

### Backend
- **Python**: Core programming language.
- **FastAPI**: Modern, fast (high-performance) web framework for building APIs.
- **Pandas**: Data manipulation and analysis.
- **PyPDF2 / pdfplumber**: PDF text extraction.

## 📦 Installation & Setup

### Prerequisites
- Node.js (v18+)
- Python (v3.8+)

### 1. Backend Setup

Navigate to the backend directory:
```bash
cd backend
```

Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Start the API server:
```bash
uvicorn main:app --reload
```
The backend will run at `http://localhost:8000`.

### 2. Frontend Setup

Open a new terminal and navigate to the frontend directory:
```bash
cd frontend
```

Install dependencies:
```bash
npm install
```

Start the development server:
```bash
npm run dev
```
The frontend will run at `http://localhost:5173`.

## 📝 Usage

1. Open the frontend application.
2. Drag and drop your Course Outline PDFs into the upload area.
3. Click "Start Extraction".
4. Once complete, you can view the data in the table or click "Download Excel" to get the file.

## 📄 License

This project is licensed under the MIT License.
# pdf_to_csv
