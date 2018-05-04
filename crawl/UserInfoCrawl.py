import time
from selenium import webdriver
from database import UserInfo
from crawl import LoginCrawl

# 爬取个人信息
def crawlUserInfo(ucid, driver):

    user_info = UserInfo.UserInfo()
    user_url  = 'https://weibo.com/' + str(ucid)
    driver.get(user_url)
    time.sleep(1)

    # 关注 & 粉丝 & 微博
    try:
        results = driver.find_elements_by_css_selector(
            "#Pl_Core_T8CustomTriColumn__3 > div > div > div > table > tbody > tr > td")
        #print(len(results))
        follow_number   = results[0].text.replace('关注', '').strip()
        follower_number = results[1].text.replace('粉丝', '').strip()
        weibo_number    = results[2].text.replace('微博', '').strip()

        print(follow_number)
        print(follower_number)
        print(weibo_number)
    except:
        return 1

    # 获取是否是认证微博
    try:
        driver.find_element_by_css_selector("div.verify_area.W_tog_hover.S_line2 > p.verify.clearfix")
        is_verify = 2
        #print('认证微博')
    except:
        is_verify = 1
        #print('未认证微博')

    # 获取个人信息详情页
    #user_info_url = driver.find_element_by_css_selector("#Pl_Core_UserInfo__6 > div > div.WB_cardwrap.S_bg2 > a.WB_cardmore.S_txt1.S_line1.clearfix").get_attribute('href')
    #print(user_info_url)
    try:
        user_info_url = driver.find_element_by_css_selector('div.PCD_person_info > a').get_attribute('href')
        driver.get(user_info_url)
    except:
        return 1

    # 用户等级
    level = ''
    try:
        level_text = driver.find_element_by_css_selector(
            "div.level_box.S_txt2 > a").text
        level = level_text.replace('Lv.', '').strip()

    except:
        #print('没有级别')
        pass

    #用户生日
    birthday = ''
    # 注册时间 & 生日
    sign_up_time = ''
    try:
        info_results = driver.find_elements_by_css_selector(
            "div:nth-child(1) > div > div.WB_innerwrap > div > ul > li")

        for value in info_results:
            if value.text.find('生日：') >= 0:
                birthday = value.text.replace('生日：' , '').strip()

        if (len(info_results) > 0) and (info_results[-1].text.find('注册时间') >= 0):
            sign_up_time = info_results[-1].text.replace('注册时间：', '').strip()
        else:
            #print('没有注册时间')
            pass
    except:
        #print('没有注册时间')
        pass

    #用户标签
    tags = ''
    try:
        flag = False
        models = driver.find_elements_by_css_selector('div.WB_frame_c > div > div')
        #print(len(models))

        for value in models:
            #print(value.text)

            if value.text.find('标签：') >= 0:
                #print('有标签')
                flag = True
                #tags = value.text.replace("\n标签：", '').replace('\n', ',')
            if flag:
                tags = tags + ',' + value.text

        if flag:
            tags = value.text.replace('\n', ',').replace("标签信息,标签：,", '')
    except:
        pass
        #print('无标签')

    print(birthday)
    print(level)
    print(sign_up_time)
    print(tags)
    print(is_verify)

    # 更新用户信息
    data_userInfo = (follow_number, follower_number, weibo_number, level, birthday, sign_up_time, is_verify, tags)
    sql = "UPDATE weibo_user_info SET " \
          "follow_number = '%s', " \
          "follower_number = '%s', " \
          "weibo_number = '%s', " \
          "level = '%s', " \
          "birthday = '%s', " \
          "sign_up_time = '%s', " \
          "is_verify = '%s', " \
          "tags = '%s'" \
          "WHERE ucid = " + ucid
    user_info.executeUpdateSql(sql, data_userInfo)

    return 0

if __name__ == "__main__":
    user_info = UserInfo.UserInfo()
    user_list = user_info.getUserInfoList(['ucid'], 100, 20)

    # 使用谷歌浏览器
    driver = webdriver.Chrome()
    driver.get('http://weibo.com/login.php')
    # 使窗口最大化显示出登录界面
    driver.maximize_window()
    # 登录
    LoginCrawl.loginWeibo('17865169752', '1835896411', driver)

    time.sleep(5)
    res = crawlUserInfo('2009178141', driver)

    # for value in user_list:
    #     crawlUserInfo(str(value['ucid']), driver)