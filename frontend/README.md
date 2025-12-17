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

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the API server:
   ```bash
   uvicorn main:app --reload
   ```

## 📝 Usage

1. Open the frontend application (usually at `http://localhost:5173`).
2. Drag and drop your Course Outline PDFs into the upload area.
3. Click "Start Extraction".
4. Once complete, you can view the data in the table or click "Download Excel" to get the file.

## 🤝 Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/amazing-feature`).
3. Commit your changes (`git commit -m 'Add some amazing feature'`).
4. Push to the branch (`git push origin feature/amazing-feature`).
5. Open a Pull Request.

## 📄 License

This project is licensed under the MIT License.
