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


import pandas as pd


# 读 read
def read_csv_safely(path):
    last_err = None
    encoding_to_try = ['utf-8', 'utf-8-sig', 'gb18030']
    for enc in encoding_to_try:
        try:
            return pd.read_csv(path, encoding=enc, dtype=str)
        except UnicodeDecodeError as e:
            last_err = e

    raise last_err


# 配置 config
PATH = 'client_orders_dirty.csv'

ID_COL = 'order_id'
NOTE_COL = 'customer_name'

CLEANER_CONFIG = {
    'qty': 'quantity',
    'order_date': 'date',
    'discount_rate': 'discount',
    'unit_price_usd': 'price',
    'shipping_cost': 'price',
}
CLEANER_REGISTER = {
    'quantity': clean_quantity,
    'date': clean_date,
    'discount': clean_discount,
    'price': clean_price,
}

# 洗 clean
df = read_csv_safely(path=PATH)

def clean_frame(df,cleaner_config,id_col,note_col):
    df = df.copy()
    # 列级清洗 columns clean
    for field, rule in CLEANER_CONFIG.items():
        func = CLEANER_REGISTER[rule]
        df[f'{field}_clean'] = df[field].apply(func)

    # 结果保存 results store
    results_df = df[[ID_COL,NOTE_COL]].copy()
    for field in CLEANER_CONFIG:
        results_df[field] = df[f'{field}_clean']

    # 错误统计 error_frames
    error_frames = []
    for field in CLEANER_CONFIG:
        mask = df[f'{field}_clean'].isna() & df[field].notna()
        if mask.any():
            tmp = df.loc[mask,[ID_COL,field]].copy()
            tmp['row'] = tmp.index + 1
            tmp['field'] = field
            tmp['raw'] = tmp[field]
            error_frames.append(tmp[['row',ID_COL,'field','raw']])
    if error_frames:
        error_df = pd.concat(error_frames,ignore_index=True)
    else:
        error_df = pd.DataFrame(columns=['row',ID_COL,'field','raw',])

    # 错误次数 error_count
    summary = error_df['field'].value_counts().to_dict()

    return (
        results_df,
        error_df,
        summary,
    )

# 输出 output
results_df,error_df,summary = clean_frame(df,CLEANER_CONFIG,ID_COL,NOTE_COL)
summary_df = (
    pd.DataFrame.from_dict(summary,orient='index',columns=['count'])
    .reset_index()
    .rename(columns={'index':'field'})
)
output = 'clean_output.xlsx'
with pd.ExcelWriter(output,engine='xlsxwriter') as writer:
    results_df.to_excel(writer,sheet_name='results',index=False)
    error_df.to_excel(writer,sheet_name='errors',index=False)
    summary_df.to_excel(writer,sheet_name='summary',index=False)
