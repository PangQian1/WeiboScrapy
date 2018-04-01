from database import BaseCursor

class UserFollowers(object):

    def __init__(self):
        self.cursor = BaseCursor.BaseCursor()

    #插入一条用户信息
    def createUserFollower(self, data):
        # 插入数据,首先检查数据是否存在，不存在执行插入，存在pass

        select_sql = "select * from weibo_user_follower WHERE ucid = '%s' and follower_ucid = '%s'"
        res  = self.cursor.query(select_sql, data)
        if res:
            #已经存在
            pass
        else:
            #不存在，执行插入操作

            sql  = "INSERT INTO weibo_user_follower (ucid, follower_ucid) " \
                   "VALUES ('%s', '%s')"

            self.cursor.create(sql, data)


if __name__ == "__main__":
    a = UserFollowers()
    a.createUserFollower(('12415', '34576788'))
    a.createUserFollower(('12415', '34576788'))
    a.createUserFollower(('124154546', '34576788'))





