from database import BaseCursor

class UserInfo(object):

    # def __init__(self, ucid, name, sex, address, birthday, introduction):
    #     self.ucid = ucid
    #     self.name = name
    #     self.sex  = sex
    #     self.address      = address
    #     self.birthday     = birthday
    #     self.introduction = introduction

    def __init__(self):
        self.cursor = BaseCursor.BaseCursor()

    # 插入一条用户信息
    def createUserInfo(self, data):
        # 插入数据,首先检查数据是否存在，不存在执行插入，存在执行更新

        ucid = data[0]
        select_sql = "select * from weibo_user_info WHERE ucid = '%s'"
        res = self.cursor.query(select_sql, ucid)
        if res:
            # 已经存在
            self.updateUserInfo(ucid, (data[1], data[2], data[3], data[4], data[5]))
        else:
            # 不存在，执行插入操作

            sql = "INSERT INTO weibo_user_info (ucid, name, sex, address, birthday, introduction, keywords) " \
                  "VALUES ( '%s', '%s', '%s', '%s', '%s', '%s', '')"

            # data = (self.ucid, self.name, self.sex, self.address, self.birthday, self.introduction)
            self.cursor.create(sql, data)

    # 更新部分用户信息
    def updateUserInfo(self, ucid, data):

        sql = "UPDATE weibo_user_info SET " \
              "name = '%s', " \
              "sex = '%s', " \
              "address = '%s', " \
              "birthday = '%s', " \
              "introduction = '%s'" \
              "WHERE ucid = " + ucid

        self.cursor.update(sql, data)

    # 获取用户个人信息
    def getUserInfoByUcid(self, ucids, fields = []):
        ucid_list = ','.join(ucids)
        print(ucid_list)

        if fields :
            fileds = ',' . join(fields)
        else :
            fileds = '*'

        sql = "SELECT " + str(fields) + " FROM weibo_user_info WHERE UCID IN (%s)"
        res = self.cursor.query(sql, (ucid_list))
        return res

    # 获取用户信息列表
    def getUserInfoList(self, fields, offset = 0, limit = 10):
        params = '*'
        if len(fields):
            params = ',' . join(fields)

        sql = "SELECT " + str(params) + " FROM weibo_user_info ORDER BY id DESC LIMIT " + str(offset) + "," + str(limit)
        res = self.cursor.query(sql, ())
        return res

    # 执行sql
    def executeSql(self, sql, data):

        self.cursor.update(sql, data)

if __name__ == "__main__":
    user_info = UserInfo()
    data = ('75927596297', '小32', 'F', '青岛', '3月1号', "胖子一个")
    # user_info.updateUserInfo('18677654377', data)
    # a = user_info.getUserInfo(['18677654377','18677754377'])
    user_info.createUserInfo(data)

