def clean_date(value):
    try:
        if value is None:
            return None
        if not isinstance(value, str):
            return None
        if value.strip() == '':
            return None

        value = value.strip().lower()  # 防御性写法，针对强否定，未验证是否报错

        None_keys = {'unknown', 'error'}
        if value in None_keys:
            return None

        if '/' in value:
            value = value.replace('/', '-').strip()

        if '.' in value:
            value = value.replace('.', '-').strip()
        # 至此格式转换完毕，开始考虑按年-月-日 排序
        parts = value.split('-')  # 此时parts还是个包（年-月-日）
        if len(parts) != 3:
            return None
        # 拆分，排序
        a, b, c = parts  # 二次拆包

        if len(a) == 4:
            year, month, day = a, b, c
        elif len(c) == 4:
            year, month, day = c, b, a
        else:
            return None
        # 合法性判断
        year, month, day = int(year), int(month), int(day)
        if month < 1 or month > 12:
            return None
        if day < 1 or day > 31:
            return None

    except (ValueError, TypeError):  # 纯粹感觉 except应该接住点什么
        return None

    return f'{year:04d}-{month:02d}-{day:02d}'


def clean_price(value):
    try:
        if value is None:
            return None
        if not isinstance(value, str):
            return None
        if value.strip() == '':
            return None

        value = value.strip().lower()
        if '$' in value:
            value = value.replace('$', '')

        if '€' in value:
            value = value.replace('€', '')

        if '≈' in value:
            value = value.replace('≈', '')

        if 'usd' in value:
            value = value.replace('usd', '')

        if '-' in value:
            left, right = value.split('-')
            value = (float(left.strip()) + float(right.strip())) / 2

        value = float(value)
    except (ValueError, TypeError):
        return None

    return value


def clean_quantity(value):
    try:
        if value is None:
            return None
        if not isinstance(value, str):
            return value
        if value.strip() == '':
            return None

        value = value.strip().lower()  # 原始数据有usd之类的英文 ，统一先转小写，方便后续

        if 'pcs' in value:
            value = value.replace('pcs', '').strip()

        if 'x' in value:
            left, right = value.split('x')
            return (float(left.strip()) * float(right.strip()))

        if '>=' in value:
            value = value.replace('>=', '').strip()

        if '-' in value:
            left, right = value.split('-')
            value = ((float(left.strip())) + (float(right.strip()))) / 2

        value = float(value)

    except (ValueError, TypeError):
        return None

    return value


import csv
import json

CLEANER = {
    'total_price': clean_price,
    'qty': clean_quantity,
    'created_at': clean_date,
}

results = []
errors = []
error_summary = {}
errors_by_uid = {}

with open('data.csv', newline='', encoding='utf-8') as f:
    for rownum, row in enumerate(csv.DictReader(f), start=2):
        new_row = {
            'uid': row.get('uid'),  # row['uid']如果遇到为空的直接报错，get好点不报错，row.get('uid')就是获取uid的值
            'note': row.get('note'),
        }
        for field, cleaner in CLEANER.items():
            raw = row.get(field)
            if raw is None:
                continue

            cleaned = cleaner(raw)

            if cleaned is not None:
                new_row[field] = cleaned

            if cleaned is None:
                uid = row['uid']
                if uid not in errors_by_uid:
                    errors_by_uid[uid] = {
                        'rownum': rownum,
                        'row': row,
                        'errors': [],
                    }
                errors_by_uid[uid]['errors'].append({
                    'field': field,
                    'raw': raw,
                    'cleaner': cleaner.__name__,
                })
                error_summary[field] = error_summary.get(field, 0) + 1

        results.append(new_row)

with open('out_result.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=4)

with open('out_errors.json', 'w', encoding='utf-8') as f:
    json.dump(errors, f, ensure_ascii=False, indent=4)

with open('out_by_uid.json','w',encoding='utf-8') as f:
    json.dump(errors_by_uid,f,ensure_ascii=False,indent=4)

with open('out_summary', 'w', encoding='utf-8') as f:
    json.dump(error_summary, f, ensure_ascii=False, indent=4)

print('all json file is done')
