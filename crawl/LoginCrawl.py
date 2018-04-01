from selenium import webdriver
from database import UserInfo

#登录微博的过程
def loginWeibo(name, password, driver):

    # 输入登录名和密码
    driver.find_element_by_xpath('//*[@id="loginname"]').clear()
    driver.find_element_by_xpath('//*[@id="loginname"]').send_keys(name)

    driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[2]/div/input').clear()
    driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[2]/div/input').send_keys(password)

    # 点击一下登录按钮使其弹出验证码图片
    # //*[@id="pl_login_form"]/div/div[3]/div[6]/a
    driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a').click()

    # 获取验证码
    res = driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[3]/a/img')
    # print(res)
    # print(res.get_attribute('height'))
    img = res.get_attribute('src')
    print(img)
    identify_code = input('Please input the identify_code:')

    #有些时候不需要验证码，这个时候此地便会报错，直接跳过就好
    try:
        # 将获得的验证码键入网页进行登录
        driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[3]/div/input').clear()
        driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[3]/div/input').send_keys(identify_code)
        # 再次点击登录
        driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a').click()
    except:
        pass

if __name__ == "__main__":

    # 使用谷歌浏览器
    driver = webdriver.Chrome()
    driver.get('http://weibo.com/login.php')
    # 使窗口最大化显示出登录界面
    driver.maximize_window()
    user_info = UserInfo.UserInfo()
