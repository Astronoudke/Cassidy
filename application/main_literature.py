from A_DataCollectors.ForumCollector.forum_collector import ForumCollector
from A_DataCollectors.ForumCollector.forum_application import ForumApplication
from A_DataCollectors.ScientificLiteratureCollector.scientific_literature_collector import ScientificLiteratureCollector
from B_Database.my_sql import DatabaseManager
from C_DataProcessors.text_preprocessor import TextPreprocessor
from D_Analyzers.Summarization.extractive_summarizer import ExtractiveSummarizer

if __name__ == "__main__":
    def test_collecting():
        pdf_url = "C:/Users/noudy/Downloads/s10791-016-9286-2.pdf"
        collector = ScientificLiteratureCollector(pdf_url)
        preprocessed_text = collector.collect('pdf', 'local', 'scipy')
        return preprocessed_text

    def test_preprocessing(article):
        summarization_steps = ['clean_data', 'split_sentences']
        summarization_preprocessor = TextPreprocessor(summarization_steps)

        return summarization_preprocessor.preprocess_grobid(article)

    # Here the issue does not appear yet

    print(test_preprocessing(test_collecting()))





