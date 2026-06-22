import csv
import io


def summarize_people_csv(text: str) -> dict:
    """Summarize a people CSV.

    Uses proper CSV parsing semantics so quoted commas, escaped quotes,
    and blank rows are handled correctly. Fully blank rows are ignored.
    """
    reader = csv.DictReader(io.StringIO(text))

    by_city: dict[str, int] = {}
    rows = 0
    for row in reader:
        # Ignore fully blank rows (every field empty/whitespace only).
        if not any((value or "").strip() for value in row.values()):
            continue
        rows += 1
        city = (row.get("city") or "").strip()
        by_city[city] = by_city.get(city, 0) + 1

    return {"rows": rows, "by_city": dict(sorted(by_city.items()))}
