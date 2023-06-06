import io
import requests
import nltk
import scipdf
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Download the NLTK English tokenizer and the stopwords of all languages
nltk.download('punkt')
nltk.download('stopwords')


class ScientificLiteratureCollector:
    def __init__(self, path: str):
        self.path = path

    def collect(self, format, source_type, method):
        method_name = f"read_{format}_from_{source_type}_using_{method}"
        summarization = getattr(self, method_name)(self.path)
        return summarization

    def read_pdf_from_url_using_scipy(self, path):
        article_dict = scipdf.parse_pdf_to_dict(path, as_list=False)
        return article_dict

    def read_pdf_from_local_using_scipy(self, path):
        article_dict = scipdf.parse_pdf_to_dict(path, as_list=False)
        return article_dict
