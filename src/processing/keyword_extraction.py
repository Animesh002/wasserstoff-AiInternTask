import re
from collections import Counter

def clean_text(text):
    """Cleans the text by removing special characters and extra spaces."""
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with single space
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    return text.lower()

def extract_keywords(text):
    """Extracts a single keyword based on the overall content of the document."""
    cleaned_text = clean_text(text)
    words = cleaned_text.split()
    
    # Filter out common stop words or generic words, adjust as needed
    stop_words = set([
        'the', 'is', 'and', 'in', 'to', 'with', 'that', 'of', 'for', 
        'as', 'a', 'on', 'are', 'by', 'it', 'this', 'an', 'be', 'at', 'was', 'or', 'from', 'The', 
        'an', 'be', 'at', 'was', 'or', 'from', 'for', 'as', 'a', 'on', 'are', 'by', 'it', 'this', 'an', 'be', 'at', 'was', 'or', 'from',
    ])
    filtered_words = [word for word in words if word not in stop_words and len(word) > 1]
    
    # Get the most common word that reflects the theme of the document
    if filtered_words:
        word_freq = Counter(filtered_words)
        # Return the most common word
        return word_freq.most_common(1)[0][0]
    
    return 'general'  # Fallback if no specific keyword found
