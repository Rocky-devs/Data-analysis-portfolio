import pandas as pd

def read_csv_safely(path): #参数小写
    last_err = None
    encoding_to_try = ['utf-8','utf-8-sig','gb18030']
    for enc in encoding_to_try:
        try:
            return pd.read_csv(path,encoding=enc,dtype=str)
        except UnicodeDecodeError as e:
            last_err = e

    raise last_err

