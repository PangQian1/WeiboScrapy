import re

#给定参数获取性别  利用字符串操作和正则表达式
def getSex(str):
    pos = str.index('sex')
    str0 = str[pos:]
    sex = re.match(r'sex=m$', str0)
    #print(sex)
    if(sex):
        return 'm'
    else:
        return 'f'

#给定参数获取用户ID，利用字符串操作
def getID(str):
    pos = str.index('&')
    res = str[3:pos]
    return res

# 过滤表情
def filterEmoji(str):
    str_list = re.findall(r"[a-zA-Z0-9\u4e00-\u9fa5]+|[+—！，。？、~@#￥%.&*（）]+|[+#-?()\.!\/_,$%^*\+\"\']+", str)

    res =  '' . join(str_list)
    if res[len(res) - 5 : ] == '收起全文d':
        res = res[ : len(res) - 5]

    return res

# 提取数字
def filterNumber(str):
    str_list = re.findall(r"[0-9]+", str)

    return ''.join(str_list)