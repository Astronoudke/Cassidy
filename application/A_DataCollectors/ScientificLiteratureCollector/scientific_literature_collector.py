import io
import requests
import nltk
import pdfplumber
import scipdf
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Download the NLTK English tokenizer and the stopwords of all languages
nltk.download('punkt')
nltk.download('stopwords')


class ScientificLiteratureCollector:
    def __init__(self, pdf_url: str):
        self.pdf_url = pdf_url


    def read_pdf_from_url_scipy(self):
        article_dict = scipdf.parse_pdf_to_dict(self.pdf_url, as_list=False)
        return article_dict

    def read_pdf_from_url(self):
        response = requests.get(self.pdf_url)
        file = io.BytesIO(response.content)

        text_content = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text_content += page.extract_text()

        return text_content

    def collect(self):
        raw_text = self.read_pdf_from_url_scipy()
        return raw_text

# https://arxiv.org/pdf/2305.07672.pdf