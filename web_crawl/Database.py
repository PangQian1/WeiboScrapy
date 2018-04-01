import pymysql.cursors

class Database_mysql(object):
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.Connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='',
            db='graduation_design',
            charset='utf8'
        )

        # 获取游标
        self.cursor = self.connect.cursor()

    #直接插入一条数据
    def insert(self, sql, data):
        self.cursor.execute(sql % data)
        self.connect.commit()

    #在relationship表中插入一条数据，如果该账户已经存在过，置fan项加一
    def insertIntoRela(self, accID, nickname):

        sql = "select * from relationship WHERE name = '%s'"
        self.cursor.execute(sql % nickname)
        #print(self.cursor.rowcount)
        if self.cursor.rowcount == 1:
            # 本身存在记录，则fan加1即可
            num = self.cursor.fetchone()[3]
            num = num + 1
            sql1 = "update relationship set fan = %d where name = '%s'"
            data = (num, nickname)
            self.cursor.execute(sql1 % data)
        elif self.cursor.rowcount == 0:
            # 说明本身并不存在记录，则进行插入
            sql2 = "insert into relationship (accountID, name, fan) values ('%s', '%s', %d)"
            data = (accID, nickname, 1)
            self.cursor.execute(sql2 % data)
            #print(sql2 % data)
            #print(self.cursor.rowcount)
        else:
            #出现异常
            print('relationship表更新出现异常！')

        self.connect.commit()

    #从数据库中取出所需账户的ID，之后会利用ID进行搜索，爬取他们的微博，存储到数据库中
    def get_AccountID(self):
        sql = "select accountID from relationship"
        res = self.cursor.execute(sql)
        return res