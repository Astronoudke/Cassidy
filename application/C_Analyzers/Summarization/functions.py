import networkx as nx
import spacy
from nltk.corpus import stopwords as nltk_stopwords
import nltk
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

nlp = spacy.load('en_core_web_sm')
stopwords = nlp.Defaults.stop_words

class TextRank:
    def sentence_similarity(self, sent1, sent2, stopwords=None):
        if stopwords is None:
            stopwords = nlp.Defaults.stop_words

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

    def build_similarity_matrix(self, sentences: list, stopwords=None):
        # Create an empty similarity matrix
        similarity_matrix = np.zeros((len(sentences), len(sentences)))

        for idx1 in range(len(sentences)):
            for idx2 in range(len(sentences)):
                if idx1 == idx2:  # ignore if both are same sentences
                    continue
                similarity_matrix[idx1][idx2] = self.sentence_similarity(sentences[idx1], sentences[idx2],
                                                                    stopwords)

        return similarity_matrix


class RelevanceScores:
    def __init__(self):
        self.text_rank = TextRank()

    def calculate_textrank_scores(self, sentences, stopwords=None):
        sim_matrix = self.text_rank.build_similarity_matrix(sentences, stopwords)
        sentence_similarity_graph = nx.from_numpy_array(sim_matrix)
        scores = nx.pagerank(sentence_similarity_graph)

        return scores

    def calculate_term_relevance_scores(self, sentences):
        vectorizer = TfidfVectorizer()

        # Fit the vectorizer to the data
        vectorizer.fit(sentences)

        # Transform the sentences to vectors
        sentence_vectors = vectorizer.transform(sentences)

        # Use all unique words in the sentences as search terms
        search_terms = [word for word, index in sorted(vectorizer.vocabulary_.items(), key=lambda item: item[1])]


        term_relevance_scores = {}
        for sentence, vector in zip(sentences, sentence_vectors.toarray()):
            score = sum(vector[vectorizer.vocabulary_.get(word, 0)] for word in search_terms)
            term_relevance_scores[sentence] = score

        return term_relevance_scores

    def calculate_position_scores(self, sentences):
        total_sentences = len(sentences)
        position_scores = {sentence: (i+1)/total_sentences for i, sentence in enumerate(sentences)}
        return position_scores

    def calculate_length_scores(self, sentences):
        max_length = max(len(sentence.split()) for sentence in sentences)
        length_scores = {sentence: len(sentence.split())/max_length for sentence in sentences}
        return length_scores

    def calculate_message_relevance_scores(self, messages, stopwords=None):
        message_relevance_scores = {}

        for message in messages:
            sentences = nltk.sent_tokenize(message)
            sentence_scores = self.calculate_textrank_scores(sentences, stopwords)

            # Calculate the average relevance score for the message
            message_relevance_score = sum(sentence_scores.values()) / len(sentence_scores)
            message_relevance_scores[message] = message_relevance_score

        return message_relevance_scores

    def select_top_messages(self, messages_dict, num_messages, stopwords=None):
        message_scores = self.calculate_message_relevance_scores(messages_dict.values(), stopwords)

        # Create a dictionary to map each message to its number
        message_to_number = {v: k for k, v in messages_dict.items()}

        # Sort the messages by their scores in descending order
        sorted_messages = sorted(message_scores.items(), key=lambda item: item[1], reverse=True)

        # Select the top messages
        top_messages = [(message_to_number[message], message) for message, score in sorted_messages[:num_messages]]

        return top_messages
