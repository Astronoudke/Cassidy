import networkx as nx
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

from .functions import TextRank


class ExtractiveSummarizer:
    def __init__(self, sentences):
        self.sentences = sentences
        self.text_rank = TextRank()

    def lead_3(self):
        """
        Returns the first three sentences of the text.
        :return:
        """
        summary = ". ".join(self.sentences[:3])
        return summary

    def textrank(self, top_n=3):
        stop_words = stopwords.words('english')

        # Here you will include the 'sentence_similarity' and 'build_similarity_matrix' functions
        # as nested functions or defined them separately

        # Build the similarity matrix
        sentence_similarity_matrix = self.text_rank.build_similarity_matrix(self.sentences, stop_words)

        # Rank sentences in similarity matrix
        sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_matrix)
        scores = nx.pagerank(sentence_similarity_graph)

        # Sort the rank and pick top sentences
        ranked_sentence = sorted(((scores[i], s) for i, s in enumerate(self.sentences)), reverse=True)

        summarize_text = []
        for i in range(top_n):
            summarize_text.append(ranked_sentence[i][1])

        # Output the summarize text
        return ". ".join(summarize_text) + "."
