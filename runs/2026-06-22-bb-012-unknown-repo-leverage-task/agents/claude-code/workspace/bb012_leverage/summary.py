from vendor.textkit import STOPWORDS, words


def summarize(text: str):
    counts = {}
    for w in words(text):
        if w in STOPWORDS:
            continue
        counts[w] = counts.get(w, 0) + 1
    top = sorted(counts.items(), key=lambda wc: (-wc[1], wc[0]))[:3]
    return [{'word': w, 'count': c} for w, c in top]
