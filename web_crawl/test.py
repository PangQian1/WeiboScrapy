
a = (3,4,5)
print(a[0])


'''
#进入进入目标微博
res = driver.find_element_by_css_selector('#pl_weibo_directtop > div > div > div > div.star_detail > p.star_card > a')
addr = res.get_attribute('href')
driver.get(addr)

#实现鼠标的悬停在微博头像上
chain = ActionChains(driver)
fan_addr = driver.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__28"]/div/div[2]/div[1]/div[2]/div/a/img')
chain.move_to_element(fan_addr).perform()

# 获取当前窗口句柄
now_handle = driver.current_window_handle
print(now_handle)

# 获取所有窗口句柄
allhandles = driver.window_handles
# 在所有窗口中查找弹出窗口

print(allhandles)

for handle in allhandles:
    if handle != now_handle:
        print('jinru')
        driver.switch_to.window(handle)  # 这两步是在弹出窗口中进行的操作，证明我们确实进入了
        temp = driver.current_url
        driver.get(temp)
'''
