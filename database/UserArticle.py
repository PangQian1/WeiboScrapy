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
            self.updateUserArticle(mid, (data[2], data[5], data[6], data[7]))
        else:
            # 不存在，执行插入操作

            sql = "INSERT INTO weibo_user_article " \
                  "(ucid, mid, content, publish_time, publish_device, transmit, comment, praise) " \
                  "VALUES ( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"

            self.cursor.create(sql, data)

    #插入微博信息
    def updateUserArticle(self, mid, data):
        sql = "UPDATE weibo_user_article SET " \
              "content  = '%s', " \
              "transmit = '%s', " \
              "comment  = '%s', " \
              "praise   = '%s' " \
              "WHERE mid = " + mid

        self.cursor.update(sql, data)

if __name__ == '__main__':
    user_article = UserArticle()
    user_article.createUserArticle(("35446457", '123488666', '小盘此次烧开后发布', '3月6日', '苹果X',
                                    '122', '4ss44', '4546'))