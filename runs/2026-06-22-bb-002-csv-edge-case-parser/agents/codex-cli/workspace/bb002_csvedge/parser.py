import csv
from io import StringIO


def summarize_people_csv(text: str) -> dict:
    parsed_rows = [
        row for row in csv.reader(StringIO(text))
        if any(cell.strip() for cell in row)
    ]
    header = parsed_rows[0]
    rows = [dict(zip(header, row)) for row in parsed_rows[1:]]
    by_city = {}
    for row in rows:
        city = row.get("city", "").strip()
        by_city[city] = by_city.get(city, 0) + 1
    return {"rows": len(rows), "by_city": dict(sorted(by_city.items()))}
