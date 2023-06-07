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

        # Vectorize the text using TF-IDF
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(all_nouns)

        # Create a dictionary to hold the scores for each noun
        tfidf_scores = {noun: tfidf_matrix[0, index] for noun, index in tfidf_vectorizer.vocabulary_.items()}

        # Go through each sentence and generate all pairings of nouns
        noun_pairs_scores = defaultdict(int)
        for sublist in sentences:
            for pair in combinations(sublist, 2):
                # Compute the score for each pair as the sum or product of individual TF-IDF scores
                pair_score = tfidf_scores.get(pair[0], 0) * tfidf_scores.get(pair[1], 0)  # or use + for sum
                noun_pairs_scores[pair] += pair_score

        # Sort the scores in descending order
        sorted_scores = sorted(noun_pairs_scores.items(), key=lambda x: x[1], reverse=True)

        # Return the top n bigrams
        top_bigrams = [bigram for bigram, score in sorted_scores[:top_n]]
        print(top_bigrams)
        return top_bigrams
