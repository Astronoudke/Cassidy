import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

nlp = spacy.load('en_core_web_sm')
nlp.add_pipe('spacytextblob')


class SentimentAnalyzer:
    def __init__(self):

    def analyze(self, model, text):
        analysis = getattr(self, model)(text)
        return analysis

    def simple_spacy(self, text):
        doc = nlp(text)
        print('Polarity:', doc._.polarity)
        print('Subjectivity:', doc._.subjectivity)