import jieba
import jieba.analyse
from logic import BaseLogic
from database import UserArticle
from database import UserFollowers
'''
结巴中文分词涉及到的算法包括：
        (1) 基于Trie树结构实现高效的词图扫描，生成句子中汉字所有可能成词情况所构成的有向无环图（DAG)；
        (2) 采用了动态规划查找最大概率路径, 找出基于词频的最大切分组合；
        (3) 对于未登录词，采用了基于汉字成词能力的HMM模型，使用了Viterbi算法。

        结巴中文分词支持的三种分词模式包括：
        (1) 精确模式：试图将句子最精确地切开，适合文本分析；
        (2) 全模式：把句子中所有的可以成词的词语都扫描出来, 速度非常快，但是不能解决歧义问题；
        (3) 搜索引擎模式：在精确模式的基础上，对长词再次切分，提高召回率，适合用于搜索引擎分词。
'''
class AnalysisLogic(BaseLogic.BaseLogic):

    # 对用户的微博进行分词
    def splitArticle(self, ucid):

        limit  = 10
        offset = 0
        user_article = UserArticle.UserArticle()
        while (True) :

            articles = user_article.getUserArticle(ucid, offset, limit)
            offset   += limit
            #print(offset)
            if not articles :
                break

            for article in articles:
                #print(article)
                # 默认的分词模式
                seg_list = jieba.cut(article['content'], cut_all = False)

                content_split = " " . join(seg_list)

                user_article.splitUserArticle(article['mid'], content_split)

                #print(u"[默认模式]: ", "/ ".join(seg_list))


    def test(self):
        # 全模式
        text = "我来到北京,高兴~~去了清华大学"
        seg_list = jieba.cut(text, cut_all = True)
        print ("," . join(seg_list))

        print (u"[全模式]: ", "/ " . join(seg_list))

        # 精确模式
        seg_list = jieba.cut(text, cut_all=False)
        print (u"[精确模式]: ", "/ ".join(seg_list))

        # 默认是精确模式
        seg_list = jieba.cut(text)
        print (u"[默认模式]: ", "/ ".join(seg_list))


        # 新词识别 “杭研”并没有在词典中,但是也被Viterbi算法识别出来了
        seg_list = jieba.cut("他来到了网易杭研大厦")
        print (u"[新词识别]: ", "/ ".join(seg_list))


        # 搜索引擎模式
        seg_list = jieba.cut_for_search(text)
        print (u"[搜索引擎模式]: ", "/ ".join(seg_list))

        # 精确模式
        text = "故宫的著名景点包括乾清宫、太和殿和午门等。其中乾清宫非常精美，午门是紫禁城的正门，午门居中向阳。"
        seg_list = jieba.cut(text, cut_all=False)
        print( u"分词结果:")

        print("/".join(seg_list))

        # 获取关键词
        tags = jieba.analyse.extract_tags(text, topK=3)
        print(u"关键词:")

        print(" ".join(tags))

if __name__ == '__main__':
    a = AnalysisLogic()
    a.splitArticle('5359730794')
    #a.test()
    input('test')

    user_followers = UserFollowers.UserFollowers()
    ucid_list = user_followers.searchFollowersUcid('1821058982')

    for ucid in ucid_list:
        a.splitArticle(ucid)