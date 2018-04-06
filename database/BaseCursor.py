import pymysql.cursors

class BaseCursor(object):
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.Connect(
            host    = 'localhost',
            port    = 3306,
            user    = 'root',
            passwd  = '',
            db      = 'graduation_design',
            charset = 'utf8',
            cursorclass = pymysql.cursors.DictCursor
        )

        # 获取游标
        self.cursor = self.connect.cursor()

    #直接插入一条数据
    def create(self, sql, data):
        self.cursor.execute(sql % data)
        self.connect.commit()

    # 查询数据
    def query(self, sql, data):
        self.cursor.execute(sql % data)
        return self.cursor.fetchall()

    # 更新一条数据
    def update(self, sql, data):
        self.cursor.execute(sql % data)
        self.connect.commit()
