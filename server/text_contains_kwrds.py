import re

def text_contains_kwrds(text: str, keywords: list | tuple | set):
    pattern = "|".join(keywords)
    match = re.search(pattern, text, re.IGNORECASE)
    return True if match else False
