# PDF Data Extraction Project - Daily Progress Log

## Project Overview
Built a Python application to extract data from tourism permit PDFs stored in ZIP files and export to CSV format.

## Problem Solved
Process ZIP files containing PDF documents in nested folder structure:

- **Type A**: Contains only "New Tourism Entry Permit" PDF
- **Type B**: Contains "New Tourism Entry Permit" PDF + "eVisa.pdf"

## Work Completed Today 05/06/2025

### 1. Core Implementation
- Created `FastPDFExtractor` class with optimized PDF processing
- Used PyMuPDF (fitz) for fast PDF text extraction
- Implemented parallel processing with ThreadPoolExecutor

### 2. Data Extraction
Built regex patterns to extract:
- Date (converted YYYY-MM-DD → DD-MM-YYYY)
- Duration (X Days format)
- Entry Type (Single/Multiple Entry)
- Nationality, Name (first 2 words), Passport Number
- Date of Birth (converted YYYY-MM-DD → DD-MM-YYYY)
- File type classification (Type A/B based on eVisa presence)

### 3. Performance Optimizations
- Pre-compiled regex patterns for speed
- Multi-threaded ZIP file processing
- Used Polars for fast CSV export
- Automatic temp file cleanup

### 4. Output Format
CSV with columns: File Name, DATE, TYPE DR, TYPE OP, NATIONALITY, NAME, PASSPORT NO, DOB, Folder Contains Multiple Files

## Technical Stack
- **PyMuPDF**: PDF text extraction
- **Polars**: Fast DataFrame operations
- **Threading**: Parallel ZIP processing
- **Regex**: Pattern matching for data extraction

## Usage
```python
extractor = FastPDFExtractor()
extractor.process_all_zips("zip_folder_path", "output.csv")
```

## Results
Efficiently processes multiple ZIP files in parallel, extracts structured data from nested PDF documents, automatically
classifies folders as Type A or Type B, and exports a clean, well-formatted CSV with proper date formatting.

---
**Status**: Complete and functional  
