import abc
import requests
from bs4 import BeautifulSoup

from .functions import extract_text_by_class, extract_href_by_class, create_discussion_url, clean_data

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from B_Database.my_sql import DatabaseManager


class ForumCollector(abc.ABC):
    def __init__(self, identification: int, name: str, base_url: str, description: str, category_id: int,
                 page_param: str, start_page: int, page_increment: int, has_url_suffix: bool = False,
                 url_suffix: str = None):
        """
        :param base_url: The base URL of the forum.
        :param page_param: The URL parameter used to specify the page number.
        :param start_page: The page number to start with.
        :param page_increment: The number of pages to increment by.
        :param has_url_suffix: Whether the URL has a suffix at the end.
        :param url_suffix: The suffix of the URL. This might be used at the end of the URL (such as .html).
        """
        self.identification = identification
        self.name = name
        self.base_url = base_url
        self.description = description
        self.category_id = category_id

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

    def scrape_messages_from_discussion(self, message_class: str, full_message_class: bool,
                                        page_param: str = None, start_page: str = None, page_increment: str = None,
                                        via_link: bool = False, discussion_link: str = None, discussion_id: int = None):
        if not via_link:
            db = DatabaseManager(user='root', password='', host='localhost', database_name='cassidy')
            db.connect()
            discussion = db.select_discussion(via_id=True, id=discussion_id)
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

    def return_discussion_info_from_scraped(self, discussion, name_class: str, creation_date_class: str,
                                            views_class: str,
                                            replies_class: str, last_post_time_class: str):
        discussion_name = extract_text_by_class(discussion, name_class)
        discussion_link = extract_href_by_class(discussion, name_class)
        discussion_creation_date = extract_text_by_class(discussion, creation_date_class)
        discussion_views = clean_data(extract_text_by_class(discussion, views_class))
        discussion_replies = clean_data(extract_text_by_class(discussion, replies_class))
        discussion_last_post_time = extract_text_by_class(discussion, last_post_time_class)

        discussion_link = create_discussion_url(self.base_url, discussion_link[0])

        return {
            "name": discussion_name,
            "link": discussion_link,
            "creation date": discussion_creation_date,
            "views": discussion_views,
            "replies": discussion_replies,
            "last_post_time": discussion_last_post_time,
            "forum_id": self.identification
        }

    def return_message_info_from_scraped(self, message, text_class: str, date_class: str, author_class: str,
                                         discussion_id: int):
        message_text = extract_text_by_class(message, text_class)
        message_date = extract_text_by_class(message, date_class)
        message_author = extract_text_by_class(message, author_class)

        return {
            "text": message_text,
            "date": message_date,
            "author": message_author,
            "discussion_id": discussion_id
        }

    def store_discussion_in_database(self, discussion):
        db = DatabaseManager(user='root', password='', host='localhost', database_name='cassidy')
        db.connect()
        db.add_discussion(
            discussion["name"],
            discussion["link"],
            discussion["creation date"],
            discussion["views"],
            discussion["replies"],
            discussion["last_post_time"],
            discussion["forum_id"]
        )
        db.close()

    def store_message_in_database(self, message, user_id: int):
        db = DatabaseManager(user='root', password='', host='localhost', database_name='cassidy')
        db.connect()
        db.add_message(
            message["text"],
            message["date"],
            user_id,
            message["discussion_id"]
        )
        db.close()

    def new_discussions_via_forumlink(self, discussion_class: str, full_discussion_class: bool,
                                      discussion_name_class: str, discussion_creation_date_class: str,
                                      discussion_views_class: str, discussion_replies_class: str,
                                      discussion_last_post_time_class: str):
        discussions = self.scrape_discussions_from_forum(discussion_class, full_discussion_class)
        for discussion in discussions:
            discussion_info = self.return_discussion_info_from_scraped(discussion, discussion_name_class,
                                                                       discussion_creation_date_class,
                                                                       discussion_views_class, discussion_replies_class,
                                                                       discussion_last_post_time_class)
            self.store_discussion_in_database(discussion_info)

    def new_messages_via_discussionlink(self, discussion_link: str, message_class: str, full_message_class: bool,
                                        message_text_class: str, message_date_class: str, message_author_class: str):
        db = DatabaseManager(user='root', password='', host='localhost', database_name='cassidy')
        db.connect()
        discussion_info = db.select_discussion(via_link=True, link=discussion_link)

        if discussion_info is None:
            raise Exception("Discussion not found in database")

        messages = self.scrape_messages_from_discussion(discussion_link=discussion_link, message_class=message_class,
                                                        full_message_class=full_message_class, via_link=True)[
            "messages"]
        for message in messages:
            message_info = self.return_message_info_from_scraped(message, message_text_class, message_date_class,
                                                                 message_author_class, discussion_info["id"])

            author = db.select_author_by_username_and_forum_id(message_info["author"], self.identification)

            if author is None:
                db.add_author(message_info["author"], self.identification)
                author_id = db.select_user_by_username_and_forum_id(message_info["author"], self.identification)["id"]
            else:
                author_id = author["id"]

            self.store_message_in_database(message_info, author_id)

        db.close()
