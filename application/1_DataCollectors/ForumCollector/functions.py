from urllib.parse import urljoin


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
