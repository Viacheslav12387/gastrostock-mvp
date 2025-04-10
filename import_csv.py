def import_csv_to_json():
    data = []
    with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for idx, row in enumerate(reader):
            item = {
                "id": idx + 1,
                "product": row["Produkt"],
                "unit": row["Jednostka"],
                "min_stock": int(row["Min. stan"]) if row["Min. stan"] else 0,
                "unit_cost": float(row["Koszt (zł)"]) if row["Koszt (zł)"] else 0.0,
                "supplier": row["Dostawca"],
                "category": row["Kategoria"]
            }
            data.append(item)

    with open(JSON_FILE, "w", encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=4)
        print(f"✅ Zaimportowano {len(data)} produktów z CSV do JSON!")
