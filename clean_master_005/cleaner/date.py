def clean_date(value):
    try:
        if value is None:
            return None
        if not isinstance(value,str):
            return None
        if value.strip() =='':
            return None

        value = value.strip().lower() #防御性写法，针对强否定，未验证是否报错

        None_keys = {'unknown','error'}
        if value in None_keys:
            return None

        if '/' in value:
            value = value.replace('/','-').strip()

        if '.' in value:
            value = value.replace('.','-').strip()
        #至此格式转换完毕，开始考虑按年-月-日 排序
        parts = value.split('-') #此时parts还是个包（年-月-日）
        if len(parts) != 3:
            return None
        #拆分，排序
        a,b,c = parts #二次拆包

        if len(a) == 4:
            year,month,day = a,b,c
        elif len(c) ==4:
            year,month,day = c,b,a
        else:
            return None
        #合法性判断
        year,month,day = int(year),int(month),int(day)
        if month < 1 or month > 12:
            return None
        if day < 1 or day > 31:
            return None

    except (ValueError,TypeError): #纯粹感觉 except应该接住点什么
        return None

    return f'{year:04d}-{month:02d}-{day:02d}'
