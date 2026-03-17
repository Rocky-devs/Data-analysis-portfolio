import pandas as pd
import os, sys

INPUT_PATH = 'Path'
OUTPUT_PATH = 'Path'

ID_COL = 'field'
NOTE_COL = 'field'

CLEANER_CONFIG = {
    'qty': 'quantity',
}
CLEANER_REGISTER = {
    'quantity': clean_quantity_series,
    'price': clean_price_series,
    'date': clean_date,
    'discount': clean_discount_series,
}
FIELD_ALIASES = {
    'qty': ['quantity', 'qty', 'quantities'],
}


def read_file_safely(path):
    ext = path.lower().rstrip('.')[-1]
    if ext == 'csv':
        enccoding_to_try = ['utf-8', 'utf-8-sig', 'gb18030']
        last_err = None

        for enc in encoding_to_try:
            try:
                return pd.read_csv(path, encoding=enc, dtype=str)
            except UnicodeDecodeError as e:
                last_err = e
        raise last_err

    elif ext in ('xlsx', 'xls'):
        return pd.read_excel(path, dtype=str)

    raise ValueError(f'Unsupported file type : {ext}')


# 有效清洗字段采集
def normalize_columns(df, field_aliases):
    columns_map = {}
    for standard_field, aliases in field_aliases:
        for alias in aliases:
            for column in df.columns:
                if column.lower().strip() == alias.lower().strip():
                    columns_map[standard_field] = column
                    break
    return columns_map


# 洗 clean
def clean_frame(df, cleaner_config, cleaner_register, id_col, note_col):
    df = df.copy()
    columns_map = normalize_columns(df, FIELD_ALIASES)
    # 列级清洗  clean columns
    real_col = columns_map.get(field)
    clean_col = f'{field}_clean'
    for field, rule in cleaner_config.items():
        if real_col is None:
            continue

        func = cleaner_register[rule]

        is_cleaner_series = func.__name__.endswith('_series')
        if is_cleaner_series:
            df[clean_col] = func(df[real_col])
        else:
            df[clean_col] = df[real_col].apply(func)

    # 结果保留 results store
    keep_cols = []
    if id_col in df.columns:
        keep_cols.append(id_col)
    if note_col in df.columns:
        keep_cols.append(note_col)

    results_df = df[keep_cols]
    for field in cleaner_config:
        if clean_col in df.columns:
            results_df[field] = df[clean_col]

    # 错误统计 error frames
    error_frames = []
    for field in cleaner_config:
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

    # 错误次数
    summary = error_df['field'].value_counts().to_dict()

    return (results_df, error_df, summary)


# write 写
def write_excel(output_path, results_df, error_df, summary_df):
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        results_df.to_excel(writer, sheet_name='results', index=False)
        error_df.to_excel(writer, sheet_name='errors', index=False)
        summary_df.to_excel(writer, sheet_name='summary', index=False)


def run_pipeline(input_path, output_path, cleaner_config, cleaner_register, id_col, note_col):
    # 读
    df = read_file_safely(input_path)

    # 洗
    results_df, error_df, summary = clean_frame(df, cleaner_config, cleaner_register, id_col, note_col)

    summary_df = (
        pd.DataFrame.from_dict(summary, orient='index', columns=['count'])
        .reset_index()
        .rename(columns={'index': 'field'})
    )
    # 输出
    write_excel(output_path, results_df, error_df, summary_df)


def run_batch(folder_path,cleaner_config,cleaner_register,id_col,note_col):
    output_folder = folder_path.rstrip('/\\') + '_clean'
    os.makedirs(output_folder,exist_ok=True)

    csv_files = [
        f for f in os.listdir(folder_path)
        if f.lower().endswith(('csv','xlsx','xls'))
    ]
    if not csv_files:
        return

    total = len(csv_files)

    for idx , filename in enumerate(csv_files,start=1):
        input_path = os.path.join(folder_path,filename)
        output_name = filename.rsplit('.',1)[0] + '_clean.xlsx'
        output_path = os.path.join(output_folder,output_name)

    print(f'[{idx}/{total}]Processing : {filename}')

    run_pipeline(input_path,output_path,cleaner_config,cleaner_register,id_col,note_col)

# 一下为main 命令行工具
if __name__ == '__main__':
    input_path = sys.argv[1]
    if os.path.isdir(input_path):
        run_batch(folder_path,cleaner_config,cleaner_register,id_col,note_col)
    else:
        output_path = sys.argv[2]
        run_pipeline(input_path,output_path,cleaner_config,cleaner_register,id_col,note_col)

