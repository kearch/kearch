n_bundle = 10

def insert_multiple_data(table,datas):
    res = list()
    index = 0
    n_data = len(datas)
    while index < n_data:
        n_insert = 0
        if index + n_bundle < n_data:
            n_insert = n_bundle
        else:
            n_insert = n_data - index
        place = ' (?'+(',?'*(len(datas[0])-1)) + ') '
        sql = 'insert into ' + table + 'values ' + place + ((','+place) * (n_insert-1))
        data = list()
        for ds in datas[index:index+n_insert]:
            for d in ds:
                data.append(d)
        res.append((sql,datas[index:index+n_insert]))
    return res
