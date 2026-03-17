import json
import csv


def clean_stock(value):
    try:
        if value is None:
            return None

        if not isinstance(value, str):
            return None

        value = value.strip().lower()#此句为抄袭gpt，因为显示数据可能是In stock AVAILABLE如果没有strip和lower那么下边的判断可能就失效了。
        #同时elif只能跟在if后边 如果跟在普通语句后边必定报错
        if value.strip() == '':
            return None

        if 'error' in value:  # 尝试过放最后，但是感觉要改放在这里
            return None

        if 'unknown' in value:#此条仅针对此处，不然全是if虽然最后可能返回out_stock但是不符合输出预期None感觉容易形成隐形问题
            return None

        if (('available' in value) or ('in stock' in value)
                or ('>=' in value) or ('y' in value) or ('yes' in value)
                or ('1' in value) or ('true' in value)):
            return 'in_stock'

        if (('out' in value) or ('0' in value) or ('no' in value ) or ('n' in value)
                or ('false' in value)):
            return 'out_of_stock'

    except TypeError:  # 没有int或者float数据类型，感觉TypeError足够接住
        return None


results = []

with open('stock.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)  # 感觉可以死记只要读csv文件都是DictReader不然不方便取列
    for row in reader:
        new_row = {
            'id': row['id'],
            'stock': clean_stock(row['stock']),
            'remark': row['remark'],
        }
        results.append(new_row)

with open('output.json','w',encoding='utf-8') as f:
    json.dump(results,f,ensure_ascii=False,indent=4)

print(f'json.dump is done') #想要看某个id或者某个key的情况，可以在for循环内通过if条件随时print
print(results)