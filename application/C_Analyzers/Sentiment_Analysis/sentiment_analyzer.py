import spacy
from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer

import nltk
nltk.download('vader_lexicon')


class SentimentAnalyzer:
    def __init__(self, text):
        self.text = text

    def analyze(self, model):
        analysis = getattr(self, model)(self.text)
        return analysis

    def textblob_analysis(self, text):
        blob = TextBlob(text)

        # Return the sentiment polarity
        return round(blob.sentiment.polarity, 2)

    def vader_analysis(self, text):
        vader_analyzer = SentimentIntensityAnalyzer()  # Initialize the VADER sentiment intensity analyzer
        sentiment = vader_analyzer.polarity_scores(text)

        # Return the compound sentiment score
        return sentiment['compound']
