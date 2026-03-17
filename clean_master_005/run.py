import json
import csv
from .pipeline import process_row
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

results = []

with open(BASE_DIR / 'data' / 'data.csv', newline='', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        results.append(process_row(row))

with open('out_date.json','w',encoding='utf-8') as f:
    json.dump(results,f,ensure_ascii=False,indent=4)

print('ETL is done')