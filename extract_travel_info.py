import spacy
import sys
from datetime import date, datetime, timedelta


def parse_date_text(text_date):
    """
    Converts Portuguese natural language date expressions into Python date objects.
    """
    today = date.today()
    text_date = text_date.lower().strip()

    # Relative dates
    if "hoje" in text_date:
        return today
    if "amanhã" in text_date:
        return today + timedelta(days=1)
    if "ontem" in text_date:
        return today - timedelta(days=1)

    # Standard date: "dia 1 de março" or "28 de fevereiro"
    months = {
        "janeiro": 1, "fevereiro": 2, "março": 3, "abril": 4, "maio": 5, "junho": 6,
        "julho": 7, "agosto": 8, "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12
    }

    words = text_date.replace("dia", "").replace(" de ", " ").split()
    day = None
    month = None

    for word in words:
        if word.isdigit():
            day = int(word)
        elif word in months:
            month = months[word]

    if day and month:
        # Default to current year, or next year if date has passed (simplistic)
        year = today.year
        try:
            parsed_date = date(year, month, day)
            # If the user is talking about a flight and the date is in the past, assume next year
            if parsed_date < today:
                parsed_date = date(year + 1, month, day)
            return parsed_date
        except ValueError:
            return text_date

    return text_date

def extract_travel_info(text):
    """
    Extracts travel details (Origin, Destination, Booking City, Dates) from the text.
    """
    travel_info = {
        "Flight From": None,
        "Flight Destination": None,
        "Booking City": None,
        "Date From": None,
        "Date To": None
    }
    try:
        nlp = spacy.load("pt_core_news_lg")
    except OSError:
        print("Model not found. Please run: python -m spacy download pt_core_news_lg")
        return

    # Add EntityRuler for better date extraction
    ruler = nlp.add_pipe("entity_ruler", before="ner")
    # ... patterns omitted for brevity, logic remains same ...
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

 
    for ent in doc.ents:
        if ent.label_ in ["LOC", "GPE"]:
            # Check dependency parse for context
            head = ent.root.head
            # Check for "Flight From" (saindo de, voar de)
            if head.text.lower() in ["embarcar", "saindo", "partindo", "origem", "de"]:
                 if travel_info["Flight From"] is None:
                    travel_info["Flight From"] = ent.text
            
            # Check for "Flight Destination" (para, ir, viajar)
            # Often 'para' is the head or a preposition child
            elif head.text.lower() in ["para", "ir", "viagem", "destino","viajar"]:
                if travel_info["Flight Destination"] is None:
                     travel_info["Flight Destination"] = ent.text
            
            # Check for "Booking City" (hotel, ficar, em)
            # Logic: Look for "hotel" or "ficar" in the same sentence or dependency chain
            elif head.text.lower() in ["hospedado", "em", "no", "na","ficar", "hotel", "hospedar", "estar", "hospedagem"]:
                 if travel_info["Booking City"] is None:
                      travel_info["Booking City"] = ent.text

        elif ent.label_ == "DATE":
            # If we have a vague date like "próximo mês", overwrite it
            parsed_val = parse_date_text(ent.text)
            if travel_info["Date From"] is None:
                travel_info["Date From"] = parsed_val
            elif travel_info["Date To"] is None:
                travel_info["Date To"] = parsed_val
             
    # Print extracted info
    print("-" * 30)
    print("Extracted Travel Information:")
    print("-" * 30)
    for key, value in travel_info.items():
        if value is not None:
            print(f"{key}: {value}")
        else:
            input(f"{key} is not clear, please provide the value: ")



if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            text = f.read()
        extract_travel_info(text)
    else:
        print("Usage: python extract_travel_info.py <path_to_text_file>")
