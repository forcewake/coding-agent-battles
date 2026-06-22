from vendor.textkit import STOPWORDS, words


def summarize(text: str):
    counts: dict[str, int] = {}
    for token in words(text):
        if token in STOPWORDS:
            continue
        counts[token] = counts.get(token, 0) + 1
    ranked = sorted(counts.items(), key=lambda wc: (-wc[1], wc[0]))
    return [{'word': w, 'count': c} for w, c in ranked[:3]]
