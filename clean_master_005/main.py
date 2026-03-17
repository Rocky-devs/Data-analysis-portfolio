import sys
import json
import csv

from clean_monster_v01 import clean_price, clean_stock, clean_date, clean_quantity

CLEANER = {
    'amount_usd': clean_price,
    'quantity': clean_quantity,
    'created_on': clean_date,
}

results = []
with open('data/data.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        new_row = {
            'uid': row['uid'],
            'note': row['note'],
        }
        for field,cleaner in CLEANER.items():
            raw = row.get(field)
            if raw is not None:
                new_row[field] = cleaner(raw)

        results.append(new_row)

with open('data/out_data.json', 'w', encoding='utf-8') as f:
    json.dump(results,f,ensure_ascii=False,indent=4)
