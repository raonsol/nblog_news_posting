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
from datetime import datetime
import os
import subprocess
import json
from bs4 import BeautifulSoup
import HTMLClipboard
from cssutils import parseStyle

#############################################################################################
# Type entry:
# [MGEN] for mgen blog, [IPF] for IPFrontiers blog
TYPE = 'MGEN'
# Category entry for MGEN:
# blockchain, smart_factory, 3dmet
# Category entry for IPF:
# patent=특허, design=상표디자인, copyright=저작권, ipsuit=IP분쟁소송, startup=Startup Info.
CATEGORY = "blockchain"
# Fill the content below:
NEWSPAPER_NAME = "연합뉴스"
HEADLINE = "블록체인으로 1천만명 이용하는 온라인 투표시스템 구축한다"
URL = 'https://www.yna.co.kr/view/AKR20210623065100017?input=1195m'

# Path of the tools needed for script
WEBDRIVER_PATH = os.path.expanduser('~\\chromedriver.exe')
ILLUSTRATOR_PATH = "C:\\Program Files\\Adobe\\Adobe Illustrator CS6 (64 Bit)\\Support Files\\Contents\\Windows\\Illustrator.exe"
SCRIPT_PATH=os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), "head_img_generator.js")
#############################################################################################
DEST_MGEN = "C:\\Users\\MGEN\\Desktop\\LYJ\\11. Blog\\Output\\"
DEST_IPF = "C:\\Users\\MGEN\\Desktop\\LYJ\\00. IPF\\Output\\"


blog_categ_mgen = {
    'blockchain': '11',
    'smart_factory': '12',
    '3dmet': '13',
}
blog_categ_ipf = {
    'patent': '22',
    'design': '23',
    'copyright': '24',
    'ipsuit': '16',
    'startup': '19',
}
blog_categ_mgen_c = {
    'blockchain': 'rgb(244, 221, 15)',
    'smart_factory': 'rgb(125, 90, 156)',
    '3dmet': 'rgb(40, 171, 171)',
}
blog_categ_ipf_c = {
    'patent': 'rgb(195,13,35)',
    'design': 'rgb(234,124,156)',
    'copyright': 'rgb(0,157,57)',
    'ipsuit': 'rgb(230,198,110)',
    'startup': 'rgb(5,181,237)',
}

class ContentBuilder:

    # get path based on current date
    def getDatePath(self, outpath):
        year = str(datetime.today().year)
        month = datetime.today().month
        month = str(month).zfill(2)
    
        return os.path.join(outpath, year, month)
    
    # clipboard method for avoid captcha
    def clipboardInput(self, user_xpath, user_input):
        temp_user_input = pyperclip.paste()  # 사용자 클립보드를 따로 저장
    
        pyperclip.copy(user_input)
        driver.find_element_by_xpath(user_xpath).click()
        ActionChains(driver).key_down(Keys.CONTROL).send_keys(
            'v').key_up(Keys.CONTROL).perform()
    
        pyperclip.copy(temp_user_input)  # 사용자 클립보드에 저장 된 내용을 다시 가져 옴
        time.sleep(1)
    
    # get content from JSON file
    def getContent(self):
        with open('./img_content.json', 'r', encoding='utf-8') as json_obj:
            content = json.load(json_obj)
        return content
    
    # get login info from the loginfo_[blog_name].txt file in same directory
    def getLogin(self, type):
        login_fname = "./logInfo_"+type+'.txt'
        f = open(login_fname, 'r')
        lines = f.readlines()
        login = {"id": lines[0], "pw": lines[1]}
        return login
    
    # method for creating head image
    def createHeadImage(self):
        print("Loading script in "+SCRIPT_PATH)
        p = subprocess.Popen([ILLUSTRATOR_PATH, SCRIPT_PATH])
        p.wait()
    
    def writeContent(self, typ, category, newspaper, headline):
        content = dict()
        content["type"] = typ
        content["category"] = category
        content["newspaper"] = newspaper
        content["headline"] = headline
        with open('./img_content.json', 'w', encoding='utf-8') as make_file:
            json.dump(content, make_file, indent="\t", ensure_ascii=False)
    
    def createSourceTable(self, type, newspaper, url, color):
        file_name = "url_source_{}.html".format(type)
    
        # shorten url
        if url.startswith("http://"):
            url = url.replace("http://", "")
        elif url.startswith("https://"):
            url = url.replace("https://", "")
    
        if url.startswith("www."):
            url = url.replace("www.", "")
    
        with open(file_name, encoding='utf-8') as fp:
            soup = BeautifulSoup(fp, 'html.parser')
    
        # change name and color of newspaper
        newspaper_content = soup.find('span', {"id": "SE-newspaper-name"})
        newspaper_content.string.replace_with(newspaper)
        style = parseStyle(newspaper_content['style'])
        style['color'] = color
        # Replace td's styles in the soup with the modified styles
        newspaper_content['style'] = style.cssText
    
        # change url
        url_content = soup.find('span', {"id": "SE-url-shorten"})
        url_content.string.replace_with(url)
    
        return str(soup)


driver = webdriver.Chrome(WEBDRIVER_PATH)
builder=ContentBuilder()
login = builder.getLogin(TYPE)

# assign catagory url and color
if TYPE == 'MGEN':
    blog_categ_idx = blog_categ_mgen[CATEGORY]
    blog_categ_c = blog_categ_mgen_c[CATEGORY]
    dest_path = builder.getDatePath(DEST_MGEN)
elif TYPE == "IPF":
    blog_categ_idx = blog_categ_ipf[CATEGORY]
    blog_categ_c = blog_categ_ipf_c[CATEGORY]
    dest_path = builder.getDatePath(DEST_IPF)
else:
    print("Blog Type error!")

login_url = "https://nid.naver.com/nidlogin.login"
blog_categ_url = ('https://blog.naver.com/PostList.nhn?blogId='
                  + login["id"]+'&from=postList&categoryNo='+blog_categ_idx)

# write content into JSON file
builder.writeContent(TYPE, CATEGORY, NEWSPAPER_NAME, HEADLINE)

# create headline image
builder.createHeadImage()

### login page ###
driver.get(login_url)
time.sleep(0.2)
builder.clipboardInput('//*[@id="id"]', login.get("id"))
time.sleep(0.1)
builder.clipboardInput('//*[@id="pw"]', login.get("pw"))
driver.find_element_by_xpath('//*[@id="log.login"]').click()

### browser save page ###
url_browser_save = "https://nid.naver.com/login/ext/deviceConfirm.nhn"
if url_browser_save in driver.current_url:
    driver.find_element_by_xpath('//*[@id="new.save"]').click()
time.sleep(1)

### editor page ###
driver.get(blog_categ_url)

driver.find_element_by_xpath('//*[@id="post-admin"]/a[1]').click()
time.sleep(3)

## 작성중인 글 닫기 ##
try:
    cancel = driver.find_element_by_css_selector(
        '.se-popup-button.se-popup-button-cancel')
    cancel.click()
    time.sleep(1)
except:
    pass

## 도움말 닫기 ##
try:
    close_help = driver.find_element_by_class_name(
        'se-help-panel-close-button')
    close_help.click()
    time.sleep(1)
except:
    pass

### fill contents ###

# editor_element=driver.find_element_by_id('mainFrame')
# driver.switch_to.frame('mainFrame')

## head content ##
#'.se-placeholder.__se_placeholder.se-ff-{폰트 이름}.se-fs32'
# css 이름이 기본 폰트 설정값에 따라 달라짐
title = driver.find_element_by_css_selector(
    '.se-placeholder.__se_placeholder.se-ff-system.se-fs32')
action = ActionChains(driver)
(
    action
    .move_to_element(title).pause(.5)
    .click()
    .send_keys(HEADLINE)
    .perform()
)
action.reset_actions()

## body content ##
contents = driver.find_element_by_css_selector(
    '.se-component.se-text.se-l-default')
contents.click()
# paste edited html
url_table = builder.createSourceTable(TYPE, NEWSPAPER_NAME, URL, blog_categ_c)
HTMLClipboard.PutHtml(url_table)
# Ctrl+V, dependant on OS
ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').perform()
time.sleep(1)

# upload head image
# TODO: 이미지 파일 경로를 줘도 파일 선택 창이 열림

IMG_PATH = os.path.join(dest_path, str(datetime.today().month).zfill(
    2)+str(datetime.today().day).zfill(2)+".png")
insert_button = driver.find_element_by_css_selector(
    '.se-insert-point-marker-icon')
insert_button.click()
insert_button = driver.find_element_by_css_selector(
    '.se-insert-menu-button.se-insert-menu-button-image').send_keys(IMG_PATH)

driver.switch_to.default_content()
