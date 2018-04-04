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

    #给定目标账户的id，搜索返回其粉丝关注的所有账户的id
    def searchFollowersUcid(self, goal_ucid):

        sql = "SELECT DISTINCT ucid FROM weibo_user_follower WHERE follower_ucid IN " \
              "(select follower_ucid from weibo_user_follower where ucid = '%s')"

        #sql = "select follower_ucid from weibo_user_follower where ucid = '%s'"
        #allFansUcid = self.cursor.query(sql, goal_ucid)

        # res是一个只读数组嵌套只读数组，通过res[i][0]访问，存放的是int型
        result = self.cursor.query(sql, goal_ucid)
        ucid_list = []
        for value in result:
             ucid_list.append(str(value[0]))

        return ucid_list

if __name__ == "__main__":
    a = UserFollowers()
    b = a.searchFollowersUcid('1880883723')
    print(b)




