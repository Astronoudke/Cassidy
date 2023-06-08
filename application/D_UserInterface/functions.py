def obtain_title(title):
    if type(title) == str:
        return title
    elif len(title) == 0:
        return "No title found or properly loaded."
    elif len(title) == 1:
        return title[0]
    else:
        return ' '.join(title)