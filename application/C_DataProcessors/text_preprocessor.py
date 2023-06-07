import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import pos_tag

import spacy
import re
import contractions
import inflect
import inflect
import en_core_web_sm

# Load the spaCy model
nlp = en_core_web_sm.load()

# If you have not downloaded these nltk packages, you will need to do so.
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('stopwords')

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()


class TextPreprocessor:
    def __init__(self, steps):
        self.steps = steps
        nltk.download('punkt')

    def preprocess_string(self, text):
        for step in self.steps:
            text = getattr(self, step)(text)
        return text

    def preprocess_grobid(self, output):
        new_data = {"title": output['title']}

        heading_counts = {}

        for section in output['sections']:
            heading = section['heading']
            # If the heading already exists, create a new unique key
            if heading in heading_counts:
                heading_counts[heading] += 1
                heading += f"_{heading_counts[heading]}"
            else:
                heading_counts[heading] = 0

            new_data[heading] = section['text']

        new_data['title'] = self.preprocess_string(new_data['title'])
        for key in new_data:
            if key != 'title':
                new_data[key] = self.preprocess_string(new_data[key])
        return new_data

    def preprocess_forum_discussion(self, discussion):
        new_data = {}

        for message_id, message_dict in discussion.items():
            new_data[message_id] = self.preprocess_string(message_dict['text'])
            #new_data[message_id]['author'] = message_dict['author']
            #new_data[message_id]['text'] = self.preprocess_string(message_dict['text'])

        return new_data

    def concatenate_sections_grobid(self, preprocessed_output):
        sections_text = [text for key, text in preprocessed_output.items()]
        combined_text = ". ".join(sections_text)
        return combined_text

    def clean_data(self, text):
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        # Remove usernames
        text = re.sub(r'\@\w+|\#', '', text)
        # Remove newlines
        text = re.sub(r'\n', '', text)
        # Remove extra whitespace
        text = text.strip()
        text = " ".join(text.split())
        # Expand contractions
        text = contractions.fix(text)

        return text

    def split_sentences(self, text):
        doc = nlp(text)
        return [sent.text for sent in doc.sents]

    def case_folding(self, text):
        return text.lower()

    def tokenize(self, text):
        if isinstance(text, list):
            return [[token.text for token in nlp(sentence)] for sentence in text]
        else:
            return [token.text for token in nlp(text)]

    def join_tokens(self, tokens):
        return " ".join(tokens)

    def pos_tagging(self, words):
        # If the list is not empty
        if words:
            # If it's a list of words (strings)
            if isinstance(words[0], str):
                return [(token.text, token.tag_) for token in nlp(words)]
            # If it's a list of lists
            elif isinstance(words[0], list):
                return [[(token.text, token.tag_) for token in nlp(" ".join(word_list))] for word_list in words]
        # If the list is empty, return an empty list
        else:
            return []

    def filter_pos_tagged(self, pos_tagged_text, tags=['NN', 'NNS', 'NNP', 'NNPS']):
        # If pos_tagged_text is not empty
        if pos_tagged_text:
            # If it's a list of (word, tag) tuples
            if isinstance(pos_tagged_text[0], tuple):
                return [word for word, tag in pos_tagged_text if tag in tags]
            # If it's a list of lists
            elif isinstance(pos_tagged_text[0], list):
                return [[word for word, tag in word_list if tag in tags] for word_list in pos_tagged_text]
        # If pos_tagged_text is empty, return an empty list
        else:
            return []

    def categorize_words(self, words):
        # implement word categorization here
        categorized_words = words
        return categorized_words

    def remove_stop_words(self, words):
        return [word for word in words if not nlp.vocab[word].is_stop]

    def lemmatize(self, words):
        print("words")
        print(words)
        if len(words) == 0:
            return []
        if isinstance(words, list):
            if isinstance(words[0], list):
                return [[token.lemma_ for token in nlp(" ".join(word_list))] for word_list in words]
            else:
                return [token.lemma_ for token in nlp(" ".join(words))]
        else:
            return [token.lemma_ for token in nlp(words)]

