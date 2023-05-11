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

    def preprocess(self, text):
        for step in self.steps:
            text = getattr(self, step)(text)
        return text

    def clean_data(self, text):
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        # Remove usernames
        text = re.sub(r'\@\w+|\#', '', text)
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

    def pos_tagging(self, words):
        # Requires tokenization
        return pos_tag(words)

    def filter_pos_tagged(self, pos_tagged_text, tags=['NN', 'NNS', 'NNP', 'NNPS']):
        return [word for word, tag in pos_tagged_text if tag in tags]

    def categorize_words(self, words):
        # implement your word categorization here
        categorized_words = words
        return categorized_words

    def remove_stop_words(self, words):
        stop_words = set(stopwords.words('english'))
        return [word for word in words if word not in stop_words]

    def lemmatize(self, words):
        return [lemmatizer.lemmatize(word) for word in words]