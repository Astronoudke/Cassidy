from A_DataCollectors.ForumCollector.forum_collector import ForumCollector
from A_DataCollectors.ForumCollector.forum_application import ForumApplication
from A_DataCollectors.ScientificLiteratureCollector.scientific_literature_collector import ScientificLiteratureCollector
from C_DataProcessors.text_preprocessor import \
    TextPreprocessor

if __name__ == "__main__":
    def test_collecting():
        pdf_url = "C:\\Users\\noudy\\Downloads\\1-s2.0-S0749596X09001247-main.pdf"
        collector = ScientificLiteratureCollector(pdf_url)
        preprocessed_text = collector.collect('pdf', 'local', 'scipy')
        return preprocessed_text


    def test_preprocessing():
        summarization_steps = ['clean_data', 'split_sentences']
        summarization_preprocessor = TextPreprocessor(summarization_steps)

        text = test_collecting()
        return summarization_preprocessor.preprocess(text)



    print(test_collecting())