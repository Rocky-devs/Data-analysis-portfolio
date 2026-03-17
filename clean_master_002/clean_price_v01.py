import csv
import json

# 判断逻辑越宽泛优先级越低，越往后/往下。规则越具体，越往前/往上
# 不要整if elif感觉非常不利于扩容  全部用if即可
def clean_price(value):
    try:
        if value is None:
            return None

        if not isinstance(value, str):
            return None

        if value.strip() == '': #前三if逻辑为字符串清洗标准防御性写法，可以死记。
            return None

        if ('€' in value) and ('-' in value):
            value = value.replace('€','')
            left,right = value.split('-')
            return (float(left.strip()) + float(right.strip()))/2 #这里比如float一次，不要因为有float兜底不写，不然python以为是str+str 有bug几率
            #这种针对性强的最好return，不然按执行逻辑因为都是if，欧元符号移除以后就进入下一步然后float兜底报错就nul了，所以逻辑闭环当场就要完成，也就是返回计算后的值，不能等统一

        if "$" in value:
            value = value.strip().replace('$','').strip()

        if '≈' in value:
            value = value.strip()
            value = value[1:]

        if 'USD' in value:
            value = value.strip().lower().replace('usd','') #涉及到英文字母的最好lower下，加点防御性

        value = float(value)
    except (ValueError, TypeError):
        return None

    return value


results = []

with open('price.csv', newline='', encoding='utf-8') as f:#不纠结这里的newline=''见多就懂了，和with open一样
    reader = csv.DictReader(f)
    for row in reader:
        new_row = {
            'id': row['id'],
            'amount': clean_price(row['price']),
            'remark': row['remark'],
        }
        results.append(new_row)#注意缩进，当前缩进表示没次循环都添加，如果和for同缩进仅在for结束后添加/只有最后一条row

with open('out_price.json','w',encoding='utf-8') as f:
    json.dump(results,f,ensure_ascii=False,indent=4) #勿要纠结json.dump()内的格式和意义

print(f'json.dump is done')#显示提醒上边的语句已经执行完毕，常用print，减少debug
print(results)
