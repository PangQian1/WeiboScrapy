from database import UserInfo
from database import UserFollowers
from app.library import Util

class UserController(object):

    def __init__(self):
        self.user_info_cursor     = UserInfo.UserInfo()
        self.user_follower_cursor = UserFollowers.UserFollowers()

    # 获取用户省份列表
    def userProvinceList(self, ucid):

        province_list = {
            'china_list'  : [],
            'oversea_list': [],
        }

        china_list   = {}
        oversea_list = {}

        fans_list = self.user_follower_cursor.searchFansUcid(ucid)
        if len(fans_list) <= 0 :
            return province_list
        user_list = self.user_info_cursor.getUserInfoByUcid(fans_list, ('ucid', 'address'))
        for value in user_list:
            #print(value)
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

    # 获取粉丝性别和认证的列表
    def userSexVerifyList(self, ucid):
        sex_verify_list = {
            'sex_list'    : [],
            'verify_list' : [],
        }

        fans_list = self.user_follower_cursor.searchFansUcid(ucid)
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
        print(sex_verify_list)
        return sex_verify_list

if __name__ == "__main__":
    a = UserController()

    a.userSexVerifyList('2009178141')
