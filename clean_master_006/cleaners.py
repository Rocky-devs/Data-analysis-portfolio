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


"""
clean_date_v02.py 纯默写版
"""


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

    return f'{year:04d}-{month:02d}-{day:02d}'  # 02d确保有0补位比如1月变成01


def clean_discount(value):
    try:
        if value is None:
            return None
        if not isinstance(value, str):
            return None
        value = value.strip().lower()
        if value == '':
            return None

        if value.endswith('%'):
            return float(value.replace('%', '')) / 100

        return float(value)
    except(ValueError, TypeError):
        return None
