import time
from selenium import webdriver
from database import UserInfo
from crawl import LoginCrawl

# 爬取个人信息
def crawlUserInfo(ucid, driver):
    user_info     = UserInfo.UserInfo()

    user_url = 'https://weibo.com/' + str(ucid)
    driver.get(user_url)
    time.sleep(3)

    # 关注 & 粉丝 & 微博
    results = driver.find_elements_by_css_selector("#Pl_Core_T8CustomTriColumn__3 > div > div > div > table > tbody > tr > td")
    print(len(results))
    follow_number = results[0].text.replace('关注', '').strip()
    follower_number = results[1].text.replace('粉丝', '').strip()
    weibo_number = results[2].text.replace('微博', '').strip()

    # 获取是否是认证微博
    try:
        driver.find_elements_by_css_selector("div.verify_area.W_tog_hover.S_line2 > p.verify.clearfix > span.icon_bed.W_fl > a")
        is_verify = 2
        print('认证微博')
    except:
        is_verify = 1
        print('未认证微博')

    # 获取个人信息详情页
    user_info_url = driver.find_element_by_css_selector("#Pl_Core_UserInfo__6 > div:nth-child(2) > div.WB_cardwrap.S_bg2 > div > a").get_attribute('href')
    print(user_info_url)
    driver.get(user_info_url)

    # 注册时间
    sign_up_time = ''
    try:
        info_results = driver.find_elements_by_css_selector(
            "#Pl_Official_PersonalInfo__58 > div:nth-child(1) > div > div.WB_innerwrap > div > ul > li")
        if len(info_results) > 0:
            sign_up_time = info_results[-1].text.replace('注册时间：', '')
        else:
            print('没有注册时间')
    except:
        print('没有注册时间')

    # 用户等级
    level_text = driver.find_element_by_css_selector(
        "#Pl_Official_RightGrowNew__56 > div > div > div > div:nth-child(2) > div > div.WB_innerwrap > div > div > a").text
    level = level_text.replace('Lv.', '').strip()

    # 用户标签
    tags_text = driver.find_element_by_css_selector(
        "#Pl_Official_PersonalInfo__58 > div:nth-child(2) > div > div.WB_innerwrap > div > ul > li").text
    tags = tags_text.replace("\n标签：", '').replace('\n', ',')

    print(follow_number)
    print(follower_number)
    print(weibo_number)
    print(level)
    print(sign_up_time)
    print(is_verify)
    print(tags)

    # 更新用户信息
    data_userInfo = (follow_number, follower_number, weibo_number, level, sign_up_time, is_verify, tags)
    sql = "UPDATE weibo_user_info SET " \
          "follow_number = '%s', " \
          "follower_number = '%s', " \
          "weibo_number = '%s', " \
          "level = '%s', " \
          "sign_up_time = '%s', " \
          "is_verify = '%s', " \
          "tags = '%s'" \
          "WHERE ucid = " + ucid
    user_info.executeSql(sql, data_userInfo)

    time.sleep(3)

if __name__ == "__main__":
    user_info = UserInfo.UserInfo()
    user_list = user_info.getUserInfoList(('ucid'))

    # 使用谷歌浏览器
    driver = webdriver.Chrome()
    driver.get('http://weibo.com/login.php')
    # 使窗口最大化显示出登录界面
    driver.maximize_window()
    # 登录
    LoginCrawl.loginWeibo('17865169752', '1835896411', driver)

    time.sleep(5)
    crawlUserInfo('1730330447', driver)

    # for value in user_list:
    #     crawlUserInfo(value['ucid'], driver)