import csv
import json


def clean_value(value):
        try:
            if value is None:
                return None

            elif  not isinstance(value,str):
                return None

            elif value.strip() == '':
                return None

            elif 'x' in value:
                left,right = value.split('x')
                value = float(left.strip()) * float(right.strip())

            elif '-' in value:
                value = value.replace('pcs','').strip()
                left,right = value.split('-')
                value = (float(left.strip()) + float(right.strip()))/2

            elif '%' in value:
                value = value.replace('%','').strip()
                value = float(value.strip())/100

            elif 'pcs' in value:
                value = value.replace('pcs','').strip()

            elif ('>=' in value) and ('pcs' in value):
                value = value.replace('>=','').replace('pcs','').strip()

            value = float(value)
        except (ValueError,TypeError):
            return None

        return value

def clean_price(value):
    try:
        if  value is None:
            return None

        elif not isinstance(value,str):
            return None

        elif value.strip() == '':
            return None

        elif '-' in value:
            left,right = value.split('-')
            value = (float(left.strip()) + float(right.strip()))/2

        elif  '\u2248' in value:#约等于不会输入，查询百度为\u2248
            value = value[1:]#尝试直接切片

        value = float(value) #以下部分皆为照抄，应该是用float来兜底，无法float的都except直接接然后返回None，待验证
    except (ValueError,TypeError):
        return None

    return value




results = []

with open ('data.csv',newline='',encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        new_row = {
            'id': row['id'],
            'quantity': clean_value(row['quantity']),
            'price': clean_price(row['price']),
            'remark': row['remark'],
        } #相当于提取quantity列清洗后，把剩余的字段统一加入new_row这个字典并append进列表result，理解题意，多做尝试，才能记住，别怕错，
        results.append(new_row)


with open('output.json','w',encoding='utf-8') as f:
    json.dump(results,f,ensure_ascii=False,indent=2)
print(f'json.dump is done')#写入完成后print一个str证明print之前的语句已经执行完毕，并检查json文件
print(results)#此处输出在pycharm内为一整行，不方便人眼阅读，待优化