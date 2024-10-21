import os
import tkinter as tk
from tkinter import filedialog, messagebox
from ingestion.pdf_ingestion import download_pdfs
from processing.summarization import summarize_text
from processing.keyword_extraction import extract_keywords
from concurrency.parallel_processing import process_pdf_concurrently
from pymongo import MongoClient
from PyPDF2 import PdfReader
import time  # For performance tracking
import csv   # To store metrics in CSV

# MongoDB Setup
client = MongoClient('mongodb://localhost:27017')
db = client['pdf_metadata_db']  # Database
pdf_metadata_collection = db['pdf_metadata']  # Collection
performance_metrics_collection = db['pdf_performance_metrics']  # Collection to store performance metrics

# CSV file to store performance metrics (optional)
csv_file = os.path.join(os.path.dirname(__file__), '../data/performance_metrics.csv')

def determine_summary_length(num_pages):
    """Determine the summary ratio based on the number of pages."""
    if num_pages > 10:
        return 0.5  # Long summary
    else:
        return 0.2  # Short summary

def process_pdf(pdf_path, status_label):
    """Processes a single PDF, extracting summary and keywords, and tracks performance metrics."""
    try:
        start_time = time.time()  # Start timing the processing
        status_label.config(text=f"Processing {os.path.basename(pdf_path)}, please wait...")
        root.update()

        with open(pdf_path, 'rb') as f:
            reader = PdfReader(f)
            pdf_content = ' '.join(page.extract_text() for page in reader.pages)

        num_pages = len(reader.pages)
        summary_ratio = determine_summary_length(num_pages)

        # Summarization
        summary = summarize_text(pdf_content, ratio=summary_ratio)

        # Keyword extraction
        keyword = extract_keywords(pdf_content)

        # End timing the processing
        end_time = time.time()
        processing_time = end_time - start_time  # Time taken to process the PDF

        # Update MongoDB with summary and keywords
        pdf_name = os.path.basename(pdf_path)
        pdf_metadata_collection.update_one(
            {'pdf_name': pdf_name},
            {'$set': {
                'summary': summary,
                'keyword': keyword,
                'summary_type': 'long' if summary_ratio == 0.5 else 'short'
            }},
            upsert=True
        )

        # Save performance metrics to MongoDB
        performance_metrics_collection.insert_one({
            'pdf_name': pdf_name,
            'num_pages': num_pages,
            'processing_time_seconds': processing_time,
            'summary_type': 'long' if summary_ratio == 0.5 else 'short'
        })

        # Optionally, save performance metrics to a CSV file
        save_metrics_to_csv(pdf_name, num_pages, processing_time, 'long' if summary_ratio == 0.5 else 'short')

        status_label.config(text=f"Processing of {pdf_name} complete!")

        return f"Metadata for {pdf_name} updated successfully in MongoDB"

    except Exception as e:
        status_label.config(text="Processing failed!")
        return f"Failed to process {pdf_path}: {e}"

def save_metrics_to_csv(pdf_name, num_pages, processing_time, summary_type):
    """Save performance metrics to a CSV file."""
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['PDF Name', 'Number of Pages', 'Processing Time (seconds)', 'Summary Type'])  # Header
        writer.writerow([pdf_name, num_pages, processing_time, summary_type])

def open_file_dialog(status_label):
    """Open a file dialog for the user to select multiple PDFs."""
    file_paths = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
    if file_paths:
        for file_path in file_paths:
            result = process_pdf(file_path, status_label)
            messagebox.showinfo("Processing Complete", result)
        ask_continue()

def ask_continue():
    """Ask the user if they want to process more PDFs or exit."""
    answer = messagebox.askquestion("Continue", "Do you want to process more PDFs?")
    if answer == "yes":
        # Reset the interface for the next PDF selection
        status_label.config(text="Click the button to select PDFs and process them")
    else:
        root.quit()

if __name__ == "__main__":
    # Create Tkinter window
    root = tk.Tk()
    root.title("PDF Processor")

    # Set window size
    root.geometry("400x250")

    # Create and place widgets
    label = tk.Label(root, text="Click the button to select PDFs and process them", pady=20)
    label.pack()

    # Status label to update during the processing
    status_label = tk.Label(root, text="", fg="blue")
    status_label.pack()

    button = tk.Button(root, text="Select PDFs", command=lambda: open_file_dialog(status_label), padx=20, pady=10)
    button.pack()

    # Run the Tkinter event loop
    root.mainloop()
