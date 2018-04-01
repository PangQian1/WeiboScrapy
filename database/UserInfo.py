from database import BaseCursor

class UserInfo(object):

    # def __init__(self, ucid, name, sex, address, birthday, introduction):
    #     self.ucid = ucid
    #     self.name = name
    #     self.sex  = sex
    #     self.address      = address
    #     self.birthday     = birthday
    #     self.introduction = introduction

    def createUserInfo(self, cursor, data):
        # 插入数据
        sql  = "INSERT INTO weibo_user_info (ucid, name, sex, address, birthday, introduction) " \
               "VALUES ( '%s', '%s', '%s', '%s', '%s', '%s')"

        # data = (self.ucid, self.name, self.sex, self.address, self.birthday, self.introduction)
        cursor.create(sql, data)

    def updateUserInfo(self, cursor, ucid, data):

        sql = "UPDATE weibo_user_info SET " \
              "name = '%s', " \
              "sex = '%s', " \
              "address = '%s', " \
              "birthday = '%s', " \
              "introduction = '%s'" \
              "WHERE ucid = " + ucid

        cursor.update(sql, data)

    def getUserInfo(self, cursor, ucids):

        ucid_list = ',' . join(ucids)

        sql = "SELECT * FROM weibo_user_info WHERE UCID IN (%s)"
        return cursor.query(sql, (ucid_list))


if __name__ == "__main__":
    cursor = BaseCursor.BaseCursor()
    user_info = UserInfo()
    data = ('小天22', 'F', '山东', '3月1号', "胖子一个")
    user_info.updateUserInfo(cursor, '18677654377', data)





