import csv
import io

def summarize_people_csv(text: str) -> dict:
    f = io.StringIO(text)
    reader = csv.reader(f, skipinitialspace=True)
    
    header = None
    rows = []
    
    for row in reader:
        # Ignore fully blank rows.
        # A row is fully blank if it is empty, or if all elements are whitespace.
        if not row or all(not cell.strip() for cell in row):
            continue
            
        if header is None:
            # We also strip header keys to be robust against leading/trailing spaces in the header.
            header = [h.strip() for h in row]
        else:
            row_dict = dict(zip(header, row))
            rows.append(row_dict)
            
    by_city = {}
    for row in rows:
        city = row.get("city", "").strip()
        by_city[city] = by_city.get(city, 0) + 1
        
    return {"rows": len(rows), "by_city": dict(sorted(by_city.items()))}
