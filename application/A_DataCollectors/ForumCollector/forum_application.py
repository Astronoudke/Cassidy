import abc

from .forum_collector import ForumCollector
from .functions import convert_date_for_db


class ForumApplication(abc.ABC):
    def __init__(self, forum_collector: ForumCollector):
        self.forum_collector = forum_collector
        self.discussions_dict = {}

    def collect_discussions_by_forum_link(self, discussion_class: str, full_discussion_class: bool,
                                          pagination_class: str,
                                          discussion_name_class: str, store_in_dict: bool = False,
                                          return_discussions: bool = False):
        # TODO: Make this function not reliant on having the user put in data about the forum.
        discussions = self.forum_collector.scrape_discussions_from_forum(discussion_class, full_discussion_class,
                                                                         pagination_class)

        if store_in_dict:
            for discussion in discussions:
                discussion_info = self.forum_collector.return_discussion_info_from_scraped(discussion,
                                                                                           discussion_name_class)
                self.discussions_dict[discussion_info["link"]] = self.forum_collector.store_discussion_in_dict(
                    discussion_info)

            if return_discussions:
                return self.discussions_dict

        else:
            discussion_num = 1
            discussions_dict = {}
            for discussion in discussions:
                discussion_info = self.forum_collector.return_discussion_info_from_scraped(discussion,
                                                                                           discussion_name_class)
                discussions_dict[discussion_num] = discussion_info
                discussion_num += 1

            if return_discussions:
                return discussions_dict

    def collect_messages_by_discussion_link(self, discussion_link: str, message_class: str,
                                            full_message_class: bool, pagination_class: str,
                                            message_text_class: str, message_author_class: str,
                                            discussion_name: str = None, forum_id: int = None,
                                            store_in_dict: bool = False, return_messages: bool = False):

        if store_in_dict:

            messages = self.forum_collector.scrape_messages_from_discussion(discussion_link=discussion_link,
                                                                            message_class=message_class,
                                                                            full_message_class=full_message_class,
                                                                            pagination_class=pagination_class,
                                                                            via_link=True)["messages"]
            message_num = 1
            for message in messages:
                message_info = self.forum_collector.return_message_info_from_scraped(message, message_text_class,
                                                                                     message_author_class,
                                                                                     discussion_id=discussion_link)
                self.discussions_dict[discussion_link]["messages"][
                    f"{message_info['author']}_{message_num}"] = self.forum_collector.store_message_in_dict(
                    message_info, message_num)
                message_num += 1

            if return_messages:
                return self.discussions_dict[discussion_link]["messages"]

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
                                                                                     message_author_class,
                                                                                     only_discussion_link=True,
                                                                                     discussion_link=discussion_link)
                messages_dict[message_num] = message_info
                message_num += 1

            if return_messages:
                return messages_dict
