from bb012_leverage import summarize

def test_uses_vendor_tokenization_and_stopwords():
    text = 'The agent, agent; AGENT! cost-of-change and process process to verify.'
    assert summarize(text) == [
        {'word': 'agent', 'count': 3},
        {'word': 'process', 'count': 2},
        {'word': 'change', 'count': 1},
    ]
