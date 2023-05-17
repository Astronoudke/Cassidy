import io
import requests
import nltk
import pdfplumber
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Download the NLTK English tokenizer and the stopwords of all languages
nltk.download('punkt')
nltk.download('stopwords')


class ScientificLiteratureCollector:
    def __init__(self, pdf_url: str):
        self.pdf_url = pdf_url

    def read_pdf_from_url(self):
        response = requests.get(self.pdf_url)
        file = io.BytesIO(response.content)

        text_content = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text_content += page.extract_text()

        return text_content

    def preprocess_text(self, text_content: str):
        # 1. Tokenize the sentences
        sentences = sent_tokenize(text_content)

        # 2. Tokenize words in each sentence
        tokenized_sentences = [word_tokenize(sentence) for sentence in sentences]

        # 3. Lowercase all words
        tokenized_sentences = [[word.lower() for word in sentence] for sentence in tokenized_sentences]

        # 4. Remove punctuation and numbers
        tokenized_sentences = [[word for word in sentence if word.isalpha()] for sentence in tokenized_sentences]

        # 5. Remove stopwords
        tokenized_sentences = [[word for word in sentence if word not in stopwords.words()] for sentence in tokenized_sentences]

        return tokenized_sentences

    def collect(self):
        raw_text = self.read_pdf_from_url()
        preprocessed_text = self.preprocess_text(raw_text)
        return raw_text

# https://arxiv.org/pdf/2305.07672.pdf