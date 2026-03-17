def clean_price(value):
    try:
        if value is None:
            return None
        if not isinstance(value,str):
            return None
        if value.strip() == '':
            return None

        value = value.strip().lower()
        if '$' in value:
            value = value.replace('$','')

        if '€' in value:
            value = value.replace('€','')

        if '≈' in value:
            value = value.replace('≈','')

        if 'usd' in value:
            value = value.replace('usd','')

        if '-' in value:
            left,right =  value.split('-')
            value = (float(left.strip()) + float(right.strip()))/2

        value = float(value)
    except (ValueError, TypeError):
        return None

    return value
