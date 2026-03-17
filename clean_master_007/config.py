ID_COL = 'order_id'
NOTE_COL = 'customer_name'

CLEANER_CONFIG = {
    'qty': 'quantity',
    'unit_price_usd': 'price',
    'order_date': 'date',
    'discount_rate': 'discount',
}

FILED_ALIASES = {
    'qty': [
        'qty',
        'quantity',
        'qty order',
        'order_qty',
        '数量',
    ],

    'unit_price_usd': [
        'unit_price_usd',
        'price',
        'unit price',
        'unit price usd',
        'price_raw',
        '单价',
    ],

    'discount_rate': [
        'discount_rate',
        'discount',
        'discount %',
        '折扣',
    ],
    'order_date': [
        'order_date',
        'date',
        'order date',
        '日期',
    ],
}
