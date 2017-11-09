n_bundle = 1000

def insert_multiple_data(table,datas,cur):
    index = 0
    n_data = len(datas)
    while index < n_data:
        n_insert = 0
        if index + n_bundle < n_data:
            n_insert = n_bundle
        else:
            n_insert = n_data - index
        place = ' (?'+(',?'*(len(datas[0])-1)) + ') '
        sql = 'insert into ' + table + ' values ' + place + ((','+place) * (n_insert-1))
        data = list()
        for i in range(index,index+n_insert):
            for d in datas[i]:
                data.append(d)
        cur.execute(sql,data)
        index += n_insert
