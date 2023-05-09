import abc

from .forum_collector import ForumCollector
from B_Database.my_sql import DatabaseManager


class ForumApplication(abc.ABC):
    def __init__(self, forum_collector: ForumCollector, database_manager: DatabaseManager):
        self.forum_collector = forum_collector
        self.db = database_manager

    def collect_discussions_by_forum_link(self, discussion_class: str, full_discussion_class: bool, pagination_class: str,
                                          discussion_name_class: str, discussion_creation_date_class: str,
                                          discussion_views_class: str, discussion_replies_class: str,
                                          discussion_last_post_time_class: str,
                                          store_in_db: bool = False, return_discussions: bool = False):
        # TODO: Make this function not reliant on having the user put in data about the forum.
        discussions = self.forum_collector.scrape_discussions_from_forum(discussion_class, full_discussion_class,
                                                                         pagination_class)

        self.db.connect()

        if store_in_db:
            discussion_num = 1
            discussions_dict = {}
            for discussion in discussions:
                discussion_info = self.forum_collector.return_discussion_info_from_scraped(discussion,
                                                                                           discussion_name_class,
                                                                                           discussion_creation_date_class,
                                                                                           discussion_views_class,
                                                                                           discussion_replies_class,
                                                                                           discussion_last_post_time_class)

                discussion_id = self.db.select_discussion(via_link=True, link=discussion_info["link"])

                if discussion_id is None:
                    self.db.add_discussion(
                        discussion_info["name"],
                        discussion_info["link"],
                        discussion_info["creation date"],
                        discussion_info["views"],
                        discussion_info["replies"],
                        discussion_info["last_post_time"],
                        self.forum_collector.identification
                    )
                else:
                    print("Discussion " + discussion_info["name"] + " already in database. Changing values...")
                    self.db.edit_discussion(
                        discussion_id,
                        discussion_info["name"],
                        discussion_info["link"],
                        discussion_info["creation date"],
                        discussion_info["views"],
                        discussion_info["replies"],
                        discussion_info["last_post_time"],
                        self.forum_collector.identification
                    )

                discussions_dict[discussion_num] = discussion_info
                discussion_num += 1

            if return_discussions:
                return discussions_dict

        else:
            discussion_num = 1
            discussions_dict = {}
            for discussion in discussions:
                discussion_info = self.forum_collector.return_discussion_info_from_scraped(discussion,
                                                                                           discussion_name_class,
                                                                                           discussion_creation_date_class,
                                                                                           discussion_views_class,
                                                                                           discussion_replies_class,
                                                                                           discussion_last_post_time_class)
                discussions_dict[discussion_num] = discussion_info
                discussion_num += 1

            if return_discussions:
                return discussions_dict

        self.db.close()

    def collect_messages_by_discussion_link(self, discussion_link: str, message_class: str,
                                            full_message_class: bool, pagination_class: str,
                                            message_text_class: str, message_date_class: str, message_author_class: str,
                                            discussion_name: str = None, discussion_creation_date: str = None,
                                            discussion_last_post_time: str = None, forum_id: int = None,
                                            store_in_db: bool = False, return_messages: bool = False):
        # TODO: Make this function not reliant on having the user put in data about the discussion.

        if store_in_db:
            self.db.connect()
            discussion_id = self.db.get_discussion_id_by_link(discussion_link)

            if discussion_id is None:
                discussion_id = self.db.add_discussion(discussion_name, discussion_link, discussion_creation_date,
                                                       0, 0, discussion_last_post_time, forum_id)

            messages = self.forum_collector.scrape_messages_from_discussion(discussion_link=discussion_link,
                                                                            message_class=message_class,
                                                                            full_message_class=full_message_class,
                                                                            pagination_class=pagination_class,
                                                                            via_link=True)["messages"]

            message_num = 1
            messages_dict = {}
            for message in messages:
                message_info = self.forum_collector.return_message_info_from_scraped(message, message_text_class,
                                                                                     message_date_class,
                                                                                     message_author_class,
                                                                                     discussion_id=discussion_id)

                author = self.db.select_author_by_username_and_forum_id(message_info["author"],
                                                                        self.forum_collector.identification)

                if author is None:
                    self.db.add_author(message_info["author"], self.forum_collector.identification)
                    author_id = self.db.select_author_by_username_and_forum_id(message_info["author"],
                                                                               self.forum_collector.identification)[
                        "id"]
                else:
                    author_id = author["id"]

                message_id = self.db.select_message_by_discussion_date_author_and_text(message_info["discussion_id"],
                                                                                       message_info["date"],
                                                                                       author_id,
                                                                                       message_info["text"])

                if message_id is None:
                    self.db.add_message(
                        message_info["text"],
                        message_info["date"],
                        author_id,
                        message_info["discussion_id"]
                    )
                else:
                    print("Message already found.")

                messages_dict[message_num] = message_info
                message_num += 1

            if return_messages:
                return messages_dict

        else:
            messages = self.forum_collector.scrape_messages_from_discussion(discussion_link=discussion_link,
                                                                            message_class=message_class,
                                                                            full_message_class=full_message_class,
                                                                            pagination_class=pagination_class,
                                                                            via_link=True)["messages"]

            message_num = 1
            messages_dict = {}
            for message in messages:
                message_info = self.forum_collector.return_message_info_from_scraped(message, message_text_class,
                                                                                     message_date_class,
                                                                                     message_author_class,
                                                                                     only_discussion_link=True,
                                                                                     discussion_link=discussion_link)
                messages_dict[message_num] = message_info
                message_num += 1

            if return_messages:
                return messages_dict

        self.db.close()
