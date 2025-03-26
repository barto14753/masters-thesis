import spacy

# Load the English language model
nlp = spacy.load("en_core_web_sm")

# Example sentence
text = "Language models are very powerful tool."

# Process the text
doc = nlp(text)

# Print syntactic analysis
for token in doc:
    print(f"{token.text:<12} | POS: {token.pos_:<10} | Dep: {token.dep_:<15} | Head: {token.head.text}")
