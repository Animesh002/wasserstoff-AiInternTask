# PDF Processing Application

This is a PDF processing application built with Python, MongoDB, and Tkinter. It allows users to select and process one or more PDFs, generating summaries and extracting keywords. The metadata, including the summary, keywords, and processing performance metrics (time taken, number of pages), is stored in a MongoDB database, and optionally, performance metrics are also saved to a CSV file.

## Features

- Select and process multiple PDFs simultaneously.
- Extract text from PDFs and summarize based on document length.
  - Long summary for documents with more than 10 pages.
  - Short summary for documents with 10 or fewer pages.
- Extract keywords from the content of the PDFs.
- Store metadata (summary, keywords, document name) into MongoDB.
- Track and save performance metrics such as the number of pages and processing time to both MongoDB and a CSV file.

## Technologies Used

- **Python**: Core language for building the application.
- **Tkinter**: For creating a graphical user interface (GUI).
- **MongoDB**: Database for storing PDF metadata (summary, keywords, performance metrics).
- **PyPDF2**: For extracting text content from PDF files.
- **Custom Summarization & Keyword Extraction**: Basic implementations for text summarization and keyword extraction.
- **CSV**: (Optional) Storing performance metrics in a CSV file.

## Setup and Installation

### Prerequisites

1. **Python 3.8+** installed on your machine.
2. **MongoDB** installed locally or access to a remote MongoDB server.
3. Install the required Python packages by running the following command:

```bash
pip install -r requirements.txt
```
