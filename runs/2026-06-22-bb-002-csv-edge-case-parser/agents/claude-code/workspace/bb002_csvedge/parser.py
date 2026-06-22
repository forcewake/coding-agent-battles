import csv
import io


def summarize_people_csv(text: str) -> dict:
    # csv.reader handles quoted commas, "" escapes, and quoting rules.
    rows = [r for r in csv.reader(io.StringIO(text)) if any(f.strip() for f in r)]
    header = rows[0]
    idx = header.index("city")
    by_city = {}
    for row in rows[1:]:
        city = row[idx].strip() if idx < len(row) else ""
        by_city[city] = by_city.get(city, 0) + 1
    return {"rows": len(rows) - 1, "by_city": dict(sorted(by_city.items()))}
