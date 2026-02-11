import spacy
import sys

def extract_entities(text):
    """
    Extracts entities from the given Portuguese text using spaCy.
    """
    try:
        nlp = spacy.load("pt_core_news_lg")
    except OSError:
        print("Model not found. Please run: python -m spacy download pt_core_news_lg")
        return

    # Add EntityRuler for better date extraction
    ruler = nlp.add_pipe("entity_ruler", before="ner")
    patterns = [
        {"label": "DATE", "pattern": [{"LOWER": "próximo"}, {"LOWER": "mês"}]},
        {"label": "DATE", "pattern": [{"LOWER": "semana"}, {"LOWER": "que"}, {"LOWER": "vem"}]},
        {"label": "DATE", "pattern": [{"LOWER": "hoje"}]},
        {"label": "DATE", "pattern": [{"LOWER": "amanhã"}]},
        {"label": "DATE", "pattern": [{"LOWER": "ontem"}]},
        {"label": "DATE", "pattern": [{"LOWER": "uma"}, {"LOWER": "semana"}]},
        {"label": "DATE", "pattern": [
            {"LOWER": "dia", "OP": "?"},
            {"IS_DIGIT": True},
            {"LOWER": "de"},
            {"LOWER": {"IN": ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]}}
        ]}
    ]
    ruler.add_patterns(patterns)

    doc = nlp(text)

    print(f"Analyzing text: {text[:50]}...")
    print("-" * 30)
    print(f"{'Entity':<20} | {'Label':<10} | {'Description'}")
    print("-" * 30)

    for ent in doc.ents:
        print(f"{ent.text:<20} | {ent.label_:<10} | {spacy.explain(ent.label_)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            text = f.read()
        extract_entities(text)
    else:
        print("Usage: python extract.py <path_to_text_file>")
