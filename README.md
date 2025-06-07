
# 🧾ZipHandle | A PDF Data Extraction Project

## 📌 Project Overview
A desktop application to extract structured data from **Tourism Permit PDFs** stored in ZIP files and export the data into a CSV file.
ZIP file contents follow a nested folder structure:
- **Type A**: Contains only the `New Tourism Entry Permit.pdf`
- **Type B**: Contains both `New Tourism Entry Permit.pdf` and `eVisa.pdf`
The application automatically identifies folder types, extracts specific data fields from the PDFs using regex, and generates a clean, formatted CSV report.

## ✅ Work Completed on 05/06/2025 – Day 1

    1️⃣ Core Implementation
    - Created `FastPDFExtractor` class to handle PDF parsing and data collection.
    - Used **PyMuPDF (`fitz`)** for fast text extraction from PDF files.
    - Implemented parallel processing with **ThreadPoolExecutor** to handle multiple ZIP files efficiently.
    
    2️⃣ Data Extraction
    Regex patterns were built to extract the following fields:
    - `Created Date` → formatted as `DD-MM-YYYY`
    - `Duration` → e.g., `30 Days`
    - `Entry Type` → `Single Entry` / `Multiple Entry`
    - `Current Nationality`
    - `Name` → First two words only
    - `Passport Number`
    - `Date of Birth` → formatted as `DD-MM-YYYY`
    - Folder classification → `Type A` or `Type B` (based on presence of `eVisa.pdf`)
    
    3️⃣ Performance Optimizations
    - Precompiled regex for efficiency.
    - Multithreaded ZIP file processing.
    - Utilized **Polars** for high-speed DataFrame operations and CSV export.
    - Implemented auto-cleanup for temporary directories.
    
    4️⃣ Output Format
    Final CSV includes:
    ```
    File Name, DATE, TYPE DR, TYPE OP, NATIONALITY, NAME, PASSPORT NO, DOB, Folder Contains Multiple Files
    ```
    
    🛠️ Tech Stack
    - `PyMuPDF` – PDF text extraction
    - `Polars` – Fast DataFrame manipulation
    - `concurrent.futures` – Parallel ZIP file processing
    - `Regex` – Data extraction
    
    🧪 Usage
    ```python
    extractor = FastPDFExtractor()
    extractor.process_all_zips("zip_folder_path", "output.csv")
    ```

---

## 🚀 Work Completed on 06/06/2025 – Day 2

    🖥️ GUI Development
    - Added a simple GUI using **Tkinter**.
    - Users can:
      - Browse and select ZIP folder
      - Choose where to save the output CSV
      - Start extraction process via button
    - Progress and completion messages are shown in the interface.
    
    ⚙️ GUI Features
    - File/folder pickers for input and output
    - Button to initiate extraction
    - Real-time status display
    - Error handling and completion alert
    
    📦 Deployment
    - Packaged application as `.exe` using **PyInstaller**:
      ```bash
      pyinstaller --onefile --icon=icon.ico ZipHandle.py
      ```
    - Verified functionality on systems without Python installed.
    
    🧰 Additional Stack
    - `Tkinter` – GUI framework
    - `PyInstaller` – EXE bundling tool
    
    ---
    
📈 Results
    - Fully working desktop tool .
    - Accurately processes nested ZIP-PDF structures.
    - Fast and scalable processing using multithreading.
    - Professional UI and easy deployment as EXE.
    
    ---

## 📄 Final Status
✅ Core extractor developed  
✅ GUI interface added  
✅ Deployed as standalone EXE
