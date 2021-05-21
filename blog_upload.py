#############################################################################################
# Script Description:
# 1. Create head image that contains following contents by user input
#       - Headline for news content
#       - Name of the newspaper
#       - Current date (applied automatically)
# 2. Accesses to the blog and shows the editor page
#############################################################################################

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pyperclip
import time
import os
import json

#############################################################################################
# Type entry:
# [MGEN] for mgen blog, [IPF] for IPFrontiers blog
TYPE='IPF'
# Category entry for MGEN:
# blockchain, smart_factory, 3dmet
# Category entry for IPF:
# patent=특허, design=상표디자인, copyright=저작권, ipsuit=IP분쟁소송, startup=Startup Info.
CATEGORY="design"
# Fill the content below:
NEWSPAPER_NAME="서울경제"
HEADLINE='"우리 가수 이름 쓰지마"···영탁 막걸리 때아닌 상표 논쟁'

# Path of the tools needed for script
WEBDRIVER_PATH = os.path.expanduser('~\\chromedriver.exe')
ESTK_PATH="C:\\Program Files (x86)\\Adobe\\Adobe Utilities - CS6\\ExtendScript Toolkit CS6\\ExtendScript Toolkit.exe"
#############################################################################################

blog_categ_mgen={
    'blockchain':'11',
    'smart_factory':'12',
    '3dmet':'13',
}
blog_categ_ipf={
    'patent':'22',
    'design':'23',
    'copyright':'24',
    'ipsuit':'16',
    'startup':'19',
}

# clipboard method for avoid captcha 
def clipboardInput(user_xpath, user_input):
    temp_user_input = pyperclip.paste()  # 사용자 클립보드를 따로 저장

    pyperclip.copy(user_input)
    driver.find_element_by_xpath(user_xpath).click()
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

    pyperclip.copy(temp_user_input)  # 사용자 클립보드에 저장 된 내용을 다시 가져 옴
    time.sleep(1)

# get login info from the loginfo_[blog_name].txt file in same directory
def getLogin(type):
    login_fname="./logInfo_"+type+'.txt'
    f=open(login_fname, 'r')
    lines=f.readlines()
    login = {"id":lines[0],"pw":lines[1]}
    return login

# method for creating head image
def headImageCreate(typ, category, newspaper, headline):
    content=dict()
    content["type"]=typ
    content["category"]=category
    content["newspaper"]=newspaper
    content["headline"]=headline
    with open('./img_content.json', 'w', encoding='utf-8') as make_file:
        json.dump(content, make_file, indent="\t", ensure_ascii=False)
    os.startfile(".\head_img_generator.jsx")

driver=webdriver.Chrome(WEBDRIVER_PATH)
login=getLogin(TYPE)

if TYPE=='MGEN':
    blog_categ_idx=blog_categ_mgen
elif TYPE=="IPF":
    blog_categ_idx=blog_categ_ipf
else: print("Blog Type error!")

login_url = "https://nid.naver.com/nidlogin.login"
blog_categ_url = ('https://blog.naver.com/PostList.nhn?blogId='
    +login["id"]+'&from=postList&categoryNo='+blog_categ_idx[CATEGORY])

#create headline image
headImageCreate(TYPE, CATEGORY,NEWSPAPER_NAME, HEADLINE)

# login page
driver.get(login_url)
time.sleep(0.2)
clipboardInput('//*[@id="id"]', login.get("id"))
time.sleep(0.1)
clipboardInput('//*[@id="pw"]', login.get("pw"))
driver.find_element_by_xpath('//*[@id="log.login"]').click()

# browser save page
url_browser_save="https://nid.naver.com/login/ext/deviceConfirm.nhn"
if url_browser_save in driver.current_url:
    driver.find_element_by_xpath('//*[@id="new.save"]').click()
time.sleep(0.2)

# editor page
driver.get(blog_categ_url)
driver.find_element_by_xpath('//*[@id="post-admin"]/a[1]').click()
time.sleep(3)

# TODO:fill contents
