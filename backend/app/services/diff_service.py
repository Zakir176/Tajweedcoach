import re
import difflib

def strip_diacritics(text: str) -> str:
    """
    Remove all Arabic diacritics (harakat) for comparison.
    """
    # Pattern includes Arabic signs (U+0600-U+060F), fatha, damma, kasra, sukun, shadda, tatweel (U+0640), superscript alef (U+0670)
    return re.sub(r'[\u0600-\u060F\u0610-\u061A\u0640\u064B-\u065F\u0670]', '', text)

def normalize_arabic(text: str) -> str:
    """
    Normalize Arabic character variants for robust comparison.
    """
    # Replace alif variants with plain alif (included ٱ U+0671)
    text = re.sub(r'[أإآٱ]', 'ا', text)
    # Replace tey marbuta with heh
    text = re.sub(r'ة', 'ه', text)
    # Replace alef maksura with yeh
    text = re.sub(r'ى', 'ي', text)
    return text

def compare_recitation(expected_text: str, transcribed_text: str):
    """
    Compare expected vs transcribed Arabic text at the word level.
    Returns (accuracy_score, diff_list).
    """
    # Strip diacritics and normalize characters
    clean_expected = normalize_arabic(strip_diacritics(expected_text))
    clean_transcribed = normalize_arabic(strip_diacritics(transcribed_text))
    
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
                diff_results.append({"word": expected_words_raw[i], "status": "correct"})
        elif tag == 'replace' or tag == 'delete':
            for i in range(i1, i2):
                diff_results.append({"word": expected_words_raw[i], "status": "incorrect"})
                
    accuracy = sum(1 for d in diff_results if d["status"] == "correct") / len(diff_results) if diff_results else 0
    return round(accuracy, 2), diff_results
