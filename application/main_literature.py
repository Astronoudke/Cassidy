from A_DataCollectors.ForumCollector.forum_collector import ForumCollector
from A_DataCollectors.ForumCollector.forum_application import ForumApplication
from A_DataCollectors.ScientificLiteratureCollector.scientific_literature_collector import ScientificLiteratureCollector
from B_Database.my_sql import DatabaseManager
from C_DataProcessors.text_preprocessor import \
    TextPreprocessor
from D_Analyzers.Summarization.extractive_summarizer import ExtractiveSummarizer

if __name__ == "__main__":
    def test_collecting():
        pdf_url = "C:\\Users\\noudy\\Downloads\\1-s2.0-S0749596X09001247-main.pdf"
        collector = ScientificLiteratureCollector(pdf_url)
        preprocessed_text = collector.collect('pdf', 'local', 'scipy')
        return preprocessed_text

    def create_table():
        db = DatabaseManager(user='root', password='', host='localhost', database_name='test_cassidy')
        db.connect()

        db.create_articles_table()

    def test_store_article():
        db = DatabaseManager(user='root', password='', host='localhost', database_name='test_cassidy')
        db.connect()

        category_id = db.add_category('Linguistics')
        article = test_collecting()
        article_id = db.add_article(article, category_id)
        print(article_id)

        db.close()

        return article_id

    def test_preprocessing(article_id):
        db = DatabaseManager(user='root', password='', host='localhost', database_name='test_cassidy')
        db.connect()

        article = db.select_article(article_id)
        summarization_steps = ['clean_data', 'split_sentences']
        summarization_preprocessor = TextPreprocessor(summarization_steps)

        text = article['text']
        return summarization_preprocessor.preprocess_grobid(text)


    create_table()
    storing = test_store_article()
    article_dct = test_preprocessing(storing)

    new_dict = {}
    for header, sentences in article_dct.items():
        es = ExtractiveSummarizer(sentences)
        summary = es.summarize('textrank', top_n=3, order_by_rank=False)

        new_dict[header] = summary

    print(new_dict)



