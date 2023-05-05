import abc
import requests
from bs4 import BeautifulSoup

from .functions import extract_text_by_class, extract_href_by_class, create_discussion_url, clean_data

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from B_Database.my_sql import DatabaseManager


class ForumCollector(abc.ABC):
    def __init__(self, base_url: str, page_param: str, start_page: int, page_increment: int,
                 has_url_suffix: bool = False, url_suffix: str = None):
        """
        :param base_url: The base URL of the forum.
        :param page_param: The URL parameter used to specify the page number.
        :param start_page: The page number to start with.
        :param page_increment: The number of pages to increment by.
        :param has_url_suffix: Whether the URL has a suffix at the end.
        :param url_suffix: The suffix of the URL. This might be used at the end of the URL (such as .html).
        """
        self.base_url = base_url
        self.page_param = page_param
        self.start_page = start_page
        self.page_increment = page_increment
        self.has_url_suffix = has_url_suffix
        self.url_suffix = url_suffix

    def scrape_discussions_from_forum(self, discussion_class: str, full_discussion_class: bool):
        all_discussions = []
        page_number = self.start_page
        last_discussion_items = None

        while True:
            if self.has_url_suffix:
                page_url = self.base_url + self.page_param + str(page_number) + self.url_suffix
            else:
                page_url = self.base_url + self.page_param + str(page_number)

            forum_url = BeautifulSoup(requests.get(page_url).content, 'html.parser')

            if full_discussion_class:
                discussion_items = forum_url.find_all(class_=lambda x: x == discussion_class)
            else:
                discussion_items = forum_url.find_all(class_=lambda x: x and x.startswith(discussion_class))

            # Check if the current list of items is the same as the previous list of items
            if last_discussion_items and discussion_items == last_discussion_items:
                break

            all_discussions.extend(discussion_items)
            last_discussion_items = discussion_items
            page_number += self.page_increment

        return all_discussions

    def scrape_discussion_from_forum_by_link(self, discussion_link: str, full_discussion_class: bool):
        pass

    def scrape_messages_from_discussion(self, message_class: str, full_message_class: bool,
                              page_param: str = None, start_page: str = None, page_increment: str = None,
                              via_link: bool = False, discussion_link: str = None, discussion_id: int = None):
        if not via_link:
            db = DatabaseManager(user='root', password='', host='localhost', database_name='cassidy')
            db.connect()
            # messages is a list containing tuples for each message, with the contents of each message item
            # in the order of (id, text, date, user_id, discussion_id)
            discussion = db.select_discussion(discussion_id)
            db.close()

            discussion_link = discussion["link"]

        if page_param is None:
            page_param = self.page_param
        if start_page is None:
            start_page = self.start_page
        if page_increment is None:
            page_increment = self.page_increment

        all_messages = []
        page_number = start_page
        last_message_items = None

        while True:
            if self.has_url_suffix:
                page_url = discussion_link + page_param + str(page_number) + self.url_suffix
            else:
                page_url = discussion_link + page_param + str(page_number)

            print(page_url)
            forum_url = BeautifulSoup(requests.get(page_url).content, 'html.parser')

            if full_message_class:
                message_items = forum_url.find_all(class_=lambda x: x == message_class)
            else:
                message_items = forum_url.find_all(class_=lambda x: x and x.startswith(message_class))

            # Check if the current list of items is the same as the previous list of items
            if last_message_items and message_items == last_message_items:
                break

            all_messages.extend(message_items)
            last_message_items = message_items
            page_number += page_increment

        return {"messages": all_messages, "discussion_id": discussion_id, "discussion_link": discussion_link}

    def return_discussion_info_from_scraped(self, discussion, title_class: str, creation_date_class: str, views_class: str,
                               replies_class: str, last_post_time_class: str):
        discussion_title = extract_text_by_class(discussion, title_class)
        discussion_link = extract_href_by_class(discussion, title_class)
        discussion_creation_date = extract_text_by_class(discussion, creation_date_class)
        discussion_views = clean_data(extract_text_by_class(discussion, views_class))
        discussion_replies = clean_data(extract_text_by_class(discussion, replies_class))
        discussion_last_post_time = extract_text_by_class(discussion, last_post_time_class)

        discussion_link = create_discussion_url(self.base_url, discussion_link[0])

        return {
            "title": discussion_title,
            "link": discussion_link,
            "creation date": discussion_creation_date,
            "views": discussion_views,
            "replies": discussion_replies,
            "last_post_time": discussion_last_post_time
        }

    def return_message_info_from_scraped(self, message, text_class: str, date_class: str, author_class: str, discussion_id: int):
        message_text = extract_text_by_class(message, text_class)
        message_date = extract_text_by_class(message, date_class)
        message_author = extract_text_by_class(message, author_class)

        return {
            "text": message_text,
            "date": message_date,
            "author": message_author,
            "discussion_id": discussion_id
        }

    def return_info_all_discussions_from_scraped(self, discussion_class: str, full_discussion_class: bool, title_class: str,
                                    creation_date_class: str, views_class: str, replies_class: str,
                                    last_post_time_class: str):
        discussions_dict = {}
        num = 1
        discussion_items = self.scrape_discussions_from_forum(discussion_class, full_discussion_class)
        for discussion in discussion_items:
            discussions_dict[num] = self.return_discussion_info_from_scraped(discussion, title_class, creation_date_class,
                                                                views_class, replies_class, last_post_time_class)
            num += 1
        return discussions_dict

    def return_info_all_messages_from_scraped(self, discussion_id: int, message_class: str, full_message_class: bool,
                                 text_class: str, date_class: str, author_class: str, store_in_database: bool = False):
        messages_dict = {}
        num = 1
        message_items = self.scrape_messages_from_discussion(discussion_id=discussion_id, message_class=message_class,
                                                   full_message_class=full_message_class, via_link=False)["messages"]
        for message in message_items:
            messages_dict[num] = self.return_message_info_from_scraped(message, text_class, date_class, author_class, discussion_id)
            num += 1

        if store_in_database:
            db = DatabaseManager(user='root', password='', host='localhost', database_name='cassidy')
            db.connect()
            # messages is a list containing tuples for each message, with the contents of each message item
            # in the order of (id, text, date, user_id, discussion_id)
            for message in messages_dict.values():
                db.add_message(message["discussion_id"], message["text"], message["date"], message["author"])
            db.close()

        return messages_dict


