from web_crawl import Database

class Fan(object):
    def __init__(self, name, sex, addr):
        self.name = name
        self.sex = sex
        self.addr = addr

    def storeInfo(self, cursor):
        # 插入数据
        sql = "INSERT INTO account (name, sex, addr) VALUES ( '%s', '%s', '%s' )"
        data = (self.name, self.sex, self.addr)
        cursor.insert(sql, data)

'''
database = Database.Database_mysql()
fan = Fan('小天', '2', '山东')
fan.storeInfo(database)
'''
