import pandas as pd

def write_excel(path,result_df,error_df,summary):
    summary_df = (
        pd.DataFrame.from_dict(summary,orient='index',columns=['count'])
        .reset_index()
        .rename(columns={'index':'field'})
    )
    with pd.ExcelWriter(path, engine='xlsxwriter') as writer:
        result_df.to_excel(writer, sheet_name='results', index=False)
        error_df.to_excel(writer, sheet_name='errors', index=False)
        summary_df.to_excel(writer, sheet_name='summary', index=False)
        # 1 下列代码块为提升用户体验，冻结首行（滚动操作时fieldname不会消失），主要要再with代码块内，不然with结束文件关闭，无法操作
        workbook = writer.book
        worksheet = writer.sheets['results']
        worksheet.freeze_panes(1, 0)
        # 2 自动列宽，不让数据挤成一坨/算最长字符串，根据最长字符串设置固定列宽
        for col_idx, col_name in enumerate(result_df.columns):
            max_len = max(
                result_df[col_name].astype(str).map(len).max(),
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