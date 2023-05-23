import networkx as nx
from nltk.corpus import stopwords

from .functions import TextRank


class ExtractiveSummarizer:
    def __init__(self, sentences):
        self.sentences = sentences
        self.text_rank = TextRank()

    def summarize(self, model, top_n=3, order_by_rank=True):
        summarization = getattr(self, model)(self.sentences, top_n, order_by_rank)
        return summarization

    def lead_3(self, sentences, top_n=3, order_by_rank=True):
        """
        Returns the first three sentences of the text.
        :return:
        """
        summary = " ".join(sentence.rstrip('.') for sentence in sentences[:min(3, len(sentences))])
        return summary + '.'

    def textrank(self, sentences, top_n=3, order_by_rank=True):
        stop_words = stopwords.words('english')

        if len(sentences) <= top_n:
            # Remove trailing periods and join sentences
            return " ".join(sentence.rstrip('.') for sentence in sentences) + '.'

        # Build the similarity matrix
        sentence_similarity_matrix = self.text_rank.build_similarity_matrix(sentences, stop_words)

        # Rank sentences in similarity matrix
        sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_matrix)
        scores = nx.pagerank(sentence_similarity_graph)

        # Sort the rank and pick top sentences
        ranked_sentence = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)

        # Pick top sentences based on user preference for ranking or original order
        if order_by_rank:
            summarize_text = [ranked_sentence[i][1] for i in range(top_n)]
        else:
            # Get the indices of the top_n sentences in their original order
            original_order_indices = sorted([i for i in range(len(sentences)) if sentences[i] in [item[1] for item in ranked_sentence[:top_n]]])
            summarize_text = [sentences[i] for i in original_order_indices]

        # Output the summarize text
        return " ".join(summarize_text) + '.'