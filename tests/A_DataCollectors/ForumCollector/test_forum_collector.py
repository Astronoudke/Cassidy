import unittest
import datetime

from application.A_DataCollectors.ForumCollector.forum_collector import ForumCollector
from application.B_Database.my_sql import DatabaseManager
from tests.functions import print_colored_text


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

        cls.discussion_link = "https://forum.psv.nl/index.php?threads/guus-til-m.1346/"
        cls.discussion_creation_date = datetime.datetime.now().date()
        cls.discussion_id = cls.db.add_discussion("Guus Til (M)", cls.discussion_link, cls.discussion_creation_date,
                                               0, 0, cls.discussion_creation_date, cls.forum_id)

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
        cls.db.clear_message_table()
        cls.db.clear_author_table()
        cls.db.clear_discussion_table()
        cls.db.clear_forum_table()
        cls.db.clear_category_table()

        cls.db.close()

    def test_01_store_discussions_by_forum_link(self):
        # TODO: Store the forum itself in the database
        """
        This test consists of the following steps:
        1. Scraping discussions from the forum using "ForumCollector.scrape_discussions_from_forum"
        2. For each discussion:
            2.1 Storing discussion info as a dict using "ForumCollector.return_discussion_info_from_scraped"
            2.2 Storing the discussion in the database using "DatabaseManager.add_discussion"
        """
        print("\n" + "Test 01: Store discussions in DB by forum link" + "\n")
        discussion_class = "structItem structItem--thread js-inlineModContainer js-threadListItem"
        full_discussion_class = False
        discussion_name_class = "structItem-title"
        discussion_creation_date_class = "structItem-startDate"
        discussion_views_class = "pairs pairs--justified structItem-minor"
        discussion_replies_class = "pairs pairs--justified"
        discussion_last_post_time_class = "structItem-latestDate u-dt"

        discussions = self.psv_collector.scrape_discussions_from_forum(discussion_class, full_discussion_class)
        print_colored_text("- Discussions scraped: " + str(len(discussions)), "green")

        for discussion in discussions:
            discussion_info = self.psv_collector.return_discussion_info_from_scraped(discussion, discussion_name_class,
                                                                                     discussion_creation_date_class,
                                                                                     discussion_views_class,
                                                                                     discussion_replies_class,
                                                                                     discussion_last_post_time_class)
            self.db.add_discussion(
                discussion_info["name"],
                discussion_info["link"],
                discussion_info["creation date"],
                discussion_info["views"],
                discussion_info["replies"],
                discussion_info["last_post_time"],
                discussion_info["forum_id"]
            )

        print_colored_text("- Discussions stored in the database: " + str(len(discussions)), "green")

    def test_02_store_messages_by_discussion_link(self):
        # TODO: Store the discussion itself in the database
        """
        This test consists of the following steps:
        1. Scraping messages from the discussion using "ForumCollector.scrape_messages_from_discussion"
        2. For each message:
            2.1 Storing message info as a dict using "ForumCollector.return_message_info_from_scraped"
            2.2 Storing the author of the message in the database if it is not yet found.
            2.3 Storing the message in the database using "DatabaseManager.add_message"
        :return:
        """
        print("\n" + "Test 02: Store messages in DB by discussion link" + "\n")
        message_class = "message message--post js-post js-inlineModContainer"
        full_message_class = False
        message_text_class = "bbWrapper"
        message_date_class = "u-dt"
        message_author_class = "username"

        messages = self.psv_collector.scrape_messages_from_discussion(discussion_link=self.discussion_link,
                                                                      message_class=message_class,
                                                                      full_message_class=full_message_class,
                                                                      via_link=True)["messages"]
        print_colored_text("- Messages scraped: " + str(len(messages)), "green")
        for message in messages:
            message_info = self.psv_collector.return_message_info_from_scraped(message, message_text_class,
                                                                               message_date_class,
                                                                               message_author_class,
                                                                               discussion_id=self.discussion_id)

            author = self.db.select_author_by_username_and_forum_id(message_info["author"],
                                                                    self.psv_collector.identification)

            if author is None:
                self.db.add_author(message_info["author"], self.psv_collector.identification)
                author_id = self.db.select_author_by_username_and_forum_id(message_info["author"],
                                                                           self.psv_collector.identification)[
                    "id"]
            else:
                author_id = author["id"]

            self.db.add_message(
                message_info["text"],
                message_info["date"],
                author_id,
                message_info["discussion_id"]
            )

        print_colored_text("- Messages stored in the database: " + str(len(messages)), "green")

    def test_03_collect_discussions_by_forum_id(self):
        """
        This test consists of the following steps:
        1. Collecting the discussions of the forum using "DatabaseManager.select_discussions_by_forum_id"
        :return:
        """
        print("\n" + "Test 03: Collect discussions by forum ID")
        discussions = self.db.select_discussions_by_forum_id(self.psv_collector.identification)

        if discussions:
            print_colored_text("- Discussions collected: " + str(len(discussions)), "green")
        else:
            print_colored_text("- No discussions found for forum ID: " + str(self.psv_collector.identification), "yellow")

    def test_04_collect_messages_by_discussion_id(self):
        """
        This test consists of the following steps:
        1. Collecting the messages of the discussion using "DatabaseManager.select_messages_by_discussion_id"
        :return:
        """
        print("\n" + "Test 04: Collect messages by discussion ID")
        messages = self.db.select_messages_by_discussion_id(self.discussion_id)

        if messages:
            print_colored_text("- Messages collected: " + str(len(messages)), "green")
        else:
            print_colored_text("- No messages found for discussion ID: " + str(self.discussion_id), "yellow")

    def test_05_collect_messages_by_forum_id(self):
        """
        This test consists of the following steps:
        1. Collecting the messages of the forum using "DatabaseManager.select_messages_by_forum_id"
        :return:
        """
        print("\n" + "Test 05: Collect messages by forum ID")
        messages = self.db.select_messages_by_forum_id(self.psv_collector.identification)

        if messages:
            print_colored_text("- Messages collected: " + str(len(messages)), "green")
        else:
            print_colored_text("- No messages found for forum ID: " + str(self.psv_collector.identification), "yellow")


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestForumCollector('test_01_store_discussions_by_forum_link'))
    suite.addTest(TestForumCollector('test_02_store_messages_by_discussion_link'))
    suite.addTest(TestForumCollector('test_03_store_discussions_by_forum_id'))
    suite.addTest(TestForumCollector('test_04_store_messages_by_discussion_id'))
    suite.addTest(TestForumCollector('test_05_store_messages_by_forum_id'))

    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
