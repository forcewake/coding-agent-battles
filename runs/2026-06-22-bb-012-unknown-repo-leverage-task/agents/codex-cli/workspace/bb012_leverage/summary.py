from collections import Counter

from vendor.textkit import STOPWORDS, words


def summarize(text: str):
    counts = Counter(word for word in words(text) if word not in STOPWORDS)
    top_words = sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:3]
    return [{'word': word, 'count': count} for word, count in top_words]
