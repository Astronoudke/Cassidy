from A_DataCollectors.ForumCollector.forum_collector import ForumCollector
from A_DataCollectors.ForumCollector.forum_application import ForumApplication
from A_DataCollectors.ScientificLiteratureCollector.scientific_literature_collector import ScientificLiteratureCollector
from C_DataProcessors.ScientificLiteratureDataProcessor.scientific_literature_data_processor import ScientificLiteratureDataProcessor

if __name__ == "__main__":
    def test_collecting():
        pdf_url = "https://arxiv.org/pdf/2305.07672.pdf"
        collector = ScientificLiteratureCollector(pdf_url)
        preprocessed_text = collector.collect()
        
        return preprocessed_text

    def test_preprocessing():
        summarization_steps = ['extract_main_body', 'clean_data', 'split_sentences']
        summarization_preprocessor = ScientificLiteratureDataProcessor(summarization_steps)

        text = test_collecting()
        return summarization_preprocessor.preprocess(text)
    
    print(test_preprocessing())
