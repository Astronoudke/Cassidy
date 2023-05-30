import networkx as nx
from nltk.corpus import stopwords
import numpy as np
from summarizer import Summarizer

from .functions import TextRank, RelevanceScores


class ExtractiveSummarizer:
    def __init__(self, sentences):
        self.sentences = sentences
        self.text_rank = TextRank()
        self.relevance = RelevanceScores()

    def summarize(self, model, top_n=3, order_by_rank=True):
        summarization = getattr(self, model)(self.sentences, top_n, order_by_rank)
        return summarization

    def lead_3(self, sentences, top_n=3, order_by_rank=True):
        """
        Returns the first three sentences of the text.
        :return:
        """
        summary = " ".join(sentence.rstrip('.') for sentence in sentences[:min(top_n, len(sentences))])
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

    def position_textrank(self, sentences, top_n=3, order_by_rank=True):
        stop_words = stopwords.words('english')

        if len(sentences) <= top_n:
            # Remove trailing periods and join sentences
            return " ".join(sentence.rstrip('.') for sentence in sentences) + '.'

        # Build the similarity matrix
        sentence_similarity_matrix = self.text_rank.build_similarity_matrix(sentences, stop_words)

        # Rank sentences in similarity matrix
        sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_matrix)
        scores = nx.pagerank(sentence_similarity_graph)

        # Compute the position weights
        position_weights = 1 - np.exp(-4 * (np.linspace(0, 1, len(sentences)) - 0.5) ** 2)
        min_value = np.min(position_weights)
        max_value = np.max(position_weights)

        # Normalize the weights so they are between 0 and 1
        position_weights = (position_weights - min_value) / (max_value - min_value)

        # Shift the weights up by 0.1 so there are no zeros
        position_weights += 0.8

        # Normalize again to ensure weights are still between 0 and 1
        min_value = np.min(position_weights)
        max_value = np.max(position_weights)
        position_weights = (position_weights - min_value) / (max_value - min_value)
        print("position_weights: ")
        print(position_weights)

        # Convert the scores dictionary to a numpy array
        scores_array = np.array([scores[i] for i in range(len(sentences))])
        print(scores_array)

        # Normalize the scores_array and position_weights
        scores_array = (scores_array - scores_array.min()) / (scores_array.max() - scores_array.min())
        position_weights = (position_weights - position_weights.min()) / (
                    position_weights.max() - position_weights.min())

        # Compute the final scores as the product of the normalized TextRank scores and the normalized position weights
        final_scores = (scores_array) * (position_weights)

        # Sort the rank and pick top sentences
        ranked_sentence = sorted(((final_scores[i], s) for i, s in enumerate(sentences)), reverse=True)

        # Pick top sentences based on user preference for ranking or original order
        if order_by_rank:
            summarize_text = [ranked_sentence[i][1] for i in range(top_n)]
        else:
            # Get the indices of the top_n sentences in their original order
            original_order_indices = sorted(
                [i for i in range(len(sentences)) if sentences[i] in [item[1] for item in ranked_sentence[:top_n]]])
            summarize_text = [sentences[i] for i in original_order_indices]

        # Output the summarize text
        return " ".join(summarize_text) + '.'

    def relevance_scores(self, sentences, top_n=3, order_by_rank=True):
        # Set standard weights
        position_weight = 0.1  # adjust to your needs
        length_weight = 0.2  # adjust to your needs
        term_weight = 0.7  # adjust to your needs

        # Calculate TextRank scores
        textrank_scores = self.relevance.calculate_textrank_scores(sentences)

        # Calculate other scores
        term_relevance_scores = self.relevance.calculate_term_relevance_scores(sentences)
        position_scores = self.relevance.calculate_position_scores(sentences)
        length_scores = self.relevance.calculate_length_scores(sentences)

        # Combine scores based on weights
        relevance_scores = {}

        for i, sentence in enumerate(sentences):
            relevance_scores[sentence] = (
                textrank_scores[i] +
                term_relevance_scores[sentence] * term_weight +
                position_scores[sentence] * position_weight +
                length_scores[sentence] * length_weight
            )

        # Sort the sentences by relevance scores
        sorted_relevance_scores = sorted(relevance_scores.items(), key=lambda item: item[1], reverse=True)

        # Select the top_n sentences
        if order_by_rank:
            summary = [sentence for sentence, _ in sorted_relevance_scores[:top_n]]
        else:
            # order_by_rank = False: Order summary by their occurrence in the original text
            summary = sorted([sentence for sentence, _ in sorted_relevance_scores[:top_n]], key=sentences.index)

        return summary

    def bertsum(self, sentences, top_n=3, order_by_rank=True):
        model = Summarizer()
        result = model(' '.join(sentences), num_sentences=top_n)
        return result
