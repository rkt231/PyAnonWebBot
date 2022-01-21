from bs4 import BeautifulSoup


def bs4_find_all(content, tag, attrs, recursive, search_string, limit):
    """
    This function is just a basic soup.find_all() wrapper
    """
    results = None
    soup = BeautifulSoup(content, "html.parser")
    results = soup.find_all(tag, attrs, recursive, string=search_string, limit=limit)
    return results