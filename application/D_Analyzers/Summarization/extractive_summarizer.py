import networkx as nx
from nltk.corpus import stopwords

from .functions import TextRank


class ExtractiveSummarizer:
    def __init__(self, sentences):
        self.sentences = sentences
        self.text_rank = TextRank()

    def summarize(self, model, top_n=3):
        summarization = getattr(self, model)(self.sentences, top_n)
        return summarization

    def lead_3(self, sentences):
        """
        Returns the first three sentences of the text.
        :return:
        """
        summary = ". ".join(sentences[:min(3, len(sentences))])
        return summary


    def textrank(self, sentences, top_n=3):
        stop_words = stopwords.words('english')

        if len(sentences) <= top_n:
            return ". ".join(sentences)

        # Build the similarity matrix
        sentence_similarity_matrix = self.text_rank.build_similarity_matrix(sentences, stop_words)

        # Rank sentences in similarity matrix
        sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_matrix)
        scores = nx.pagerank(sentence_similarity_graph)

        # Sort the rank and pick top sentences
        ranked_sentence = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)

        summarize_text = []
        for i in range(top_n):
            summarize_text.append(ranked_sentence[i][1])

        # Output the summarize text
        return ". ".join(summarize_text)
