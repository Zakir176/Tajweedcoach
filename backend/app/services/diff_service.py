import re
import difflib

def normalize(text: str) -> str:
    import re
    # Remove diacritics
    text = re.sub(r'[\u0610-\u061A\u064B-\u065F\u0670]', '', text)
    # Normalize alef variants
    text = re.sub(r'[أإآٱ]', 'ا', text)
    # Normalize teh marbuta
    text = re.sub(r'ة', 'ه', text)
    # Normalize yeh
    text = re.sub(r'ى', 'ي', text)
    # Normalize waw
    text = re.sub(r'ؤ', 'و', text)
    # Remove tatweel
    text = re.sub(r'ـ', '', text)
    # Remove non-Arabic characters
    text = re.sub(r'[^\u0600-\u06FF\s]', '', text)
    # Normalize whitespace
    text = ' '.join(text.split())
    return text

def compare_recitation(expected_text: str, transcribed_text: str):
    """
    Compare expected vs transcribed Arabic text at the word level.
    Returns (accuracy_score, diff_list).
    """
    # Normalize expected and transcribed texts
    clean_expected = normalize(expected_text)
    clean_transcribed = normalize(transcribed_text)
    
    # Split into words and remove punctuation noise
    expected_words_raw = expected_text.split()
    expected_words_clean = clean_expected.split()
    transcribed_words_clean = clean_transcribed.split()
    
    matcher = difflib.SequenceMatcher(None, expected_words_clean, transcribed_words_clean)
    diff_results = []
    
    # We walk through the expected words and mark status
    # Note: We use the raw expected words for the display, but clean ones for the match
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            for i in range(i1, i2):
                if i < len(expected_words_raw):
                    diff_results.append({"word": expected_words_raw[i], "status": "correct"})
        elif tag == 'replace' or tag == 'delete':
            for i in range(i1, i2):
                if i < len(expected_words_raw):
                    diff_results.append({"word": expected_words_raw[i], "status": "incorrect"})
                
    accuracy = sum(1 for d in diff_results if d["status"] == "correct") / len(diff_results) if diff_results else 0
    return round(accuracy, 2), diff_results
