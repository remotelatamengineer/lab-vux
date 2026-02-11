import spacy
import sys

def parse_phrases(text):
    """
    Parses the given text into phrases (sentences) using spaCy.
    """
    try:
        nlp = spacy.load("pt_core_news_lg")
    except OSError:
        print("Model not found. Please run: python -m spacy download pt_core_news_lg")
        return

    doc = nlp(text)

    print(f"Analyzing text for phrases...")
    print("-" * 30)
    
    for i, sent in enumerate(doc.sents, 1):
        print(f"Phrase {i}: {sent.text.strip()}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            text = f.read()
        parse_phrases(text)
    else:
        print("Usage: python parse_phrases.py <path_to_text_file>")
