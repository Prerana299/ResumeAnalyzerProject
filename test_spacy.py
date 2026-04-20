import spacy

nlp = spacy.load("en_core_web_sm")

doc = nlp("Prerana is building a resume analyzer project.")

for token in doc:
    print(token.text, token.pos_)
