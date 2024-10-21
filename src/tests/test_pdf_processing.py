import os
import sys
import unittest
from pymongo import MongoClient

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from processing.summarization import summarize_text
from processing.keyword_extraction import extract_keywords
from main import process_pdf  # Adjust this import based on your main function

class TestPDFProcessing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Setup MongoDB connection
        cls.client = MongoClient('mongodb://localhost:27017')
        cls.db = cls.client['pdf_metadata_db']
        cls.collection = cls.db['pdf_metadata']

        # Example PDF file for testing (ensure this PDF exists for the tests)
        cls.test_pdf_path = os.path.join(os.path.dirname(__file__), '../data/input_pdfs/sample.pdf')
    
    @classmethod
    def tearDownClass(cls):
        # Clean up: drop the test collection
        cls.db.drop_collection(cls.collection.name)
        cls.client.close()

    def test_summarization(self):
        """Test summarization functionality."""
        text = "This is a simple text for testing the summarization function."
        summary = summarize_text(text, ratio=0.5)
        self.assertIsInstance(summary, str)
        self.assertGreater(len(summary), 0)

    def test_keyword_extraction(self):
        """Test keyword extraction functionality."""
        text = "Keyword extraction is the process of identifying key terms."
        keywords = extract_keywords(text)
        self.assertIsInstance(keywords, list)
        self.assertGreater(len(keywords), 0)

    def test_process_pdf(self):
        """Test the process_pdf function."""
        result = process_pdf(self.test_pdf_path, status_label=None)
        self.assertIn("Metadata for", result)

    def test_performance_benchmark(self):
        """Benchmark the performance of the process_pdf function."""
        import time
        start_time = time.time()
        process_pdf(self.test_pdf_path, status_label=None)
        end_time = time.time()
        processing_time = end_time - start_time
        self.assertLess(processing_time, 5)  # Adjust this threshold as needed

if __name__ == '__main__':
    unittest.main()
