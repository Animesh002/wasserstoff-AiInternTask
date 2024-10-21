import os
import json
import requests
import logging
from pymongo import MongoClient, errors

# Paths
DATASET_PATH = os.path.join(os.path.dirname(__file__), '../../data/Dataset.json')
INPUT_PDFS_PATH = os.path.join(os.path.dirname(__file__), '../../data/input_pdfs/')
LOGS_PATH = os.path.join(os.path.dirname(__file__), '../../data/logs/error.log')

# Setup logging
logging.basicConfig(filename=LOGS_PATH, level=logging.ERROR, 
                    format='%(asctime)s %(levelname)s %(message)s')

# MongoDB Setup (assuming MongoDB is running locally on default port 27017)
try:
    client = MongoClient('mongodb://localhost:27017')
    db = client['pdf_metadata_db']  # Database
    pdf_metadata_collection = db['pdf_metadata']  # Collection
    print("Connected to MongoDB successfully")
except errors.ConnectionFailure as e:
    logging.error(f"Failed to connect to MongoDB: {e}")
    print("Failed to connect to MongoDB. Please check if MongoDB is running.")
    exit()

def download_pdfs():
    """Downloads PDFs from URLs in Dataset.json and stores metadata in MongoDB."""
    
    # Ensure input_pdfs folder exists
    if not os.path.exists(INPUT_PDFS_PATH):
        os.makedirs(INPUT_PDFS_PATH)
    
    try:
        # Read Dataset.json
        with open(DATASET_PATH, 'r') as f:
            pdf_urls = json.load(f)

        for pdf_name, pdf_url in pdf_urls.items():
            try:
                # Check if this PDF already exists in MongoDB
                existing_pdf = pdf_metadata_collection.find_one({'pdf_name': f"{pdf_name}.pdf"})
                
                if existing_pdf:
                    print(f"Metadata for {pdf_name}.pdf already exists in MongoDB. Skipping download.")
                    continue  # Skip this PDF if it's already in the database

                # Define the path to save the PDF
                pdf_file_path = os.path.join(INPUT_PDFS_PATH, f"{pdf_name}.pdf")
                
                # Download the PDF
                response = requests.get(pdf_url)
                response.raise_for_status()

                # Save the PDF to input_pdfs folder
                with open(pdf_file_path, 'wb') as pdf_file:
                    pdf_file.write(response.content)
                
                # Get PDF size in bytes
                pdf_size = os.path.getsize(pdf_file_path)

                # Log metadata to MongoDB (including the file path)
                pdf_metadata = {
                    'pdf_name': f"{pdf_name}.pdf",
                    'pdf_size': pdf_size,  # Size in bytes
                    'pdf_path': pdf_file_path  # Path to the PDF file
                }

                # Insert the metadata into MongoDB
                result = pdf_metadata_collection.insert_one(pdf_metadata)
                
                if result.inserted_id:
                    print(f"Successfully stored metadata for {pdf_name}.pdf in MongoDB")
                else:
                    print(f"Failed to insert metadata for {pdf_name}.pdf into MongoDB")

            except requests.exceptions.RequestException as e:
                # Log any download issues to the error log
                logging.error(f"Error downloading {pdf_name}: {e}")
                print(f"Failed to download {pdf_name}.pdf. Error logged.")

    except Exception as e:
        logging.error(f"Error processing Dataset.json: {e}")
        print(f"Failed to process Dataset.json. Error logged.")
