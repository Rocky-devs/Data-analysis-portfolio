"""
因为用的都是if，数据流入后会进入每个符合条件的if，而不是if elif结构一样只会进入其中一个if
此版本v2 默写 禁止参照v1 只准看price.csv也就是输入数据。测试euro先一个if移除euro，用后续的if继续处理
以后约等于号之类的不要查询\u2248这种邪典方法浪费时间，直接通过输入数据复制
可以根据输入数据写对应逻辑，但是写完最好根据逻辑调整下顺序
"""
import csv
import json
def clean_price(value):
    try:
        if value == None:
            return None

        if not isinstance(value,str):
            return None

        if value.strip() == '':
            return None

        value = value.strip().lower()

        if '$' in value:
            value = value.replace('$','').strip()

        if '€' in value:
            value = value.replace('€','').strip()


        if '≈' in value:
            value = value.replace('≈','').strip()

        if 'usd' in value:
            value = value.replace('usd','').strip()

        if '-' in value:
            left,right = value.split('-')
            value = (float(left.strip()) + float(right.strip()))/2

        value = float(value) #报错前要有个兜底，相当于上边挡不住的这里挡住，给except接住？
    except(ValueError,TypeError):
        return None

    return value

