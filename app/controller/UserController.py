from database import UserInfo
from app.library import Util

class UserController(object):

    def __init__(self):
        self.user_info_cursor = UserInfo.UserInfo()

    # 获取用户列表
    def userProvinceList(self):

        province_list = {
            'china_list'  : [],
            'oversea_list': [],
        }

        china_list   = {}
        oversea_list = {}

        user_list = self.user_info_cursor.getUserInfoList(('ucid', 'address'), 0, 500)
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
            dic = {'name': k, 'value': v}
            province_list['china_list'].append(dic)

        # 遍历中国省份
        for k, v in oversea_list.items():
            dic = {'name': k, 'value': v}
            province_list['oversea_list'].append(dic)

        return  province_list

if __name__ == "__main__":
    a = UserController()
    a.userProvinceList()
