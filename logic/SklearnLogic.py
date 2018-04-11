import time
import codecs
from logic import BaseLogic
from database import UserArticle
from database import UserFollowers
from sklearn import feature_extraction
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

'''
计算词项在向量中的权重方法——TF-IDF
它表示TF（词频）和IDF（倒文档频率）的乘积：

其中TF表示某个关键词出现的频率，IDF为所有文档的数目除以包含该词语的文档数目的对数值。
 
|D|表示所有文档的数目，|w∈d|表示包含词语w的文档数目。
最后TF-IDF计算权重越大表示该词条对这个文本的重要性越大，它的目的是去除一些"的、了、等"出现频率较高的常用词。

Python简单实现基于VSM的余弦相似度计算
https://blog.csdn.net/eastmount/article/details/49898133
'''

class SklearnLogic(BaseLogic.BaseLogic):

    '''''
    sklearn里面的TF-IDF主要用到了两个函数：
        CountVectorizer()  TfidfTransformer()。
        CountVectorizer 是通过 fit_transform 函数将文本中的词语转换为词频矩阵。
        矩阵元素 weight[i][j] 表示j词在第i个文本下的词频，即各个词语出现的次数。
        通过 get_feature_names()可看到所有文本的关键字，通过 toarray() 可看到词频矩阵的结果。
        TfidfTransformer也有个 fit_transform 函数，它的作用是计算 tf-idf 值。
    '''

    #给定一个ucid，返回该用户发布的所有分词后的微博
    def getAllArticles(self, ucid):

        content = ''

        user_article = UserArticle.UserArticle()

        limit = 100
        offset = 0

        while (True):
            articles = user_article.getUserArticle(ucid, offset, limit)

            offset += limit

            if not articles:
                break

            for article in articles:
                # print(article)
                #中间要以空格隔开
                content = content + ' ' + article['content_split']

        #print(content)
        return content

    #生成待处理的文档，其中ucid_list为用户id列表，corpus为对应的每个用户发布的所有经过空格分割的分词后的微博
    def generateDocument(self, ucid, ucid_list, corpus):

        user_followers = UserFollowers.UserFollowers()
        ucid_list_original = user_followers.searchFollowersUcid(ucid)

        for ulo in ucid_list_original:
            res = self.getAllArticles(ulo)
            if res != '':
                ucid_list.append(ulo)
                corpus.append(res)


    #计算tfidf
    def calculateTFIDF(self, ucid):

        ucid_list = []  # 用户列表
        corpus = []  # 文档预料 空格连接

        self.generateDocument(ucid, ucid_list, corpus)

        print(len(ucid_list))
        print(len(corpus))

        # 将文本中的词语转换为词频矩阵 矩阵元素a[i][j] 表示j词在i类文本下的词频
        vectorizer = CountVectorizer()

        # 该类会统计每个词语的tf-idf权值
        transformer = TfidfTransformer()

        # 第一个fit_transform是计算tf-idf 第二个fit_transform是将文本转为词频矩阵
        tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))

        # 获取词袋模型中的所有词语
        word = vectorizer.get_feature_names()

        # 将tf-idf矩阵抽取出来，元素w[i][j]表示j词在i类文本中的tf-idf权重
        weight = tfidf.toarray()
        '''
        resName = "result.txt"
        result  = codecs.open(resName, 'w', 'utf-8')
        for j in range(len(word)):
            result.write(word[j] + ' ')
        result.write('\r\n\r\n')

        # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for遍历某一类文本下的词语权重
        for i in range(len(weight)):
            print(u"-------这里输出第", i, u"类文本的词语tf-idf权重------")

            for j in range(len(word)):
                result.write(str(weight[i][j]) + ' ')
            result.write('\r\n\r\n')

        result.close()
        '''
        return weight

    # K-means聚类
    def getKmeans(self, weight):
        print('Start Kmeans:')
        clf = KMeans(n_clusters = 5)
        s   = clf.fit(weight)
        print(s)

        # 20个中心点
        print(clf.cluster_centers_)

        # 每个样本所属的簇
        print(clf.labels_)
        i = 1
        while i <= len(clf.labels_):
            print(i, clf.labels_[i - 1])

            i = i + 1

        # 用来评估簇的个数是否合适，距离越小说明簇分的越好，选取临界点的簇个数
        print(clf.inertia_)

    def test(self):
            corpus = []  # 文档预料 空格连接

            # 读取预料 一行预料为一个文档
            for line in open('BaiduSpider_Result.txt', 'r').readlines():
                print(line)
                corpus.append(line.strip())
            # print corpus
            time.sleep(5)

            # 将文本中的词语转换为词频矩阵 矩阵元素a[i][j] 表示j词在i类文本下的词频
            vectorizer = CountVectorizer()

            # 该类会统计每个词语的tf-idf权值
            transformer = TfidfTransformer()

            # 第一个fit_transform是计算tf-idf 第二个fit_transform是将文本转为词频矩阵
            tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))

            # 获取词袋模型中的所有词语
            word = vectorizer.get_feature_names()

            # 将tf-idf矩阵抽取出来，元素w[i][j]表示j词在i类文本中的tf-idf权重
            weight = tfidf.toarray()

            resName = "BaiduTfidf_Result.txt"
            result = codecs.open(resName, 'w', 'utf-8')
            for j in range(len(word)):
                result.write(word[j] + ' ')
            result.write('\r\n\r\n')

            # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
            for i in range(len(weight)):
                print (u"-------这里输出第", i, u"类文本的词语tf-idf权重------")

                for j in range(len(word)):
                    result.write(str(weight[i][j]) + ' ')
                result.write('\r\n\r\n')

            result.close()


if __name__ == '__main__':
    a = SklearnLogic()
    #weight = a.getTFIDF('1768305123')
    #a.getKmeans(weight)

    weight = a.calculateTFIDF('1821058982')
    a.getKmeans(weight)