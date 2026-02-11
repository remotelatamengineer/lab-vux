import spacy
import sys

print("Python executable:", sys.executable)
print("Spacy version:", spacy.__version__)

try:
    print("Loading blank model 'pt'...")
    nlp = spacy.blank("pt")
    print("Blank model loaded successfully.")

    print("Loading 'pt_core_news_lg' with all components disabled...")
    nlp = spacy.load("pt_core_news_lg", disable=["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer", "ner"])
    print("Disabled model loaded successfully.")

    print("Loading 'pt_core_news_lg' full...")
    nlp = spacy.load("pt_core_news_lg")
    print("Full model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    import traceback
    traceback.print_exc()
