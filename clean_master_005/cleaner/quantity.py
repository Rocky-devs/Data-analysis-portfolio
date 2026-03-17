

def clean_quantity(value):
    try:
        if value is None:
            return None
        if not isinstance(value,str):
            return value
        if value.strip() == '':
            return None

        value = value.strip().lower() #原始数据有usd之类的英文 ，统一先转小写，方便后续

        if 'pcs' in value:
            value = value.replace('pcs','').strip()

        if 'x' in value:
            left,right = value.split('x')
            return  (float(left.strip()) * float(right.strip()))

        if '>=' in value:
            value = value.replace('>=','').strip()

        if '-' in value:
            left,right = value.split('-')
            value = ((float(left.strip())) + (float(right.strip())))/2

        value = float(value)

    except (ValueError, TypeError):
        return None

    return value