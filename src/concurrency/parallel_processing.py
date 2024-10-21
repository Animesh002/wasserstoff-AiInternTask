import threading

def process_pdf_concurrently(pdf_paths, process_function):
    """Process PDFs concurrently using threading."""
    threads = []
    
    for pdf_path in pdf_paths:
        thread = threading.Thread(target=process_function, args=(pdf_path,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print("All PDF files processed successfully.")
