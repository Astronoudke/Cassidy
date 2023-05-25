import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import pos_tag
import re
import contractions
import inflect

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
        print(discussion)

        for message_id, message_dict in discussion.items():
            new_data[message_id] = {}
            new_data[message_id]['author'] = message_dict['author']
            new_data[message_id]['text'] = self.preprocess_string(message_dict['text'])

        return new_data

    def concatenate_sections_grobid(self, preprocessed_output):
        sections_text = [text for key, text in preprocessed_output.items()]
        combined_text = ". ".join(sections_text)
        return combined_text

    def extract_main_body(self, text):
        # Define start and end markers
        start_markers = ["abstract", "Abstract", "ABSTRACT"]
        end_markers = ["acknowledgements", "Acknowledgements", "ACKNOWLEDGEMENTS", "references", "References",
                       "REFERENCES"]

        # Find the start of the main body
        start_idx = len(text)
        for marker in start_markers:
            idx = text.find(marker)
            if idx != -1 and idx < start_idx:
                start_idx = idx

        # Find the end of the main body
        end_idx = len(text)
        for marker in end_markers:
            idx = text.find(marker)
            if idx != -1 and idx < end_idx:
                end_idx = idx

        # Extract the main body
        if start_idx < end_idx:
            text = text[start_idx:end_idx]
        else:
            # If no valid start and end markers were found, return the original text
            text = text

        return text

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
        # Convert numbers to words
        p = inflect.engine()
        text = re.sub(r'\d+', lambda x: p.number_to_words(x.group()), text)
        # Expand contractions
        text = contractions.fix(text)
        return text

    def split_sentences(self, text):
        return sent_tokenize(text)

    def case_folding(self, text):
        return text.lower()

    def tokenize(self, text):
        return word_tokenize(text)

    def tokenize_sentences(self, sentences):
        return [word_tokenize(sentence) for sentence in sentences]

    def join_tokens(self, tokens):
        return " ".join(tokens)

    def pos_tagging(self, words):
        # If it's a list of words (strings)
        if isinstance(words[0], str):
            return pos_tag(words)
        # If it's a list of lists
        elif isinstance(words[0], list):
            return [pos_tag(word_list) for word_list in words]

    def filter_pos_tagged(self, pos_tagged_text, tags=['NN', 'NNS', 'NNP', 'NNPS']):
        # If it's a list of (word, tag) tuples
        if isinstance(pos_tagged_text[0], tuple):
            return [word for word, tag in pos_tagged_text if tag in tags]
        # If it's a list of lists
        elif isinstance(pos_tagged_text[0], list):
            return [[word for word, tag in word_list if tag in tags] for word_list in pos_tagged_text]

    def categorize_words(self, words):
        # implement your word categorization here
        categorized_words = words
        return categorized_words

    def remove_stop_words(self, words):
        stop_words = set(stopwords.words('english'))
        return [word for word in words if word not in stop_words]

    def lemmatize(self, words):
        return [lemmatizer.lemmatize(word) for word in words]

    def join_words(self, words):
        return " ".join(words)
