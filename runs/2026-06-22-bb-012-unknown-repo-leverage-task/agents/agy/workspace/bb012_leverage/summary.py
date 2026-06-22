from vendor import textkit

def summarize(text: str):
    # Use vendor.textkit.words for punctuation/case handling
    all_words = textkit.words(text)
    
    # Ignore stopwords from vendor.textkit.STOPWORDS
    filtered_words = [w for w in all_words if w not in textkit.STOPWORDS]
    
    # Count frequencies
    counts = {}
    for w in filtered_words:
        counts[w] = counts.get(w, 0) + 1
        
    # Sort: count descending, then word ascending
    sorted_words = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    
    # Return at most 3 entries as list of {word, count} dicts
    return [{'word': w, 'count': c} for w, c in sorted_words][:3]
