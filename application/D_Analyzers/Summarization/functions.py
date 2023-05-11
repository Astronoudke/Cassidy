import networkx as nx
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


class TextRank:
    def sentence_similarity(self, sent1, sent2, stopwords=None):
        if sent1 is None or sent2 is None:
            return 0

        sent1 = [w.lower() for w in sent1.split()]
        sent2 = [w.lower() for w in sent2.split()]

        all_words = list(set(sent1 + sent2))

        vector1 = [0] * len(all_words)
        vector2 = [0] * len(all_words)

        # build the vector for the first sentence
        for w in sent1:
            if w in stopwords:
                continue
            vector1[all_words.index(w)] += 1

        # build the vector for the second sentence
        for w in sent2:
            if w in stopwords:
                continue
            vector2[all_words.index(w)] += 1

        return 1 - cosine_similarity([vector1], [vector2])

    def build_similarity_matrix(self, sentences, stopwords=None):
        # Create an empty similarity matrix
        similarity_matrix = np.zeros((len(sentences), len(sentences)))

        for idx1 in range(len(sentences)):
            for idx2 in range(len(sentences)):
                if idx1 == idx2:  # ignore if both are same sentences
                    continue
                similarity_matrix[idx1][idx2] = self.sentence_similarity(sentences[idx1], sentences[idx2],
                                                                    stopwords)

        return similarity_matrix
