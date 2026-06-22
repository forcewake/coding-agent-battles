def summarize(text: str):
    # BUG: whitespace split keeps punctuation/case and stopwords.
    counts = {}
    for token in text.split():
        counts[token] = counts.get(token, 0) + 1
    return [{'word': w, 'count': c} for w, c in counts.items()][:3]
