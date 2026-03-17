
def clean_stock(value):
    try:
        if value is None:
            return None
        if not isinstance(value,str):
            return None
        if value.strip() =='':
            return None

        value = value.strip().lower() #先转小写，后续不必在意大小写

        None_keys = {'unknown','error','',} #前边已经‘’了，这里集合内不需要‘’，虽然不错，但是冗余
        if value in None_keys:
            return None

        in_stock_keys = {'yes','y','true','1',}#这是集合，其中元素貌似具有唯一性，比较符合本题目标，不应该用列表，因为列表有排序且可以重复
        if value in in_stock_keys:
            return 'in_stock'

        out_stock_keys = {'no','n','false','0',} #最后一个元素后边都加个comma，方便以后扩展，反正不报错
        if value in out_stock_keys:
            return 'out_of_stock'

    except Exception as e:#纯粹瞎记，不知道用什么错误类型，也不知道用什么兜底
        return None

    return None