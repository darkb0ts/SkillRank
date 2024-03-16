import nltk  # Assuming NLTK for preprocessing
import spacy

nlp = spacy.load("en_core_web_sm")


def extract_skills(text):
    doc = nlp(text)
    skills = [ent.text for ent in doc.ents if ent.label_ == "SKILL"]
    return skills


def preprocess_resume(text):
    # Lowercase, remove punctuation, tokenize, etc.
    tokens = nltk.word_tokenize(text.lower())
    # Apply further processing (e.g., stemming, lemmatization) as needed
    return tokens
