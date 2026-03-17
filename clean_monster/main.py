from data_clean_monster import clean_stock

import csv
import json
import sys

print('Running_file:',__file__) #此行相当于debug，第一时间输出在run的file避免改a运行b
if len(sys.argv) != 4:  # 这一步是参数检查，应该是确定参数只要不等于4个就直接print
    print('Usage:python3 main.py <input_csv> <output_json>')
    sys.exit(1)
mode = sys.argv[1]
input_csv = sys.argv[2]
output_json = sys.argv[3]

from data_clean_monster import clean_stock, clean_date, clean_price

CLEANER = {
    'stock': {
        'func': clean_stock,
        'field': 'stock',
    },
    'date': {
        'func': clean_date,
        'field': 'date',
    },
    'price': {
        'func': clean_price,
        'field': 'price', #这里的field是变量名：右边的是具体的列名所以一定不要搞错，遇到KeyError检查配置里的名字
    },
}  # 大概相当于这个字典里都是清洁工个，应该是需要哪个就调用哪个，目测field应该是调用名，func是背后对应的函数
if mode not in CLEANER:
    print(f'Unknow mode: {mode}')
    sys.exit(1)

cleaner = CLEANER[mode]['func']  # 中间的列表mode作用未知
field = CLEANER[mode]['field']

results = []
with open(input_csv, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print("DEBUG field =", field)
        print("DEBUG row keys =", row.keys())#这两行主要为了确认field避免KeyError
        new_row = {
            'id': row['id'],
            'field': cleaner(row[field]),  # 之前为clean_stock相当于用变量又加了一道锁，透明度降低，暴露风险更小
            'remark': row['remark'],
        }
        results.append(new_row)

with open(output_json, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=4)  # indent为缩进，通常为了人类可读性


