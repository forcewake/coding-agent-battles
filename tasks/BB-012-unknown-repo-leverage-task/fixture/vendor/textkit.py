import re
STOPWORDS = {'the', 'and', 'of', 'to', 'a'}
def words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())
