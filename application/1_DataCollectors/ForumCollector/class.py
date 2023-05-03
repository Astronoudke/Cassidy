import abc
import requests
from bs4 import BeautifulSoup

from functions import extract_text_by_class, extract_href_by_class, create_discussion_url


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

    def collect_discussion_items(self, discussion_class: str, full_discussion_class: bool):
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

    def collect_message_items(self, discussion_link: str, message_class: str, full_message_class: bool,
                              page_param: str = None, start_page: str = None, page_increment: str = None):

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

        return all_messages

    def return_discussion_info(self, discussion, title_class: str, date_class: str, last_post_time_class: str):
        discussion_title = extract_text_by_class(discussion, title_class)
        discussion_link = extract_href_by_class(discussion, title_class)
        discussion_date = extract_text_by_class(discussion, date_class)
        discussion_last_post_time = extract_text_by_class(discussion, last_post_time_class)

        discussion_link = create_discussion_url(self.base_url, discussion_link[0])

        return {
            "title": discussion_title,
            "link": discussion_link,
            "creation date": discussion_date,
            "last_post_time": discussion_last_post_time
        }

    def return_message_info(self, message, text_class: str, date_class: str, author_class: str):
        message_text = extract_text_by_class(message, text_class)
        message_date = extract_text_by_class(message, date_class)
        message_author = extract_text_by_class(message, author_class)

        return {
            "text": message_text,
            "date": message_date,
            "author": message_author
        }

    def return_info_all_discussions(self, discussion_items, title_class: str, date_class: str, last_post_time_class: str):
        discussions_dict = {}
        num = 1
        for discussion in discussion_items:
            discussions_dict[num] = self.return_discussion_info(discussion, title_class, date_class, last_post_time_class)
            num += 1
        return discussions_dict

    def return_info_all_messages(self, message_items, text_class: str, date_class: str, author_class: str):
        messages_dict = {}
        num = 1
        for message in message_items:
            messages_dict[num] = self.return_message_info(message, text_class, date_class, author_class)
            num += 1
        return messages_dict


if __name__ == "__main__":
    psv_collector = ForumCollector(base_url="https://forum.psv.nl/index.php?forums/psv-1-selectie-technische-staf.11/",
                                page_param="page-", start_page=1, page_increment=1)

    psv_discussions = psv_collector.collect_discussion_items(discussion_class="structItem structItem--thread "
                                                                          "js-inlineModContainer js-threadListItem",
                                                             full_discussion_class=False)

    psv_info_discussions = psv_collector.return_info_all_discussions(discussion_items=psv_discussions, title_class="structItem-title",
                                           date_class="structItem-startDate",
                                           last_post_time_class="structItem-latestDate u-dt")

    psv_messages = psv_collector.collect_message_items(discussion_link=psv_info_discussions[4]["link"],
                                                   message_class="message message--post js-post js-inlineModContainer",
                                                   full_message_class=False)

    psv_info_messages = psv_collector.return_info_all_messages(message_items=psv_messages, text_class="bbWrapper", date_class="u-dt", author_class="username")

    print(psv_info_messages)