import fitz  
import polars as pl  
import zipfile
import re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from datetime import datetime
import os
from typing import List, Dict, Tuple

class FastPDFExtractor:
    def __init__(self):
        self.patterns = {
            'date': re.compile(r'Created Date:\s*(\d{4}-\d{2}-\d{2})'),
            'duration': re.compile(r'Duration\s+(\d+)\s+Days'),
            'entry_type': re.compile(r'Entry\s+(Single Entry|Multiple Entry)'),
            'nationality': re.compile(r'Current Nationality\s+([A-Z]+)'),
            'name': re.compile(r'Applicant:\s*([A-Z\s]+)', re.MULTILINE),
            'passport': re.compile(r'Passport Number\s+([A-Z0-9]+)'),
            'dob': re.compile(r'Date of Birth\s+(\d{4}-\d{2}-\d{2})')
        }
    
    def extract_text_fast(self, pdf_path: str) -> str:
        """Ultra-fast PDF text extraction using PyMuPDF"""
        try:
            doc = fitz.open(pdf_path)
            # Extract text 
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text
        except:
            return ""
    
    def extract_data_from_text(self, text: str, file_path: str, has_multiple_files: bool) -> Dict:
        #Extract data using regex
        data = {
            'File Name': file_path,
            'DATE': '',
            'TYPE DR': '',
            'TYPE OP': '',
            'NATIONALITY': '',
            'NAME': '',
            'PASSPORT NO': '',
            'DOB': '',
            'Folder Contains Multiple Files': has_multiple_files
        }
        
        # pattern matching
        date_match = self.patterns['date'].search(text)
        if date_match:
            # Convert date format eg: 2025-04-04 to 04-04-2025
            date_obj = datetime.strptime(date_match.group(1), '%Y-%m-%d')
            data['DATE'] = date_obj.strftime('%d-%m-%Y')
        
        duration_match = self.patterns['duration'].search(text)
        if duration_match:
            data['TYPE DR'] = f"{duration_match.group(1)} Days"
        
        entry_match = self.patterns['entry_type'].search(text)
        if entry_match:
            data['TYPE OP'] = entry_match.group(1)
        
        nationality_match = self.patterns['nationality'].search(text)
        if nationality_match:
            data['NATIONALITY'] = nationality_match.group(1)
        
        name_match = self.patterns['name'].search(text)
        if name_match:
            full_name = name_match.group(1).strip()
            data['NAME'] = ' '.join(full_name.split()[:2])

        
        passport_match = self.patterns['passport'].search(text)
        if passport_match:
            data['PASSPORT NO'] = passport_match.group(1)
        
        dob_match = self.patterns['dob'].search(text)
        if dob_match:
            # Convert date format eg: 1978-03-25 to 25-03-1978
            dob_obj = datetime.strptime(dob_match.group(1), '%Y-%m-%d')
            data['DOB'] = dob_obj.strftime('%d-%m-%Y')
        
        return data
    
    def process_single_pdf(self, pdf_path: Path, has_multiple_files: bool) -> Dict:
        """Process a single PDF file"""
        text = self.extract_text_fast(str(pdf_path))
        return self.extract_data_from_text(text, str(pdf_path), has_multiple_files)
    
    def process_zip_file(self, zip_path: Path) -> List[Dict]:
        """Process a single ZIP file and return extracted data"""
        results = []
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Extract to temporary directory
            temp_dir = Path(f"temp_{zip_path.stem}")
            zip_ref.extractall(temp_dir)
            
            try:
                # Navigate to the date folder (e.g., 05.04.2025)
                date_folders = [d for d in temp_dir.iterdir() if d.is_dir()]
                
                for date_folder in date_folders:
                    # Get passport number folders (e.g., Z8152290, Z8159689, etc.)
                    passport_folders = [d for d in date_folder.iterdir() if d.is_dir()]
                    
                    for passport_folder in passport_folders:
                        # Check if eVisa.pdf exists (Type B) or not (Type A)
                        evisa_exists = (passport_folder / "eVisa.pdf").exists()
                        has_multiple_files = evisa_exists
                        
                        # Find the "New Tourism Entry Permit" PDF
                        permit_pdfs = list(passport_folder.glob("New Tourism Entry Permit*.pdf"))
                        
                        for permit_pdf in permit_pdfs:
                            result = self.process_single_pdf(permit_pdf, has_multiple_files)
                            results.append(result)
            
            finally:
                # Cleanup temp directory
                import shutil
                if temp_dir.exists():
                    shutil.rmtree(temp_dir)
        
        return results
    
    def process_all_zips(self, zip_folder: str, output_file: str = "Output.csv"):
        """Process all ZIP files in parallel for maximum speed"""
        zip_folder_path = Path(zip_folder)
        zip_files = list(zip_folder_path.glob("*.zip"))
        
        if not zip_files:
            print("No ZIP files found!")
            return
        
        print(f"Processing {len(zip_files)} ZIP files...")
        
        # Process ZIP files in parallel for maximum speed
        all_results = []
        with ThreadPoolExecutor(max_workers=min(len(zip_files), os.cpu_count())) as executor:
            zip_results = list(executor.map(self.process_zip_file, zip_files))
            
        # Flatten results
        for result_list in zip_results:
            all_results.extend(result_list)
        
        if all_results:
            # Use Polars for ultra-fast DataFrame operations
            df = pl.DataFrame(all_results)
            df.write_csv(output_file)
            print(f"Processed {len(all_results)} records in {output_file}")
            
            # Print summary
            type_a_count = sum(1 for r in all_results if not r['Folder Contains Multiple Files'])
            type_b_count = sum(1 for r in all_results if r['Folder Contains Multiple Files'])
            print(f"Type A folders (Permit only): {type_a_count}")
            print(f"Type B folders (Permit + eVisa): {type_b_count}")
        else:
            print("No data extracted!")

# Usage
if __name__ == "__main__":
    extractor = FastPDFExtractor()
    
    # Process all ZIP files in the specified folder
    zip_folder =r"D:\Opine Infotech Internship\Project1\Problem"  # path to zip file
    extractor.process_all_zips(zip_folder,r"D:\Opine Infotech Internship\Project1\Solution\op.csv" )