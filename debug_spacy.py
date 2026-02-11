import spacy

nlp = spacy.load("pt_core_news_lg")
text = "Eu quero viajar para o Rio de Janeiro no dia 28 de Março saindo da cidade de Curitiba e vou ficar hospedado na cidade de Vassouras O Retorno é no dia 5 de Março obrigado"
doc = nlp(text)

for token in doc:
    print(f"Token: {token.text:15} | POS: {token.pos_:6} | Nerve: {token.ent_type_:6} | Dep: {token.dep_}")

print("\nEntities found:")
for ent in doc.ents:
    print(f"Entity: {ent.text:20} | Label: {ent.label_}")
