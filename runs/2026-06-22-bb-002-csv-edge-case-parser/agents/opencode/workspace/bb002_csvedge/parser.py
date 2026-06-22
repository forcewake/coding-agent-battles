import csv
import io


def summarize_people_csv(text: str) -> dict:
    reader = csv.DictReader(io.StringIO(text))
    by_city = {}
    rows = 0
    for row in reader:
        if row is None:
            continue
        if not any((value or "").strip() for value in row.values()):
            continue
        rows += 1
        city = (row.get("city") or "").strip()
        by_city[city] = by_city.get(city, 0) + 1
    return {"rows": rows, "by_city": dict(sorted(by_city.items()))}
