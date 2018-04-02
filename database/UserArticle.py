from database import BaseCursor

class UserArticle(object):
    def __init__(self):
        self.cursor = BaseCursor.BaseCursor()

    #给定目标账户的id，搜索返回其粉丝关注的所有账户的id
    def searchFollowersUcid(self, goal_ucid):

        sql = "SELECT ucid FROM weibo_user_follower WHERE follower_ucid IN " \
              "(select follower_ucid from weibo_user_follower where ucid = '%s')"

        #sql = "select follower_ucid from weibo_user_follower where ucid = '%s'"
        #allFansUcid = self.cursor.query(sql, goal_ucid)

        # res是一个只读数组嵌套只读数组，通过res[i][0]访问，存放的是int型
        res = self.cursor.query(sql, goal_ucid)
        #m = res[8][0]
        #print(type(m))
        #print(m)
        return res




if __name__ == '__main__':
    user_article = UserArticle()
    user_article.searchFollowersUcid('1880883723')