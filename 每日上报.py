import os
import traceback

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

print('初始化浏览器')
USERNAME = os.environ['ID']
PASSWORD = os.environ['PASSWORD']

option = webdriver.ChromeOptions()
option.headless = True
option.add_experimental_option('prefs', {'intl.accept_languages': 'zh-CN'})
driver = webdriver.Chrome(
    service=Service(executable_path='/usr/bin/chromedriver'), options=option)

success = False
print('正在登录')
for i in range(5):
    try:
        driver.get('https://uis.nwpu.edu.cn/cas/login')
        driver.find_element(By.ID, 'username').send_keys(USERNAME)
        driver.find_element(By.ID, 'password').send_keys(PASSWORD)
        driver.find_element(By.ID, 'fm1').find_element(By.NAME,
                                                       'submit').click()
        if driver.get_cookie('TGC') is not None:
            success = True
            break
    except:
        traceback.print_exc()
        print(f'登录失败{i + 1}次，正在重试...')

if not success:
    raise Exception('登录多次失败，可能学工系统已更新')

success = False
print('正在上报')
for i in range(5):
    try:
        driver.get('https://yqtb.nwpu.edu.cn/wx/ry/jrsb_js.jsp')

        state = driver.find_element(By.ID, 'rbxx_div').find_element(
            By.CLASS_NAME, 'page__top2').text
        print(state)
        if '您已提交今日填报' in state:
            success = True
            break

        driver.find_element(By.ID, 'rbxx_div').find_element(
            By.CLASS_NAME, 'weui-btn-area').find_element(By.TAG_NAME,
                                                         'a').click()
        confirm_cb = driver.find_element(By.ID, 'brcn')
        if not confirm_cb.is_selected():
            confirm_cb.find_element(By.XPATH,
                                    './..').find_element(By.TAG_NAME,
                                                         'i').click()
        driver.find_element(By.ID, 'save_div').click()
    except:
        traceback.print_exc()
        print(f'失败{i + 1}次，正在重试...')
driver.quit()
if success:
    print('上报完成')
else:
    raise Exception('上报多次失败，可能学工系统已更新')
