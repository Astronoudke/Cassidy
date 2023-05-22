from collections import defaultdict
from itertools import combinations
from sklearn.feature_extraction.text import CountVectorizer


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
