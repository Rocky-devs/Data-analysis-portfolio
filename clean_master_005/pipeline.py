from .cleaner.price import clean_price
from .cleaner.date import clean_date
from .cleaner.quantity import clean_quantity
import csv

CLEANER = {
    'quantity': clean_quantity,
    'price': clean_price,
    'date': clean_date,
}


def process_row(row):
    new_row = {
        'uid': row['uid']
    }  # 这个字典里都是需要原封不动保留的字段，并且在清洗后的结果中靠前，第二个for清洗后的字段排在这个字典之后

    for field, cleaner in CLEANER.items():
        raw = row.get(field)  # 让row自己通过。get方法去获取列名并赋值给raw
        if raw is None:
            print(f'[MISS] field not found or empty -> {field}')
            continue
        cleaned = cleaner(raw)

        if cleaned is None:
            print(f'[FAIL] cleaner return None -> {field} | raw={raw}')

        new_row[field] = cleaned #这套应该是在清洗之前加规则，好及时确认是raw原数据的问题还是cleaned以后的数据问题。

    return new_row