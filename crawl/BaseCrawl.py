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
