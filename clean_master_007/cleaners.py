import pandas as pd


def clean_price_series(series):  # 一般类似replace这样的不用if，不然冗余，split之类的可以

    s = series.str.lower().str.strip()

    none_tokens = {'', '-', '—', 'n/a', 'na', 'none', 'null', 'unknown', 'error', ''}
    s = s.replace(list(none_tokens), pd.NA)

    s = (
        s.str.replace(',', '', regex=False)
        .str.replace('$', '', regex=False)
        .str.replace('￥', '', regex=False)
        .str.replace('¥', '', regex=False)
        .str.replace('€', '', regex=False)

        .str.replace('usd', '', regex=False)
        .str.replace('cny', '', regex=False)
        .str.replace('rmb', '', regex=False)

        .str.replace('=', '', regex=False)
        .str.replace('≈', '', regex=False)
        .str.replace('~', '', regex=False)
        .str.replace(' ', '', regex=False)
    )

    s = s.str.extract(r'(\d+\.?\d*)')[0]

    return s.astype(float)

def clean_quantity_series(series):

    s = series.astype(str).str.lower().str.strip()

    none_tokens = {'', '-', '—', 'n/a', 'na', 'none', 'null', 'unknown', 'error'}
    s = s.replace(list(none_tokens), pd.NA)

    s = (
        s.str.replace('units', '', regex=False)
        .str.replace('unit', '', regex=False)
        .str.replace('pieces', '', regex=False)  # pieces规则一定要在piece之前，不然肯定出问题，其他无所谓，类似复数规则必须复数在前
        .str.replace('piece', '', regex=False)
        .str.replace('plus', '', regex=False)
        .str.replace('approx', '', regex=False)
        .str.replace('about', '', regex=False)
        .str.replace('pcs', '', regex=False)

        .str.replace('+', '', regex=False)
        .str.replace('~', '', regex=False)
        .str.replace(',', '', regex=False)
        .str.replace('<=', '', regex=False)
        .str.replace('>=', '', regex=False)
        .str.replace(' ', '', regex=False)
    )

    first = s.str.extract(r'(\d+\.?\d*)')[0].astype(float)
    second = s.str.extract(r'\d+\.?\d*[x\-\*](\d+\.?\d*)')[0].astype(float)

    result = first.copy()

    mask_mul = (
        s.str.contains('x', na=False)
        | s.str.contains(r'\*', na=False)
    )

    result[mask_mul] = first[mask_mul] * second[mask_mul]

    mask_range = s.str.contains('-', na=False)

    result[mask_range] = (
        first[mask_range] + second[mask_range]) / 2

    return result

def clean_discount_series(series):
    # 入口统一化，转字符串，转小写，去空格
    s = series.astype(str).str.lower().str.strip()

    none_tokens = {'', '-', 'n/a', 'na', 'none','null', 'unknown', 'error'}
    s = s.replace(list(none_tokens), pd.NA)  # 统一缺失值，pd.NA为pandas官方推荐，避免出现个别数据类型的隐性问题

    s = (
        s.str.replace('%', '', regex=False)
        .str.replace('％','',regex=False)
        .str.replace('percent', '', regex=False)
        .str.replace('pct', '', regex=False)
        .str.replace(' ', '', regex=False)
    )  # 去除文字单位

    # 转成数值
    s = pd.to_numeric(s, errors='coerce')

    # 大于1的
    s = s.where(s <= 1, s / 100) # 括号内第一个参数为con，即s<=1 True时保留原值，如果是False证明原值>1，就用原值/100
    # 保留合法折扣0～1
    s = s.where((s >= 0) & (s <= 1)) # 只保留符合（）内条件的值/0<= s <= 1，其余的全部pd.NA,等价于s.where((s>=1)&(s<=1),pd.NA)

    return s


from datetime import datetime


def clean_date(value):
    try:
        if value is None:
            return None
        value = str(value).lower().strip()

        none_tokens = {'unknown', 'error', 'na', 'n/a', 'none', 'null', '-', '—', '', }
        if value in none_tokens:
            return None

        if 't' in value:
            value = value.split('t')[0]
        # 标准化分隔符
        value = (
            value.replace('/', '-')
            .replace('.', '-')
        )

        # 支持YYYY-MM-DD
        if value.isdigit() and len(value) == 8:
            return f'{value[:4]}-{value[4:6]}-{value[6:8]}'

        # 支持YYYY-MM
        if len(value) == 7 and value.count('-') == 1:
            return value + '-01'

        # 支持完整格式
        formats = {
            '%Y-%m-%d',
            '%d-%m-%Y',
            '%m-%d-%Y',
            '%Y-%d-%m',
            '%Y%m%d',
        }
        for fmt in formats:
            try:
                dt = datetime.strptime(value, fmt)
                return dt.strftime('%Y-%m-%d')
            except ValueError:
                continue
    except (ValueError, TypeError):
        return None

    return None