

def run_batch_pipeline_recursive(folder_path, cleaner_config, cleaner_register, id_col, note_col):
    # 创建输出文件夹
    output_folder = folder_path.rstrip('/\\') + '_clean'

    os.makedirs(output_folder,exist_ok=True) #已取消if not exists判断，直接创建，exist_ok 为flag，预计方便后续扩展

    # 收集所有子目录csv
    csv_files = []
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.lower().endswith('.csv'):
                full_path = os.path.join(root, filename)
                csv_files.append(full_path)
    total = len(csv_files)
    if total == 0:
        print('No CSV files found')
        return # 等价于return None 这里不return也会继续往下执行，但是可能会浪费性能

    # 开始处理
    for index , input_path in enumerate(csv_files,start=1):
        filename = os.path.basename(input_path)
        output_name = filename.replace('.csv','_clean.xlsx')
        output_path = os.path.join(output_folder,output_name)

        print(f'[{index}/{total}] Processing : {filename}')

        run_pipeline(
            input_path,
            output_path,
            cleaner_config,
            cleaner_register,
            id_col,
            note_col,
        )

    print(f'\nCompleted. Output folder : {output_folder}')




import sys
import os

if __name__ == '__main__':

    if len(sys.argv) < 3:
        print('Usage : python3 test001.py input.cs output.xlsx')
        print('Usage : python3 foler_path output_folder')
        sys.exit(1)

    input_path = sys.argv[1]

    recursive = '--recursive' in sys.argv

    if os.path.isdir(input_path):

        if recursive:
            run_batch_pipeline_recursive(
                input_path,
                CLEANER_CONFIG,
                CLEANER_REGISTER,
                ID_COL,
                NOTE_COL,
            )
        else:
            run_batch_pipeline(
                input_path,
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