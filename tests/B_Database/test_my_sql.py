import unittest
import datetime

from application.B_Database.my_sql import DatabaseManager
from tests.functions import print_colored_text


class TestDatabaseManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_manager = DatabaseManager(user='root', password='', host='localhost', database_name='test_cassidy')
        cls.db_manager.connect()
        cls.db_manager.create_tables()

    @classmethod
    def tearDownClass(cls):
        cls.db_manager.close()

    def test_01_categories(self):
        """
        This test consists of the following steps:
        1. Add a category
        2. Edit the category
        3. Select the category
        4. Delete the category
        """
        category_id = None
        try:
            # Add a category
            print('Test: Categories')
            category_name = 'TestCategory'
            category_id = self.db_manager.add_category(category_name)
            print_colored_text('- Category added: ' + category_name, 'green')

            # Edit the category
            category_name = 'UpdatedTestCategory'
            self.db_manager.edit_category(category_id, category_name)
            print_colored_text('- Category edited: ' + category_name, 'green')

            # Select the category
            category = self.db_manager.select_category(category_id)
            self.assertEqual(category['name'], category_name)
            print_colored_text('- Category selected: ' + category_name, 'green')

        finally:
            # Delete the category
            if category_id:
                self.db_manager.delete_category(category_id)
                print_colored_text('- Category deleted: ' + category_name, 'green')

        print('\n')

    def test_02_forums(self):
        """
        This test consists of the following steps:
        1. Add a forum
        2. Edit the forum
        3. Select the forum
        4. Delete the forum
        """
        category_id = None
        forum_id = None
        try:
            # Add a forum
            print('Test: Forums')
            category_name = 'TestCategory'
            category_id = self.db_manager.add_category(category_name)
            forum_name = 'TestForum'
            forum_url = 'https://example.com'
            forum_description = 'Test description'
            forum_id = self.db_manager.add_forum(forum_name, forum_url, forum_description, category_id)
            print_colored_text('- Forum added: ' + forum_name, 'green')

            # Edit the forum
            updated_forum_name = 'UpdatedTestForum'
            self.db_manager.edit_forum(forum_id, updated_forum_name, forum_url)
            print_colored_text('- Forum edited: ' + updated_forum_name, 'green')

            # Select the forum
            forum = self.db_manager.select_forum(forum_id)
            self.assertEqual(forum['name'], updated_forum_name)
            self.assertEqual(forum['base_url'], forum_url)
            self.assertEqual(forum['description'], forum_description)
            self.assertEqual(forum['category_id'], category_id)
            print_colored_text('- Forum selected: ' + updated_forum_name, 'green')

        finally:
            # Delete the forum
            if forum_id:
                self.db_manager.delete_forum(forum_id)
                print_colored_text('- Forum deleted: ' + updated_forum_name, 'green')

            if category_id:
                self.db_manager.delete_category(category_id)

        print('\n')

    def test_03_discussions(self):
        """
        This test consists of the following steps:
        1. Add a discussion
        2. Edit the discussion
        3. Select the discussion
        4. Delete the discussion
        """
        category_id = None
        forum_id = None
        discussion_id = None
        try:
            # Add a discussion
            print('Test: Discussions')
            category_name = 'TestCategory'
            category_id = self.db_manager.add_category(category_name)
            forum_name = 'TestForum'
            forum_url = 'https://example.com'
            forum_description = 'Test description'
            forum_id = self.db_manager.add_forum(forum_name, forum_url, forum_description, category_id)
            discussion_name = 'TestDiscussion'
            discussion_url = 'https://example.com'
            discussion_views = 0
            discussion_replies = 0
            discussion_creation_date = datetime.datetime.now().date()
            discussion_id = self.db_manager.add_discussion(discussion_name, discussion_url, discussion_creation_date,
                                                           discussion_views, discussion_replies,
                                                           discussion_creation_date, forum_id)
            print_colored_text('- Discussion added: ' + discussion_name, 'green')

            # Edit the discussion
            updated_discussion_name = 'UpdatedTestDiscussion'
            self.db_manager.edit_discussion(discussion_id, updated_discussion_name, discussion_url,
                                            discussion_creation_date, discussion_views, discussion_replies,
                                            discussion_creation_date)
            print_colored_text('- Discussion edited: ' + updated_discussion_name, 'green')

            # Select the discussion
            discussion = self.db_manager.select_discussion(via_id=True, id=discussion_id)
            self.assertEqual(discussion['name'], updated_discussion_name)
            self.assertEqual(discussion['link'], discussion_url)
            self.assertEqual(discussion['creation_date'], discussion_creation_date)
            self.assertEqual(discussion['views'], discussion_views)
            self.assertEqual(discussion['replies'], discussion_replies)
            self.assertEqual(discussion['last_post_time'].date(), discussion_creation_date)
            self.assertEqual(discussion['forum_id'], forum_id)
            print_colored_text('- Discussion selected: ' + updated_discussion_name, 'green')

        finally:
            # Delete the discussion
            if discussion_id:
                self.db_manager.delete_discussion(discussion_id)
                print_colored_text('- Discussion deleted: ' + updated_discussion_name, 'green')

            if forum_id:
                self.db_manager.delete_forum(forum_id)

            if category_id:
                self.db_manager.delete_category(category_id)

        print('\n')

    def test_04_messages(self):
        """
        This test consists of the following steps:
        1. Add a message
        2. Edit the message
        3. Select the message
        4. Delete the message
        """
        category_id = None
        forum_id = None
        discussion_id = None
        message_id = None
        try:
            # Add a message
            print('Test: Messages')
            category_name = 'TestCategory'
            category_id = self.db_manager.add_category(category_name)
            forum_name = 'TestForum'
            forum_url = 'https://example.com'
            forum_description = 'Test description'
            forum_id = self.db_manager.add_forum(forum_name, forum_url, forum_description, category_id)
            author_name = 'TestAuthor'
            author_id = self.db_manager.add_author(author_name, forum_id)
            discussion_name = 'TestDiscussion'
            discussion_url = 'https://example.com'
            discussion_creation_date = datetime.datetime.now().date()
            discussion_id = self.db_manager.add_discussion(discussion_name, discussion_url, discussion_creation_date,
                                                           0, 0, discussion_creation_date, forum_id)
            message_text = 'Test message'
            message_date = datetime.datetime.now()
            message_id = self.db_manager.add_message(message_text, message_date, author_id, discussion_id)
            print_colored_text('- Message added: ' + message_text, 'green')

            # Edit the message
            updated_message_text = 'UpdatedTestMessage'
            self.db_manager.edit_message(message_id, updated_message_text)
            print_colored_text('- Message edited: ' + updated_message_text, 'green')

            # Select the message
            message = self.db_manager.select_message(message_id)
            self.assertEqual(message['text'], updated_message_text)
            self.assertEqual(message['author_id'], author_id)
            self.assertEqual(message['discussion_id'], discussion_id)
            print_colored_text('- Message selected: ' + updated_message_text, 'green')

        finally:
            # Delete the message
            if message_id:
                self.db_manager.delete_message(message_id)
                print_colored_text('- Message deleted: ' + updated_message_text, 'green')

            if author_id:
                self.db_manager.delete_author(author_id)

            if discussion_id:
                self.db_manager.delete_discussion(discussion_id)

            if forum_id:
                self.db_manager.delete_forum(forum_id)

            if category_id:
                self.db_manager.delete_category(category_id)

        print('\n')


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestDatabaseManager('test_01_categories'))
    suite.addTest(TestDatabaseManager('test_02_forums'))
    suite.addTest(TestDatabaseManager('test_03_discussions'))
    suite.addTest(TestDatabaseManager('test_04_messages'))
    # Add more test methods as needed
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
