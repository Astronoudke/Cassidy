import unittest
import datetime

from application.A_DataCollectors.ForumCollector.forum_collector import ForumCollector
from application.B_Database.my_sql import DatabaseManager
from application.tests.functions import print_colored_text


class TestForumCollector(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = DatabaseManager(user='root', password='', host='localhost', database_name='test_cassidy')
        cls.db.connect()
        cls.db.create_tables()
        cls.category_id = cls.db.add_category('Soccer')
        cls.forum_id = cls.db.add_forum('PSV 1: Selectie & Technische Staf',
                                        'https://forum.psv.nl/index.php?forums/psv-1-selectie-technische-staf.11/',
                                        'In dit onderdeel kunnen alle spelers en trainers van PSV 1 besproken worden.',
                                        cls.category_id)
        cls.forum = cls.db.select_forum(id=cls.forum_id)

    def setUp(self):
        self.psv_collector = ForumCollector(identification=self.forum["id"],
                                            name=self.forum["name"],
                                            base_url=self.forum["base_url"],
                                            description=self.forum["description"],
                                            category_id=self.forum["category_id"],
                                            page_param="page-",
                                            start_page=1,
                                            page_increment=1
                                            )

    @classmethod
    def tearDownClass(cls):
        cls.db.delete_forum(cls.forum_id)
        cls.db.delete_category(cls.category_id)
        cls.db.close()

    def test_01_store_discussions_of_forum_link(self):
        # TODO: Store the forum itself in the database
        """
        This test consists of the following steps:
        1. Scraping discussions from the forum using "ForumCollector.scrape_discussions_from_forum"
        2. For each discussion:
            2.1 Storing discussion info as a dict using "ForumCollector.return_discussion_info_from_scraped"
            2.2 Storing the discussion in the database using "DatabaseManager.add_discussion"
            2.3 Deleting the discussion from the database using "DatabaseManager.delete_discussion"
        """
        discussion_class = "structItem structItem--thread js-inlineModContainer js-threadListItem"
        full_discussion_class = False
        discussion_name_class = "structItem-title"
        discussion_creation_date_class = "structItem-startDate"
        discussion_views_class = "pairs pairs--justified structItem-minor"
        discussion_replies_class = "pairs pairs--justified"
        discussion_last_post_time_class = "structItem-latestDate u-dt"

        discussions = self.psv_collector.scrape_discussions_from_forum(discussion_class, full_discussion_class)
        print_colored_text("Discussions scraped: " + str(len(discussions)), "green")

        for discussion in discussions:
            discussion_info = self.psv_collector.return_discussion_info_from_scraped(discussion, discussion_name_class,
                                                                                     discussion_creation_date_class,
                                                                                     discussion_views_class,
                                                                                     discussion_replies_class,
                                                                                     discussion_last_post_time_class)
            discussion_id = self.db.add_discussion(
                discussion_info["name"],
                discussion_info["link"],
                discussion_info["creation date"],
                discussion_info["views"],
                discussion_info["replies"],
                discussion_info["last_post_time"],
                discussion_info["forum_id"]
            )

        self.db.clear_discussion_table()

        print_colored_text("Discussions stored and deleted: " + str(len(discussions)), "green")

    def test_02_messages_of_discussion_link(self):
        # TODO: Store the discussion itself in the database
        """
        This test consists of the following steps:
        1. Scraping messages from the discussion using "ForumCollector.scrape_messages_from_discussion"
        2. For each message:
            2.1 Storing message info as a dict using "ForumCollector.return_message_info_from_scraped"
            2.2 Storing the message in the database using "DatabaseManager.add_message"
            2.3 Deleting the message from the database using "DatabaseManager.delete_message"
        :return:
        """
        discussion_id = None
        try:
            discussion_link = "https://forum.psv.nl/index.php?threads/guus-til-m.1346/"
            discussion_creation_date = datetime.datetime.now().date()
            discussion_id = self.db.add_discussion("Guus Til (M)", discussion_link, discussion_creation_date,
                                                   0, 0, discussion_creation_date, self.forum_id)
            message_class = "message message--post js-post js-inlineModContainer"
            full_message_class = False
            message_text_class = "bbWrapper"
            message_date_class = "u-dt"
            message_author_class = "username"

            messages = self.psv_collector.scrape_messages_from_discussion(discussion_link=discussion_link,
                                                                          message_class=message_class,
                                                                          full_message_class=full_message_class,
                                                                          via_link=True)["messages"]
            print_colored_text("Messages scraped: " + str(len(messages)), "green")
            for message in messages:
                message_info = self.psv_collector.return_message_info_from_scraped(message, message_text_class,
                                                                                   message_date_class,
                                                                                   message_author_class, discussion_id)

                self.db.add_author(message_info["author"], self.psv_collector.identification)
                user_id = self.db.select_author_by_username_and_forum_id(message_info["author"],
                                                                         self.psv_collector.identification)["id"]

                self.db.add_message(
                    message_info["text"],
                    message_info["date"],
                    user_id,
                    message_info["discussion_id"]
                )

            print_colored_text("Messages stored and deleted: " + str(len(messages)), "green")

            self.db.clear_message_table()
            self.db.clear_author_table()

        finally:
            if discussion_id:
                self.db.delete_discussion(discussion_id)

    def test_03_discussions_of_forum_id(self):
        pass

    def test_04_messages_of_discussion_id(self):
        pass

    def test_05_messages_of_forum_id(self):
        pass


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestForumCollector('test_01_discussions_of_forum_link'))
    suite.addTest(TestForumCollector('test_02_messages_of_discussion_link'))
    suite.addTest(TestForumCollector('test_03_discussions_of_forum_id'))
    suite.addTest(TestForumCollector('test_04_messages_of_discussion_id'))
    suite.addTest(TestForumCollector('test_05_messages_of_forum_id'))
    # Add more test methods as needed
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
