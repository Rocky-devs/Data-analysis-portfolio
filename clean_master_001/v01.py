raw_values = ["10 pcs","5pcs","3 x 4","20-30 pcs","50%",">=100 pcs","",None, "abc",]
"""
规则越“具体”，越应该放前面
规则越“宽泛”，越应该放后面
'x' → 很具体
'%' → 很具体
'pcs' → 非常宽泛（很多字符串都有）
"""

def clean_value(value):
        try:
            if value is None:
                return None

            elif  not isinstance(value,str):
                return None

            elif value.strip() == '':
                return None

            elif 'x' in value:
                left,right = value.split('x')
                value = float(left.strip()) * float(right.strip())

            elif '-' in value:
                value = value.replace('pcs','').strip()
                left,right = value.split('-')
                value = (float(left.strip()) + float(right.strip()))/2

            elif '%' in value:
                value = value.replace('%','').strip()
                value = float(value.strip())/100

            elif ('>=' in value) and ('pcs' in value):
                value = value.replace('>=','').replace('pcs','').strip()

            elif 'pcs' in value:
                value = value.replace('pcs','').strip()


            value = float(value)
        except (ValueError,TypeError):
            return None

        return value

for v in raw_values:
    result = clean_value(v)
    print(result)
