from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pyperclip
import time

login = {
    "id" : "",
    "pw" : ""
}

WEBDRIVER_PATH = "C:\\Users\\MGEN\\chromedriver.exe"

login_url = "https://nid.naver.com/nidlogin.login"
blog_categ_url = 'https://blog.naver.com/PostList.nhn?blogId=mgen007&from=postList&categoryNo='
blog_categ_idx={
    'blockchain':'11',
    'smart_factory':'12',
    '3DMET':'13',
}

def clipboard_input(user_xpath, user_input):
        temp_user_input = pyperclip.paste()  # 사용자 클립보드를 따로 저장

        pyperclip.copy(user_input)
        driver.find_element_by_xpath(user_xpath).click()
        ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

        pyperclip.copy(temp_user_input)  # 사용자 클립보드에 저장 된 내용을 다시 가져 옴
        time.sleep(1)


driver=webdriver.Chrome(WEBDRIVER_PATH)

# login page
driver.get(login_url)
time.sleep(0.2)
clipboard_input('//*[@id="id"]', login.get("id"))
time.sleep(0.2)
clipboard_input('//*[@id="pw"]', login.get("pw"))
driver.find_element_by_xpath('//*[@id="log.login"]').click()

#browser save page
time.sleep(0.3)
driver.find_element_by_xpath('//*[@id="new.save"]').click()

#editor page
driver.get(blog_categ_url+blog_categ_idx['3DMET'])
driver.find_element_by_xpath('//*[@id="post-admin"]/a[1]').click()
time.sleep(3)
