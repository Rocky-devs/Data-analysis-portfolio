from cleaners import clean_quantity, clean_price, clean_date, clean_discount

CSV_PATH = 'client_orders_dirty.csv'
OUTPUT_PATH = 'cleaned.xlsx'
ID_COL = 'order_id'
NOTE_COL = 'customer_name'


CLEANER_CONFIG = {
    'qty': 'quantity',
    'unit_price_usd': 'price',
    'order_date': 'date',
    'discount_rate': 'discount',
    'shipping_cost': 'price',
}
CLEANER_REGISTER = {
    'quantity': clean_quantity,
    'price': clean_price,
    'date': clean_date,
    'discount': clean_discount,
}
