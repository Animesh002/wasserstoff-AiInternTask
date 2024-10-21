import re
from collections import Counter

def clean_text(text):
    """Cleans the text by removing special characters and extra spaces."""
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with single space
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    return text.lower()

def get_sentence_scores(text):
    """Calculates scores for each sentence based on word frequency."""
    cleaned_text = clean_text(text)
    words = cleaned_text.split()
    word_freq = Counter(words)

    sentences = text.split('. ')
    sentence_scores = {}

    for sentence in sentences:
        sentence_cleaned = clean_text(sentence)
        sentence_word_count = len(sentence_cleaned.split())
        sentence_score = sum(word_freq.get(word, 0) for word in sentence_cleaned.split())

        # Average score per word in the sentence
        if sentence_word_count > 0:
            sentence_scores[sentence] = sentence_score / sentence_word_count
    
    return sentence_scores

def summarize_text(text, ratio=0.3):
    """Generates a summary by selecting the top sentences based on their scores."""
    sentence_scores = get_sentence_scores(text)
    ranked_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)

    # Select top sentences to form the summary
    summary_length = max(1, int(len(ranked_sentences) * ratio))  # Ensure at least one sentence
    summary_sentences = ranked_sentences[:summary_length]
    return '. '.join(summary_sentences) + '.'
