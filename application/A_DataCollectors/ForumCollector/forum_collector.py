import abc
import requests
from bs4 import BeautifulSoup, NavigableString, Tag

from .functions import extract_text_by_class, extract_href_by_class, create_discussion_url, clean_view_or_reply_amount, extract_text_by_class_split, filter_ints, find_href_by_text

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from B_Database.my_sql import DatabaseManager


class ForumCollector(abc.ABC):
    def __init__(self, identification: int, name: str, base_url: str, description: str, category_id: int,
                 has_url_suffix: bool = False, url_suffix: str = None):
        """
        :param base_url: The base URL of the forum.
        :param has_url_suffix: Whether the URL has a suffix at the end.
        :param url_suffix: The suffix of the URL. This might be used at the end of the URL (such as .html).
        """
        self.identification = identification
        self.name = name
        self.base_url = base_url
        self.description = description
        self.category_id = category_id

        self.has_url_suffix = has_url_suffix
        self.url_suffix = url_suffix

    def scrape_discussions_from_forum(self, discussion_class: str, full_discussion_class: bool, pagination_class: str):
        all_discussions = []

        # First determine the pages to parse through
        forum_url = BeautifulSoup(requests.get(self.base_url).content, 'html.parser')

        pagination = forum_url.find(class_=lambda x: x == pagination_class)
        pagination_texts = extract_text_by_class_split(pagination)
        pagination_pages = [int(x) for x in pagination_texts if x.isdigit()]

        start_page = 1
        end_page = max(pagination_pages)

        page = start_page

        while True:
            if page > end_page:
                break
            href = find_href_by_text(pagination, str(page))
            if self.has_url_suffix:
                if page == 1:
                    page_url = self.base_url + self.url_suffix
                else:
                    page_url = create_discussion_url(self.base_url, href) + self.url_suffix
            else:
                if page == 1:
                    page_url = self.base_url
                else:
                    page_url = create_discussion_url(self.base_url, href)
            print(page_url)
            forum_url = BeautifulSoup(requests.get(page_url).content, 'html.parser')

            if full_discussion_class:
                discussion_items = forum_url.find_all(class_=lambda x: x == discussion_class)
            else:
                discussion_items = forum_url.find_all(class_=lambda x: x and x.startswith(discussion_class))

            all_discussions.extend(discussion_items)
            page += 1

        return all_discussions

    def scrape_messages_from_discussion(self, message_class: str, full_message_class: bool, pagination_class: str,
                                        via_link: bool = False, discussion_link: str = None, discussion_id: int = None):
        if not via_link:
            db = DatabaseManager(user='root', password='', host='localhost', database_name='cassidy')
            db.connect()
            discussion = db.select_discussion(via_id=True, id=discussion_id)
            db.close()

            discussion_link = discussion["link"]

        all_messages = []

        # First determine the pages to parse through
        page_content = BeautifulSoup(requests.get(discussion_link).content, 'html.parser')

        pagination = page_content.find(class_=lambda x: x == pagination_class)
        pagination_texts = extract_text_by_class_split(pagination)
        pagination_pages = [int(x) for x in pagination_texts if x.isdigit()]

        start_page = 1
        end_page = max(pagination_pages)

        page = start_page

        while True:
            print(page)
            pagination = page_content.find(class_=lambda x: x == pagination_class)
            if page > end_page:
                break
            href = find_href_by_text(pagination, str(page))
            if self.has_url_suffix:
                if page == 1:
                    page_url = discussion_link + self.url_suffix
                else:
                    page_url = create_discussion_url(discussion_link, href) + self.url_suffix
            else:
                if page == 1:
                    page_url = discussion_link
                else:
                    page_url = create_discussion_url(discussion_link, href)
            print(page_url)
            page_content = BeautifulSoup(requests.get(page_url).content, 'html.parser')

            if full_message_class:
                message_items = page_content.find_all(class_=lambda x: x == message_class)
            else:
                message_items = page_content.find_all(class_=lambda x: x and x.startswith(message_class))

            all_messages.extend(message_items)
            page += 1

        return {"messages": all_messages}

    def return_discussion_info_from_scraped(self, discussion, name_class: str, creation_date_class: str,
                                            views_class: str, replies_class: str, last_post_time_class: str):
        discussion_name = extract_text_by_class(discussion, name_class)
        discussion_link = extract_href_by_class(discussion, name_class)
        discussion_creation_date = extract_text_by_class(discussion, creation_date_class)
        discussion_views = clean_view_or_reply_amount(extract_text_by_class(discussion, views_class))
        discussion_replies = clean_view_or_reply_amount(extract_text_by_class(discussion, replies_class))
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
                                         only_discussion_link: bool = False, discussion_link: str = None,
                                         discussion_id: int = None):
        message_text = extract_text_by_class(message, text_class)
        message_date = extract_text_by_class(message, date_class)
        message_author = extract_text_by_class(message, author_class)

        if only_discussion_link:
            return {
                "text": message_text,
                "date": message_date,
                "author": message_author,
                "discussion_link": discussion_link
            }

        else:
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
