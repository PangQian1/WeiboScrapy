import random
from database import UserInfo
from database import UserFollowers
from app.library import Util

class UserController(object):

    def __init__(self):
        self.user_info_cursor     = UserInfo.UserInfo()
        self.user_follower_cursor = UserFollowers.UserFollowers()

    """
    获取用户个人信息
    """
    def userInfo(self, ucid) :
        user_info = {}
        # 如果ucid为空 就把所有人的信息取出来
        if not ucid.strip() :
            user_info = {
                'name' : '管理员',
                'introduction' : '微博爬虫爬取的全部微博用户',
                'keywords' : '微博爬虫爬取的全部微博用户',
                'sex' : 'f',
                'is_verify' : 2,
                'follow_number' : '9999',
                'follower_number' : '9999',
                'weibo_number' : '9999',
            }
            return user_info

        result = self.user_info_cursor.getUserInfoByUcid([ucid], ())
        if len(result) :
            user_info = result[0]
            del user_info['ctime']
            del user_info['mtime']

        return user_info

    """
    获取用户省份列表
    """
    def userProvinceList(self, ucid):
        province_list = {
            'china_list'  : [],
            'oversea_list': [],
        }

        china_list   = {}
        oversea_list = {}

        fans_list = []
        # 如果ucid为空 就把所有人的信息取出来
        if not ucid.strip() :
            result = self.user_info_cursor.getUserInfoList(['ucid'], 0, 10000)
            for value in result :
                fans_list.append(str(value['ucid']))
        else :
            fans_list = self.user_follower_cursor.searchFansUcid(ucid)

        if len(fans_list) <= 0 :
            return province_list
        user_list = self.user_info_cursor.getUserInfoByUcid(fans_list, ('ucid', 'address'))
        for value in user_list:
            address = value['address'].split(' ')
            if address[0] == '海外':
                if len(address) <= 1:
                    address.append('其他')

                number = Util.extractVal(oversea_list, address[1], 0)
                number += 1
                oversea_list[address[1]] = number
            else :
                number = Util.extractVal(china_list, address[0], 0)
                number += 1
                china_list[address[0]] = number

        # 遍历中国省份
        for k,v in china_list.items():
            dic = {'name' : k, 'value' : v,}
            if k == '北京' :
                dic = {'name': k, 'value': v, 'selected' : True}

            province_list['china_list'].append(dic)

        # 遍历中国省份
        for k, v in oversea_list.items():
            dic = {'name': k, 'value': v}
            province_list['oversea_list'].append(dic)

        return  province_list

    '''
    获取粉丝性别和认证的列表
    '''
    def userSexVerifyList(self, ucid):
        sex_verify_list = {
            'sex_list'    : [],
            'verify_list' : [],
        }
        ucid = str(ucid)
        fans_list = self.user_follower_cursor.searchFansUcid(ucid)
        # 如果ucid为空 就把所有人的信息取出来
        if not ucid.strip() :
            result = self.user_info_cursor.getUserInfoList(['ucid'], 0, 10000)
            for value in result :
                fans_list.append(str(value['ucid']))

        if len(fans_list) <= 0 :
            return sex_verify_list
        user_sex_list = self.user_info_cursor.getUserInfoByUcid(fans_list, ('count(sex) as number' ,'sex'), 'GROUP BY sex')
        for value in user_sex_list:
            if value['sex'] == 'f' :
                dic = {'name' : '女', 'value' : value['number'], }
            elif value['sex'] == 'm' :
                dic = {'name' : '男', 'value' : value['number'], }
            else :
                dic = {'name' : '其他', 'value' : value['number'], }

            sex_verify_list['sex_list'].append(dic)

        user_verify_list = self.user_info_cursor.getUserInfoByUcid(fans_list, ('count(is_verify) as number', 'is_verify'), 'GROUP BY is_verify')
        for value in user_verify_list :
            if value['is_verify'] == '1' :
                dic = {'name' : '未认证', 'value' : value['number'], }
            elif value['is_verify'] == '2' :
                dic = {'name' : '微博认证', 'value' : value['number'], 'selected' : True}
            else :
                dic = {'name' : '其他', 'value' : value['number'], }

            sex_verify_list['verify_list'].append(dic)

        return sex_verify_list

    """
    获取用户注册时间
    """
    def userSignupList(self, ucid):
        user_signup_list = {
            'signup_list' : [],
            'percent_list' : [],
        }

        ucid = str(ucid)
        fans_list = self.user_follower_cursor.searchFansUcid(ucid)
        # 如果ucid为空 就把所有人的信息取出来
        if not ucid.strip() :
            result = self.user_info_cursor.getUserInfoList(['ucid'], 0, 10000)
            for value in result :
                fans_list.append(str(value['ucid']))

        if len(fans_list) <= 0 :
            return user_signup_list

        total_number = 0
        sub_sql = 'substr(sign_up_time, 1, 4)'
        result  = self.user_info_cursor.getUserInfoByUcid(fans_list, ( 'count(' + sub_sql +') as number', sub_sql + ' as sign_up_time' ), ' GROUP BY ' + sub_sql)
        # 注册时间人数 按照年份统计
        for value in result:

            if value['sign_up_time'].strip() :
                total_number += int(value['number'])
                dic = value['number']
            else :
                continue

            user_signup_list['signup_list'].append(dic)

        # 注册时间百分比 按照年份统计
        for value in result :
            if value['sign_up_time'].strip() :
                percent = round((int(value['number']) / total_number) * 100, 1)
                dic = percent
            else :
                continue

            user_signup_list['percent_list'].append(dic)

        return user_signup_list

    """
    搜索用户信息
    """
    def userSearchList(self, username):
        user_list = {
            'search_list'  : [],
            'commend_list' : [],
        }
        # 搜索结果
        if username.strip() :
            sql = "select * from weibo_user_info where name like '%s'"
            result = self.user_info_cursor.executeSelectSql(sql, ('%' + username +'%'))
            for value in result :
                del value['ctime']
                del value['mtime']
                user_list['search_list'].append(value)

        # 推荐用户
        offset = random.randint(0, 20)
        size = 3
        sql = "select * from weibo_user_info ORDER BY follower_number DESC LIMIT %s,%s "
        result = self.user_info_cursor.executeSelectSql(sql, (offset, size))
        for value in result :
            del value['ctime']
            del value['mtime']
            user_list['commend_list'].append(value)

        print(user_list)
        return user_list

if __name__ == "__main__":
    a = UserController()
    a.userSearchList('胡歌')