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


def clean_price(value):
    try:
        if value is None:
            return None

        elif not isinstance(value, str):
            return None

        elif value.strip() == '':
            return None

        elif '$' in value:
            value = value.replace('$', '').strip()

        elif ('€' in value) and ('-' in value):
            value = value.replace('€', '').strip()
            left,right = value.split('-')
            value = (float(left.strip())+float(right.strip()))/2

        elif '€' in value:
            value = value.replace('€', '').strip()

        elif '≈' in value:
            value = value.replace('≈', '').strip()

        elif '￥' in value:
            value = value.replace('￥', '').strip()

        elif 'USD' in value:
            value = value.replace('USD', '').strip()

        value = float(value)
    except (ValueError, TypeError):
        return None

    return value
