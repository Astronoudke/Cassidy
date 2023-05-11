from A_DataCollectors.ForumCollector.forum_collector import ForumCollector
from A_DataCollectors.ForumCollector.forum_application import ForumApplication
from B_Database.my_sql import DatabaseManager
from C_DataProcessors.text_preprocessor import TextPreprocessor
from D_Analyzers.Summarization.extractive_summarizer import ExtractiveSummarizer
from E_Evaluate.Summarization.summarization_evaluator import ROUGE

if __name__ == "__main__":
    def test_collecting():
        db = DatabaseManager(user='root', password='', host='localhost', database_name='test_cassidy')
        db.connect()

        db.create_tables()

        # Creating a category
        category_id = db.add_category('Space')

        forum_id = db.add_forum('Telescopes, Star Charts, & Planetariums',
                                'https://forums.space.com/forums/telescopes-star-charts-planetariums.64/',
                                '', category_id)
        forum = db.select_forum(id=forum_id)
        db.close()

        space_collector = ForumCollector(identification=forum["id"],
                                       name=forum["name"],
                                       base_url=forum["base_url"],
                                       description=forum["description"],
                                       category_id=forum["category_id"]
                                       )

        app = ForumApplication(space_collector, db)

        ds = app.collect_discussions_by_forum_link(
            discussion_class="structItem structItem--thread js-trendingThreadItem",
            full_discussion_class=False, pagination_class="pageNav-main",
            discussion_name_class="structItem-title", discussion_creation_date_class="u-dt",
            discussion_views_class="",
            discussion_replies_class="pairs pairs--justified",
            discussion_last_post_time_class="structItem-latestDate u-dt",
            store_in_db=True,
            return_discussions=True)

        print(ds)

        ds_messages = app.collect_messages_by_discussion_link(
            discussion_link="https://forums.space.com/threads/constellations-space-travel.29641/",
            message_class="message-content js-messageContent",
            full_message_class=False,
            pagination_class="pageNav-main",
            message_text_class="bbWrapper",
            message_date_class="u-dt",
            message_author_class="username",
            store_in_db=True,
            return_messages=True)

        print(ds_messages)

    def test_preprocessing():
        summarization_steps = ['clean_data', 'split_sentences']
        relation_extraction_steps = ['clean_data', 'case_folding', 'split_sentences', 'tokenize_sentences']
        sentiment_analysis_steps = ['clean_data', 'case_folding', 'tokenize', 'remove_stop_words', 'lemmatize']
        word_frequency_steps = ['clean_data', 'case_folding', 'tokenize','pos_tagging', 'filter_pos_tagged', 'lemmatize']

        summarization_preprocessor = TextPreprocessor(summarization_steps)
        relation_extraction_preprocessor = TextPreprocessor(relation_extraction_steps)
        sentiment_analysis_preprocessor = TextPreprocessor(sentiment_analysis_steps)

        text = "Hey, I just found the following. Hope it helps: Richard Adkins, Amateur astronomer for over half a century. " \
               "Answered Aug 21, 2015 https://www.quora.com/How-far-would-you-have-to-go-for-the-constellations-to-appear" \
               "-different# The apparent location of stars within the field of view of an observer traveling through " \
               "interstellar space would change with distance as the traveler got further and further from earth. The " \
               "constellations, as we have defined them are, are made up of objects in vastly different positions in three " \
               "dimensional space. Some are comparably close to us and others are extremely far away within a single " \
               "constellation. The shape of a constellation would change depending on which one you were looking at. Alpha " \
               "Centauri is the closest star to us (it is actually a binary star) and is part of the constellation Centaurus. " \
               "Traveling anything close to 4 light years tangentially to that constellation would alter the appearance of " \
               "centaurus very quickly. There is a free program that will allow you to look at the stars from 'any' position " \
               "in space and, therefore, see exactly how constellations change for yourself. See: Celestia: Home"

        return relation_extraction_preprocessor.preprocess(text)

    def test_analyzing():
        extractive_summarizer = ExtractiveSummarizer(test_preprocessing())

        print(extractive_summarizer.summarize('textrank'))

    def test_evaluating():
        rouge = ROUGE('textrank')

        print(rouge.state_bills())


    print(test_preprocessing())
