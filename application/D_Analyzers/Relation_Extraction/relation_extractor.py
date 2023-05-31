from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
from itertools import combinations
from nltk import word_tokenize, pos_tag


class RelationExtractor:
    def __init__(self, sentences):
        self.sentences = sentences

    def extract(self, model, top_n=10):
        extraction = getattr(self, model)(self.sentences, top_n)
        return extraction

    def co_occurrence(self, sentences, top_n):
        # Create a dictionary to hold co-occurrence counts
        co_occurrences = defaultdict(int)

        # Go through each sentence
        for sentence in sentences:
            # For each pair of words in the sentence, increment the count in the dictionary
            for word1, word2 in combinations(sentence, 2):
                if word1 > word2:   # Ensure the pair is in a consistent order
                    word1, word2 = word2, word1
                co_occurrences[(word1, word2)] += 1

        # Sort the co-occurrences in descending order
        sorted_co_occurrences = sorted(co_occurrences.items(), key=lambda x: x[1], reverse=True)

        # Return the top n pairs without their counts
        top_pairs = [pair for pair, count in sorted_co_occurrences[:top_n]]
        return top_pairs

    def tfidf_relations(self, sentences, top_n):
        # Flatten the list of sentences to feed to the vectorizer
        all_nouns = [noun for sublist in sentences for noun in sublist]

        # Vectorize the text using TF-IDF with bigrams
        tfidf_vectorizer = TfidfVectorizer(ngram_range=(2, 2))
        tfidf_matrix = tfidf_vectorizer.fit_transform(all_nouns)

        # Create a dictionary to hold the scores for each bigram
        tfidf_scores = defaultdict(int)

        # Go through each bigram and its score
        for bigram, index in tfidf_vectorizer.vocabulary_.items():
            score = tfidf_matrix.sum(axis=0).tolist()[0][index]
            tfidf_scores[bigram] = score

        # Sort the scores in descending order
        sorted_scores = sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)

        # Return the top n bigrams without their scores
        top_bigrams = [tuple(bigram.split(' ')) for bigram, score in sorted_scores[:top_n]]
        print(top_bigrams)
        return top_bigrams

