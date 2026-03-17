import pandas as pd

def clean_price(value): # 一般类似replace这样的不用if，不然冗余，split之类的可以
    try:
        if value is None:
            return None
        if not isinstance(value, str):
            return None
        if value.strip() == '':
            return None

        value = value.strip().lower()

        value = value.replace(',','')
        value = value.replace('$', '')
        value = value.replace('€', '')
        value = value.replace('≈', '')
        value = value.replace('usd', '')

        value = value.strip()

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

        value = value.replace('pcs', '')
        value = value.replace('>=', '')
        value = value.replace('units','')
        value = value.replace('unit','')
        value = value.replace('approx','')

        value = value.strip()

        if 'x' in value:
            left, right = value.split('x')
            return (float(left.strip()) * float(right.strip()))

        if '-' in value:
            left, right = value.split('-')
            value = ((float(left.strip())) + (float(right.strip()))) / 2

        value = float(value)

    except (ValueError, TypeError):
        return None

    return value

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
        if not isinstance(value,str):
            return None
        value = value.strip().lower()
        if value == '':
            return None

        if value.endswith('%'):
            return float(value.replace('%','')) / 100

        return float(value)
    except(ValueError, TypeError):
        return None

import csv
import json


def read_csv_safely(path: str) -> pd.DataFrame:
    encodings_to_try = ['utf-8', 'utf-8-sig', 'gb18030']
    # 第一种最常见，第二种主要针对excel（带bom），第三种主要是中文，windows常见编码
    last_err = None
    for enc in encodings_to_try:  # 每次从这个列表里边提取一种编码形式去读取文件
        try:
            df = pd.read_csv(
                path,
                encoding=enc,  # 没次一种编码尝试
                dtype=str,  # 把数据全部当成str能够避开乱码和隐式类型
            )
            return df
        except UnicodeDecodeError as e:
            last_err = e

    raise last_err  # for循环完毕如果三种都失败就证明有异常，except接住了，然后这里循环结束后直接抛出捕获的异常


def clean_dataframe(
        df: pd.DataFrame,
        CLEANER: dict,
        ID_COL: str,
        NOTE_COL: str,
):
    df = df.copy()

    # A 列级清洗
    for field, rule_name in CLEANER_CONFIG.items():
        func= CLEANER_REGISTER[rule_name]
        df[f'{field}_clean'] = df[field].apply(func)

    # B 错误行标记
    error_flags = []
    for field in CLEANER:
        flag = df[f'{field}_clean'].isna() & df[field].notna()
        error_flags.append(flag)

    df['has_error'] = False
    for flag in error_flags:
        df['has_error'] |= flag

    # C 结果保留nan，不要让整行因为某个field是nan或者有错就被抛弃
    result_df = df[[ID_COL, NOTE_COL]].copy()  # 类似于原生python的new_row即要保留的不变/不清洗的字段
    for field in CLEANER:
        result_df[field] = df[f'{field}_clean']

    # D 错误明细表
    error_frames = []
    for field in CLEANER:
        mask = df[f'{field}_clean'].isna() & df[field].notna()
        if mask.any():
            tmp = df.loc[mask, [ID_COL, field]].copy()
            tmp['row'] = tmp.index
            tmp['field'] = field
            tmp['raw'] = tmp[field]
            error_frames.append(tmp[['row', ID_COL, 'field', 'raw']])

    errors_df = (
        pd.concat(error_frames, ignore_index=True)
        if error_frames
        else pd.DataFrame(columns=['row', ID_COL, 'field', 'raw'])
    )

    # E 错误汇总
    error_summary = errors_df['field'].value_counts().to_dict()

    return (
        result_df, #如果这里用了to_dict将返回值变成字典，下边就要result_df.pd.DataFrame
        errors_df,
        error_summary,
    )


# 1 读数据
CSV_PATH = 'data_d5.csv'

ID_COL = 'order_id'
NOTE_COL = 'comment'

# 2 清洗规则表
CLEANER_CONFIG = {
    'qty_text': 'quantity',
    'unit_cost': 'price',
    'order_date': 'date',
    'discount':'discount',
    'shipping_fee':'price',
}
CLEANER_REGISTER = {
    'quantity': clean_quantity,
    'price': clean_price,
    'date': clean_date,
    'discount':clean_discount,
}
df = read_csv_safely(CSV_PATH)

results, errors, summary = clean_dataframe(df, CLEANER_CONFIG, ID_COL, NOTE_COL)

results_df = results
errors_df = errors
summary_df = (
    pd.DataFrame.from_dict(summary, orient='index', columns=['count'])
    .reset_index()
    .rename(columns={'index': 'field'})
)

from xlsxwriter import Workbook

output_path = 'clean_output.xlsx'
with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
    results_df.to_excel(writer, sheet_name='results', index=False)
    errors_df.to_excel(writer, sheet_name='errors', index=False)
    summary_df.to_excel(writer, sheet_name='summary', index=False)
    # 1 下列代码块为提升用户体验，冻结首行（滚动操作时fieldname不会消失），主要要再with代码块内，不然with结束文件关闭，无法操作
    workbook = writer.book
    worksheet = writer.sheets['results']
    worksheet.freeze_panes(1, 0)
    # 2 自动列宽，不让数据挤成一坨/算最长字符串，根据最长字符串设置固定列宽
    for col_idx, col_name in enumerate(results_df.columns):
        max_len = max(
            results_df[col_name].astype(str).map(len).max(),
            len(col_name),
        )  # 算长度
        worksheet.set_column(col_idx, col_idx, max_len + 2)  # 设列宽
    # 3 轻微高亮（此处仅为提升客户体验上限）当前范例仅对errors操作
    errors_ws = writer.sheets['errors']
    red_format = workbook.add_format({
        'font_color': 'red',
    })
    errors_ws.set_column('A:D', 20)
    errors_ws.freeze_panes(1, 0)  # 冻结首行
    errors_ws.set_row(0, None, red_format)

print(output_path)
