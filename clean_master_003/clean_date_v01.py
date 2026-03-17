import csv
import json


def clean_date(value):
    try:
        if value is None:
            return None

        elif value.strip() == '':
            return None

        elif any(ch.isalpha() for ch in value):#此句为gpt提供，具体含义不懂，像个列表推导式
            return None

        elif '/' in value:
            value = value.replace('/', '-').strip()  # 链式调用的strip()为防御，比如以后扩容更多方法爬有space出bug

        elif '.' in value:
            value = value.replace('.', '-0').strip()  # 此处讨巧直接replace一起替换

        elif '-' in value:
            left,mid,right = value.split('-')
            if len(left)==4:
                value = f'{left}-{mid}-{right}'
            else:
                value = f'{right}-{left}-{mid}'#此处偏脚本思维，仅能针对当前情况

    except (ValueError, TypeError):
        return None

    return value

results = [] #读取之前就要新建一个空列表，因为读取，写入都要用
with open('date.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row["id"] in {"5", "7"}:  # 此为gpt提供debug方法，打印指定id的数据，本质疑似还是为for key in dict，因为id是个key，in后边的是字典
            print("ROW DEBUG:", row)
        new_row = {
            'id': row['id'],
            'date': clean_date(row['date']),
            'remark': row['remark'],
        }
        results.append(new_row)

with open('output.json','w', encoding= 'utf-8') as f:
    json.dump(results,f,ensure_ascii=False,indent=4)

print(f'results.json is output')#保持print测试习惯 减少debug时间



