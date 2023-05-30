from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict


class WordCounter:
    def __init__(self, text):
        self.text = text

    def analyze(self, model, top_n=10):
        analysis = getattr(self, model)(self.text, top_n)
        return analysis

    def tfidf_relations(self, sentences, top_n):
        # Create a list to hold all noun bigrams
        all_noun_bigrams = []

        # Go through each sentence
        for sentence in sentences:
            # Create a list to hold the bigrams in the current sentence
            sentence_bigrams = [" ".join(bigram) for bigram in zip(sentence[:-1], sentence[1:])]
            # Add the bigrams to the all_noun_bigrams list
            all_noun_bigrams.extend(sentence_bigrams)

        # Vectorize the text using TF-IDF
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(all_noun_bigrams)

        # Create a dictionary to hold the scores for each bigram
        tfidf_scores = defaultdict(int)

        # Go through each bigram and its score
        for bigram, index in tfidf_vectorizer.vocabulary_.items():
            score = tfidf_matrix.sum(axis=0).tolist()[0][index]
            tfidf_scores[bigram] = score

        # Sort the scores in descending order
        sorted_scores = sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)

        # Return the top n bigrams with their scores
        top_bigrams = sorted_scores[:top_n]
        print(top_bigrams)
        return top_bigrams
