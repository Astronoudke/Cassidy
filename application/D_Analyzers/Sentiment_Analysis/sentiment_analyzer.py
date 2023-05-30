import spacy
from textblob import TextBlob
import stanza


class SentimentAnalyzer:
    def __init__(self, text):
        self.text = text
        #stanza.download('en')  # Download the English model
        #self.nlp = stanza.Pipeline('en')  # Initialize the English pipeline

    def analyze(self, model):
        analysis = getattr(self, model)(self.text)
        return analysis

    def textblob_analysis(self, text):
        blob = TextBlob(text)

        # Return the sentiment polarity
        return round(blob.sentiment.polarity, 2)

    def stanza_analysis(self, text):
        doc = self.nlp(text)

        # Calculate and return the average sentiment polarity of the sentences in the text
        avg_sentiment = sum([sentence.sentiment for sentence in doc.sentences]) / len(doc.sentences)
        return round(avg_sentiment, 2)
