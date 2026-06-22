import csv
import io


def summarize_people_csv(text: str) -> dict:
    reader = csv.reader(io.StringIO(text))
    rows = [row for row in reader if row and any(cell.strip() for cell in row)]
    header = rows[0]
    data_rows = rows[1:]
    by_city = {}
    for row in data_rows:
        record = dict(zip(header, row))
        city = record.get("city", "").strip()
        by_city[city] = by_city.get(city, 0) + 1
    return {"rows": len(data_rows), "by_city": dict(sorted(by_city.items()))}
