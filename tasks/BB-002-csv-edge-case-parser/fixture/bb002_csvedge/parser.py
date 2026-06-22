def summarize_people_csv(text: str) -> dict:
    lines = [line for line in text.splitlines() if line.strip()]
    header = lines[0].split(",")
    rows = [dict(zip(header, line.split(","))) for line in lines[1:]]
    by_city = {}
    for row in rows:
        city = row.get("city", "").strip()
        by_city[city] = by_city.get(city, 0) + 1
    return {"rows": len(rows), "by_city": dict(sorted(by_city.items()))}
