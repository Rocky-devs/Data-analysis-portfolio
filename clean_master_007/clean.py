from cleaners import clean_quantity_series, clean_price_series, clean_date, clean_discount_series
from config import CLEANER_CONFIG, ID_COL, NOTE_COL, FILED_ALIASES
import pandas as pd
import sys

CLEANER_REGISTER = {
    'quantity': clean_quantity_series,
    'price': clean_price_series,
    'date': clean_date,
    'discount': clean_discount_series,
}

CSV_PATH = 'data/working/dirty_orders.csv'
OUTPUT_PATH = 'data/output/test.xlsx'


# 读 read
def read_table_safely(path):
    ext = path.lower().split('.')[-1]
    if ext == 'csv':
        encoding_to_try = ['utf-8', 'utf-8-sig', 'gb18030']
        last_err = None

        for enc in encoding_to_try:
            try:
                return pd.read_csv(path, encoding=enc, dtype=str).reset_index(drop=True)
            except UnicodeDecodeError as e:
                last_err = e

        raise last_err

    elif ext in ('xlsx', 'xls'):
        return pd.read_excel(path, dtype=str).reset_index(drop=True)

    raise ValueError(f'Unsupported file type : {ext}')


# 字段识别
def normalize_columns(df, field_aliases):
    column_map = {}
    for standard_field, aliases in field_aliases.items():
        for alias in aliases:
            for column in df.columns:
                if column.lower().strip() == alias.lower().strip():
                    column_map[standard_field] = column
                    break
    return column_map


# 洗 clean
def clean_frame(df, cleaner_config, cleaner_register, field_aliases, id_col, note_col):
    df = df.copy()
    column_map = normalize_columns(df, field_aliases)
    print('column_map:', column_map)
    print('Columns', df.columns.tolist())
    # 列级清洗 clean columns
    for field, rule in cleaner_config.items():
        real_col = column_map.get(field)
        if real_col is None:
            print(f'Skipping missing field : {field}')
            continue

        func = cleaner_register[rule]
        clean_col = f'{field}_clean'

        is_series_cleaner = func.__name__.endswith('_series')
        if is_series_cleaner:
            df[clean_col] = func(df[real_col])
        else:
            df[clean_col] = df[real_col].apply(func)

    # 结果保留 results store
    keep_cols = []
    if id_col in df.columns:
        keep_cols.append(id_col)
    if note_col in df.columns:
        keep_cols.append(note_col)

    results_df = df[keep_cols].copy()
    for field in cleaner_config:
        clean_col = f'{field}_clean'
        if clean_col in df.columns:
            results_df[field] = df[f'{field}_clean']

    # 错误统计 error frames
    error_frames = []

    for field in cleaner_config:

        real_col = column_map.get(field)
        clean_col = f'{field}_clean'

        if real_col is None or clean_col not in df.columns:
            continue

        mask = df[clean_col].isna() & df[real_col].notna()

        if mask.any():
            tmp = df.loc[mask, :].copy()
            tmp['row'] = tmp.index + 1
            tmp['field'] = field
            tmp['raw'] = tmp[real_col]

            cols_keep = ['row', 'field', 'raw']

            if id_col in tmp.columns:
                cols_keep.insert(1, id_col)

            if note_col in tmp.columns:
                cols_keep.insert(2, note_col)

            error_frames.append(tmp[cols_keep])

    if error_frames:
        error_df = pd.concat(error_frames, ignore_index=True)
    else:
        error_df = pd.DataFrame(columns=['row', id_col, 'field', 'raw'])

    # 次数统计 error summary
    summary = error_df['field'].value_counts().to_dict()

    if 'qty' in results_df.columns and 'unit_price_usd' in results_df.columns:
        discount = results_df.get('discount_rate', pd.Series(pd.NA, index=results_df.index))
        # discount转数值，转不了的就转成Nan
        discount = pd.to_numeric(discount, errors='coerce').fillna(0.0)  # 没折扣当成0折扣
        results_df['total_amount'] = (
                results_df['qty'] *
                results_df['unit_price_usd'] *
                (1 - discount)
        )
    return (
        results_df,
        error_df,
        summary,
    )


# 输出 output
def write_excel(output_path, results_df, errors_df, summary_df):
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        results_df.to_excel(writer, sheet_name='results', index=False)
        errors_df.to_excel(writer, sheet_name='errors', index=False)
        summary_df.to_excel(writer, sheet_name='summary', index=False)


def run_pipeline(input_path, output_path, cleaner_config, cleaner_register, id_col, note_col):
    # 读 read
    df = read_table_safely(input_path)

    # 洗 clean
    results_df, errors_df, summary = clean_frame(df, cleaner_config, cleaner_register, id_col, note_col)
    summary_df = (
        pd.DataFrame.from_dict(summary, orient='index', columns=['count'])
        .reset_index()
        .rename(columns={'index': 'field'}))
    # 输出 output
    write_excel(output_path, results_df, errors_df, summary_df)

    print(f'Completed output_path : {output_path}')


import os


def run_batch(folder_path, cleaner_config, cleaner_register, id_col, note_col):
    output_folder = folder_path.rstrip('/\\') + '_clean'
    os.makedirs(output_folder, exist_ok=True)

    csv_files = [
        f for f in os.listdir(folder_path)
        if f.lower().endswith(('.csv', '.xlsx', '.xls'))
    ]
    if not csv_files:
        print('No csv files found')
        return
    total = len(csv_files)

    for idx, filename in enumerate(csv_files, start=1):
        input_path = os.path.join(folder_path, filename)
        output_name = filename.rsplit('.', 1)[0] + '_clean.xlsx'
        output_path = os.path.join(output_folder, output_name)

        print(f'[{idx}/{total}] Processing: {filename}')

        run_pipeline(
            input_path,
            output_path,
            cleaner_config,
            cleaner_register,
            id_col,
            note_col
        )

    print(f'\nCompleted output folder : {output_folder}')


if __name__ == '__main__':
    input_path = sys.argv[1]
    if os.path.isdir(input_path):
        run_batch(input_path,
                  CLEANER_CONFIG,
                  CLEANER_REGISTER,
                  ID_COL,
                  NOTE_COL,
                  )
    else:
        output_path = sys.argv[2]
        run_pipeline(
            input_path,
            output_path,
            CLEANER_CONFIG,
            CLEANER_REGISTER,
            ID_COL,
            NOTE_COL,
        )
