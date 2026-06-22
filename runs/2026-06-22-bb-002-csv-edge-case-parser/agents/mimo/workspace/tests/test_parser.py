from bb002_csvedge import summarize_people_csv


def test_quoted_commas_and_escaped_quotes():
    data = (
        'name,city,note\n'
        '"Doe, Jane",Amsterdam,"likes ""quoted"" text"\n'
        'John,Rotterdam,plain\n'
        '\n'
        'Alice,Amsterdam,"x,y"\n'
    )
    assert summarize_people_csv(data) == {"rows": 3, "by_city": {"Amsterdam": 2, "Rotterdam": 1}}
