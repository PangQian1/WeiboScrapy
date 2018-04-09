from database import BaseCursor

class UserArticle(object):
    def __init__(self):
        self.cursor = BaseCursor.BaseCursor()

    #插入微博信息
    def createUserArticle(self, data):
        mid  = data[1]
        select_sql = "select * from weibo_user_article WHERE mid = '%s'"
        res = self.cursor.query(select_sql, mid)
        if res:
            # 已经存在
            print('更新微博：' + mid)
            self.updateUserArticle(mid, (data[2], data[5], data[6], data[7]))
        else:
            # 不存在，执行插入操作
            sql = "INSERT INTO weibo_user_article " \
                  "(ucid, mid, content, publish_time, publish_device, transmit, comment, praise) " \
                  "VALUES ( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"

            self.cursor.create(sql, data)
            print('添加微博：' + data[0] + '  ' + data[1])

    #更新微博信息
    def updateUserArticle(self, mid, data):
        sql = "UPDATE weibo_user_article SET " \
              "content  = '%s', " \
              "transmit = '%s', " \
              "comment  = '%s', " \
              "praise   = '%s' " \
              "WHERE mid = " + mid

        self.cursor.update(sql, data)

    # 获取用户发布的微博
    def getUserArticle(self, ucid, offset = 0,  limit = 100):
        select_sql    = "SELECT * FROM weibo_user_article WHERE ucid = '%s' LIMIT " + str(offset) + "," + str(limit)
        user_articles = self.cursor.query(select_sql, (ucid))
        return user_articles

    # 对用户的微博分词
    def splitUserArticle(self, mid, content_split):
        sql = "UPDATE weibo_user_article SET " \
              "content_split  = '%s' " \
              "WHERE mid = " + str(mid)

        self.cursor.update(sql, (content_split))

if __name__ == '__main__':
    user_article = UserArticle()
    user_article.createUserArticle(("35446457", '123488666', '小盘此次烧开后发布', '3月6日', '苹果X',
                                    '122', '4ss44', '4546'))