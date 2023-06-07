import abc
import requests
from bs4 import BeautifulSoup, NavigableString, Tag

from .functions import extract_text_by_class, extract_href_by_class, create_discussion_url, clean_view_or_reply_amount, extract_text_by_class_split, filter_ints, find_href_by_text

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))


class ForumCollector(abc.ABC):
    def __init__(self, name: str, base_url: str, description: str, category: str,
                 has_url_suffix: bool = False, url_suffix: str = None):
        """
        :param base_url: The base URL of the forum.
        :param has_url_suffix: Whether the URL has a suffix at the end.
        :param url_suffix: The suffix of the URL. This might be used at the end of the URL (such as .html).
        """
        self.name = name
        self.base_url = base_url
        self.description = description
        self.category = category

        self.has_url_suffix = has_url_suffix
        self.url_suffix = url_suffix

    def scrape_discussions_from_forum(self, discussion_class: str, full_discussion_class: bool, pagination_class: str):
        all_discussions = []

        # First determine the pages to parse through
        page_content = BeautifulSoup(requests.get(self.base_url).content, 'html.parser')

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
                    page_url = self.base_url + self.url_suffix
                else:
                    page_url = create_discussion_url(self.base_url, href) + self.url_suffix
            else:
                if page == 1:
                    page_url = self.base_url
                else:
                    page_url = create_discussion_url(self.base_url, href)
            print(page_url)
            page_content = BeautifulSoup(requests.get(page_url).content, 'html.parser')

            if full_discussion_class:
                discussion_items = page_content.find_all(class_=lambda x: x == discussion_class)
            else:
                discussion_items = page_content.find_all(class_=lambda x: x and x.startswith(discussion_class))

            all_discussions.extend(discussion_items)
            page += 1

        return all_discussions

    def scrape_messages_from_discussion(self, message_class: str, full_message_class: bool, pagination_class: str,
                                        discussion_link: str):
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

    def return_discussion_info_from_scraped(self, discussion, name_class: str):
        discussion_name = extract_text_by_class(discussion, name_class)
        discussion_link = extract_href_by_class(discussion, name_class)

        discussion_link = create_discussion_url(self.base_url, discussion_link[0])

        return {
            "name": discussion_name,
            "link": discussion_link,
        }

    def return_message_info_from_scraped(self, message, text_class: str, author_class: str, discussion_link: str = None):
        message_text = extract_text_by_class(message, text_class)
        message_author = extract_text_by_class(message, author_class)

        return {
                "text": message_text,
                "author": message_author,
                "discussion_link": discussion_link
            }

    def store_discussion_in_dict(self, discussion):
        return {"name": discussion["name"], "link": discussion["link"]}

    def store_message_in_dict(self, message, user_id):
        message_id = f"{message['author']}_{user_id}"
        return {message_id: message["text"]}
