import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from Extractor import FastPDFExtractor
import os
import threading
from pathlib import Path

class PDFExtractorGui:
    def __init__(self, root):
        self.root = root
        self.extractor = FastPDFExtractor()
        self.setup_window()
        self.create_interface()
        
    def setup_window(self):
        self.root.title("ZipWise")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        self.root.configure(bg='#ffffff')


        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - 300
        y = (self.root.winfo_screenheight() // 2) - 200
        self.root.geometry(f'600x400+{x}+{y}')
        
    def create_interface(self):
        self.zip_folder = tk.StringVar()
        self.output_file = tk.StringVar()
        self.is_processing = False

        main = tk.Frame(self.root, bg='#ffffff')
        main.pack(fill='both', expand=True, padx=40, pady=40)

        # Title
        tk.Label(main, text="ZipWise Data Extractor", 
                 font=('Segoe UI', 24), bg='#ffffff', fg='#2c3e50').pack(pady=(0, 30))

        # Inputs
        self.create_input_section(main)

        # Extract Button
        self.extract_btn = tk.Button(main, text="Start Extraction",
                                     font=('Segoe UI', 12, 'bold'),
                                     bg='#3498db', fg='white',
                                     activebackground='#2980b9',
                                     activeforeground='white',
                                     relief='flat', borderwidth=0,
                                     cursor='hand2',
                                     height=2, width=20,
                                     command=self.start_extraction)
        self.extract_btn.pack(pady=20)
        self.extract_btn.bind("<Enter>", lambda e: self.extract_btn.config(bg='#2980b9'))
        self.extract_btn.bind("<Leave>", lambda e: self.extract_btn.config(bg='#3498db'))

        # Progress bar
        self.progress = ttk.Progressbar(main, mode='indeterminate', length=200)
        self.progress.pack(pady=(0, 10))
        self.progress.stop()
        self.progress.place_forget()  # Hide initially

        # Status
        self.status = tk.Label(main, text="Ready", 
                               font=('Segoe UI', 10),
                               bg='#ffffff', fg='#7f8c8d')
        self.status.pack(pady=(10, 0))
        
    def create_input_section(self, parent):
        # ZIP Folder Selection
        self.add_input_row(parent, "ZIP Folder", self.zip_folder, self.browse_folder)
        
        # Output File Selection
        self.add_input_row(parent, "Output File", self.output_file, self.browse_output)

    def add_input_row(self, parent, label_text, variable, command):
        frame = tk.Frame(parent, bg='#ffffff')
        frame.pack(fill='x', pady=(0, 15))

        tk.Label(frame, text=label_text, font=('Segoe UI', 12), bg='#ffffff', fg='#2c3e50').pack(anchor='w')

        input_row = tk.Frame(frame, bg='#ffffff')
        input_row.pack(fill='x', pady=(5, 0))

        entry = tk.Entry(input_row, textvariable=variable,
                         font=('Segoe UI', 10), relief='solid', bd=1, state='readonly')
        entry.pack(side='left', fill='x', expand=True, ipady=5)

        browse_btn = tk.Button(input_row, text="Browse", 
                               font=('Segoe UI', 9), bg='#ecf0f1', fg='#2c3e50',
                               relief='flat', cursor='hand2',
                               command=command)
        browse_btn.pack(side='right', padx=(10, 0))
        
    def browse_folder(self):
        folder = filedialog.askdirectory(title="Select ZIP Files Folder")
        if folder:
            self.zip_folder.set(folder)
            self.update_status("Folder selected")

    def browse_output(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Save As"
        )
        if file_path:
            self.output_file.set(file_path)
            self.update_status("Output file selected")

    def update_status(self, message):
        self.status.config(text=message)
        self.root.update_idletasks()

    def start_extraction(self):
        if not self.zip_folder.get() or not self.output_file.get():
            messagebox.showerror("Error", "Please select both ZIP folder and output file.")
            return

        if not os.path.isdir(self.zip_folder.get()):
            messagebox.showerror("Error", "Invalid folder path.")
            return

        if not list(Path(self.zip_folder.get()).glob("*.zip")):
            messagebox.showwarning("Warning", "No ZIP files found in selected folder.")
            return

        self.is_processing = True
        self.extract_btn.config(text="Processing...", state='disabled', bg='#95a5a6')
        self.progress.place(relx=0.5, rely=0.85, anchor='center')
        self.progress.start()
        self.update_status("Extracting data...")

        threading.Thread(target=self.extract_data, daemon=True).start()

    def extract_data(self):
        try:
            self.extractor.process_all_zips(self.zip_folder.get(), self.output_file.get())
            self.root.after(0, self.extraction_complete)
        except Exception as e:
            self.root.after(0, lambda: self.extraction_error(str(e)))

    def extraction_complete(self):
        self.is_processing = False
        self.extract_btn.config(text="Start Extraction", state='normal', bg='#3498db')
        self.progress.stop()
        self.progress.place_forget()
        self.update_status("Extraction completed successfully")
        filename = os.path.basename(self.output_file.get())
        messagebox.showinfo("Success", f"Data extracted to: {filename}")

    def extraction_error(self, error):
        self.is_processing = False
        self.extract_btn.config(text="Start Extraction", state='normal', bg='#3498db')
        self.progress.stop()
        self.progress.place_forget()
        self.update_status("Extraction failed")
        messagebox.showerror("Error", f"Extraction failed:\n{error}")

def main():
    root = tk.Tk()
    app = PDFExtractorGui(root)
    root.mainloop()

if __name__ == "__main__":
    main()
