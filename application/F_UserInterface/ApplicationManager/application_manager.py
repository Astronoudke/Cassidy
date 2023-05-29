import sys
sys.path.append('C:\\Users\\noudy\\PycharmProjects\\Cassidy\\application')

from A_DataCollectors.ScientificLiteratureCollector.scientific_literature_collector import ScientificLiteratureCollector
from A_DataCollectors.ForumCollector.forum_collector import ForumCollector
from A_DataCollectors.ForumCollector.forum_application import ForumApplication
from C_DataProcessors.text_preprocessor import TextPreprocessor
from D_Analyzers.Summarization.extractive_summarizer import ExtractiveSummarizer
from D_Analyzers.Relation_Extraction.relation_extractor import RelationExtractor
from D_Analyzers.Sentiment_Analysis.sentiment_analyzer import SentimentAnalyzer


class ScientificLiteratureAnalyzer:
    def __init__(self, path):
        self.path = path
        self.format = 'pdf'
        self.source_type = 'url' if path.startswith('http') else 'local'
        self.method = 'scipy'

    def analyze(self, functionality, preprocessing_steps=[]):
        analysis = getattr(self, functionality)(preprocessing_steps)
        return analysis

    def summarize(self, preprocessing_steps=[]):
        # Collect data
        collector = ScientificLiteratureCollector(self.path)
        text = collector.collect(self.format, self.source_type, self.method)

        # Preprocess data
        summarization_steps = preprocessing_steps
        preprocessor = TextPreprocessor(summarization_steps)
        preprocessed_text = preprocessor.preprocess_grobid(text)

        # Summarize data
        new_dict = {}
        for header, sentences in preprocessed_text.items():
            es = ExtractiveSummarizer(sentences)
            summary = es.summarize('textrank', top_n=3, order_by_rank=False)

            # filter out sentences less than four words long
            summary = '. '.join(sentence for sentence in summary.split('. ') if len(sentence.split()) >= 3)

            new_dict[header] = summary


        return new_dict

    def relation_extractor(self, preprocessing_steps=[]):
        # Collect data
        collector = ScientificLiteratureCollector(self.path)
        text = collector.collect(self.format, self.source_type, self.method)

        # Preprocess data
        relation_steps = ['clean_data']
        preprocessor = TextPreprocessor(relation_steps)
        preprocessed_text = preprocessor.preprocess_grobid(text)
        preprocessed_text = preprocessor.concatenate_sections_grobid(preprocessed_text)

        relation_extraction_steps = preprocessing_steps
        relation_preprocessor = TextPreprocessor(relation_extraction_steps)
        new_text = relation_preprocessor.preprocess_string(preprocessed_text)

        # Analyze the data
        relation_extractor = RelationExtractor(new_text)
        relations = relation_extractor.extract('co_occurrence')

        return relations

    def sentiment_analysis(self, preprocessing_steps=[]):
        # Collect data
        collector = ScientificLiteratureCollector(self.path)
        text = collector.collect(self.format, self.source_type, self.method)

        # Preprocess data
        sentiment_preprocessor = TextPreprocessor(preprocessing_steps)
        preprocessed_data = sentiment_preprocessor.preprocess_grobid(text)

        new_dict = {}
        for header, text in preprocessed_data.items():
            sa = SentimentAnalyzer(text)
            new_dict[header] = sa.analyze('textblob_analysis')

        return new_dict


class ForumAnalyzer:
    def __init__(self,discussion_link, message_class, full_message_class, pagination_class, message_text_class, message_author_class):
        self.discussion_link = discussion_link
        self.message_class = message_class
        self.full_message_class = full_message_class
        self.pagination_class = pagination_class
        self.message_text_class = message_text_class
        self.message_author_class = message_author_class
        self.collector = ForumCollector(name='name', base_url='base', description='desc', category='cat')
        self.app = ForumApplication(self.collector)
        self.collected_messages = self.app.collect_messages_by_discussion_link(
            discussion_link=self.discussion_link,
            message_class=self.message_class,
            full_message_class=self.full_message_class,
            pagination_class=self.pagination_class,
            message_text_class=self.message_text_class,
            message_author_class=self.message_author_class,
            store_in_dict=False,  # Here's the second change
            return_messages=True
        )

    def analyze(self, functionality, preprocessing_steps=[]):
        analysis = getattr(self, functionality)(preprocessing_steps)
        return analysis

    def summarize(self, preprocessing_steps=[]):
        # Preprocess data
        summarization_steps = preprocessing_steps
        preprocessor = TextPreprocessor(summarization_steps)
        preprocessed_text = preprocessor.preprocess_forum_discussion(self.collected_messages)

        # Summarize data
        new_dict = {}
        for header, messages in preprocessed_text.items():
            print("Messages: ")
            print(messages)
            es = ExtractiveSummarizer(messages)
            summary = es.summarize('relevance_scores', top_n=3, order_by_rank=False)

            print(summary)

            # filter out messages less than four words long
            summary = '. '.join(message for message in summary if len(message.split()) >= 3)

            new_dict[header] = summary

        return new_dict

    def relation_extractor(self, preprocessing_steps=[]):
        # Preprocess data
        relation_steps = ['clean_data']
        preprocessor = TextPreprocessor(relation_steps)
        preprocessed_text = preprocessor.preprocess_forum_discussion(self.collected_messages)
        preprocessed_text = preprocessor.concatenate_sections_grobid(preprocessed_text)

        relation_extraction_steps = preprocessing_steps
        relation_preprocessor = TextPreprocessor(relation_extraction_steps)
        new_text = relation_preprocessor.preprocess_string(preprocessed_text)

        # Analyze the data
        relation_extractor = RelationExtractor(new_text)
        relations = relation_extractor.extract('co_occurrence')

        return relations

    def sentiment_analysis(self, preprocessing_steps=[]):
        summarization_preprocessor = TextPreprocessor(preprocessing_steps)
        preprocessed_data = summarization_preprocessor.preprocess_forum_discussion(self.collected_messages)

        print("Preprocessed text: ")
        print(preprocessed_data)

        new_dict = {}
        for header, text in preprocessed_data.items():
            sa = SentimentAnalyzer(text)
            new_dict[header] = sa.analyze('textblob_analysis')

        return new_dict
