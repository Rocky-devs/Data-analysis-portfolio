import pandas as pd
from config import CLEANER_REGISTER
def clean_frame(df,cleaner_config,id_col,note_col):
    df = df.copy()
    # 列级清洗 clean columns
    for field , rule in cleaner_config.items():
        func = CLEANER_REGISTER[rule]
        df[f'{field}_clean'] = df[field].apply(func)

    # 结果保存 results store
    results_df = df[[id_col,note_col]].copy()
    for field in cleaner_config:
        results_df[field] = df[f'{field}_clean']

    # 错误统计 error_frames
    error_frames = []
    for field in cleaner_config:
        mask = df[f'{field}_clean'].isna() & df[field].notna()
        if mask.any():
            tmp = df.loc[mask,[id_col,field]].copy()
            tmp['row'] = tmp.index + 1
            tmp['field'] = field
            tmp['raw'] = tmp[field]
            error_frames.append(tmp[['row',id_col,'field','raw']])

    if error_frames:
        error_df = pd.concat(error_frames,ignore_index=True)
    else:
        error_df = pd.DataFrame(columns=['row',id_col,'field','raw',])

    # 错误次数 error_summary
    summary = error_df['field'].value_counts().to_dict()

    return (
        results_df,
        error_df,
        summary,
    )
