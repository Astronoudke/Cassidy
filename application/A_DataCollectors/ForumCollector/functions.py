from urllib.parse import urljoin
from bs4 import NavigableString, Tag
from datetime import datetime


def extract_text_by_class(soup, class_: str):
    elements = soup.find_all(class_=class_)
    texts = []
    for element in elements:
        text = element.text.strip()
        if text:
            texts.append(text)
    return ' '.join(texts)


def extract_href_by_class(soup, class_: str):
    elements = soup.find_all(class_=class_)
    hrefs = []
    for element in elements:
        href = element.get('href')
        if href:
            hrefs.append(href)
        else:
            for sub_element in element.find_all('a', href=True):
                hrefs.append(sub_element['href'])
    return hrefs


def create_discussion_url(base_url: str, relative_url: str) -> str:
    """
    Creates a full discussion URL based on the base URL and a relative URL.

    :param base_url: The base URL of the forum.
    :param relative_url: The relative URL of the discussion.
    :return: The full URL of the discussion.
    """
    return urljoin(base_url, relative_url)


def convert_to_int(value):
    multiplier = 1

    if 'K' in value:
        multiplier = 1000
        value = value.replace('K', '')
    elif 'M' in value:
        multiplier = 1000000
        value = value.replace('M', '')

    try:
        return int(float(value) * multiplier)
    except ValueError:
        return 0


def clean_view_or_reply_amount(value):
    value = value.split('\n')[-1]
    cleaned_value = convert_to_int(value)

    return cleaned_value


def convert_date_for_db(date_string):
    for format in ["%b %d, %Y", "%d %B %Y", "%d %b %Y"]:
        try:
            return datetime.strptime(date_string, format).date()
        except ValueError:
            pass  # continue to next format

    return None


# Functions for pagination
def extract_text_by_class_split(element: Tag) -> list:
    """A function for getting the text within the pagination class."""
    texts = []
    for descendant in element.descendants:
        if isinstance(descendant, NavigableString):
            text = descendant.strip()  # remove leading/trailing white spaces
            if text:  # check if the text is not an empty string
                texts.append(text)
    return texts


def filter_ints(strings):
    """A function for getting the numbers out of the list of text within the pagination class."""
    result = []
    for string in strings:
        try:
            int(string)
            result.append(string)
        except ValueError:
            pass
    return result


def find_href_by_text(element: Tag, text: str) -> str:
    for descendant in element.descendants:
        if isinstance(descendant, Tag) and descendant.name == 'a':
            if descendant.get_text(strip=True) == text:
                return descendant.get('href')
    return None  # return None if no link with the specified text was found
