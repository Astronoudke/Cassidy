from A_DataCollectors.ForumCollector.forum_collector import ForumCollector
from A_DataCollectors.ForumCollector.forum_application import ForumApplication
from A_DataCollectors.ScientificLiteratureCollector.scientific_literature_collector import ScientificLiteratureCollector
from B_Database.my_sql import DatabaseManager
from C_DataProcessors.text_preprocessor import TextPreprocessor
from D_Analyzers.Summarization.extractive_summarizer import ExtractiveSummarizer
from D_Analyzers.Relation_Extraction.relation_extractor import RelationExtractor

if __name__ == "__main__":
    def test_collecting():
        pdf_url = "C:/Users/noudy/Downloads/s10791-016-9286-2.pdf"
        collector = ScientificLiteratureCollector(pdf_url)
        preprocessed_text = collector.collect('pdf', 'local', 'scipy')
        return preprocessed_text

    def test_preprocessing(article):
        summarization_steps = ['clean_data', 'case_folding', 'split_sentences', 'tokenize', 'pos_tagging', 'filter_pos_tagged']
        summarization_preprocessor = TextPreprocessor(summarization_steps)

        return summarization_preprocessor.preprocess_grobid(article)

    def test_analysis(preprocessed_article):
        relation_extractor = RelationExtractor(preprocessed_article)
        relations = relation_extractor.extract('co_occurrence')

        return relations

    # Here the issue does not appear yet

    raw_text = test_collecting()
    print(raw_text)
    preprocessed_text = test_preprocessing(raw_text)
    print(preprocessed_text)
    relations = test_analysis(preprocessed_text)
    print(relations)
