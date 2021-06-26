#!/usr/bin/python
# main.py

import sys
import os
import time
import subprocess
import shutil

from chromedriver import generate_chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from datetime import datetime

PROJECT_DIR = str(os.path.dirname(os.path.abspath(__file__)))
DOWNLOAD_DIR = f'{PROJECT_DIR}\download'
driver_path = f'{PROJECT_DIR}/lib/webDriver/'

platform = sys.platform
if platform == 'darwin':
    print('System platform : Darwin')
    driver_path += 'chromedriverMac'
elif platform == 'linux':
    print('System platform : Linux')
    driver_path += 'chromedriverLinux'
elif platform == 'win32':
    print('System platform : Window')
    driver_path += 'chromedriverWindow'
else:
    print(f'[{sys.platform}] not supported. Check your system platform.')
    raise Exception()

# 크롬 드라이버 인스턴스 생성    
chrome = generate_chrome(
    driver_path=driver_path,
    headless=False,
    download_path=DOWNLOAD_DIR)

# 페이지 요청
url = 'https://www.ahnlab.com/kr/site/login/loginForm.do'
chrome.get(url)
time.sleep(1.5) 

elm = chrome.find_element_by_id('userId')
elm.send_keys('userID') 
elm = chrome.find_element_by_id('passwd')
elm.send_keys('password') 

time.sleep(1)
elm.send_keys(Keys.ENTER)
time.sleep(1)

elm = chrome.find_element_by_xpath('//*[@id="mainEngineVersion"]')
enginedate = elm.text.replace('.', '', 3)[4:]

print(enginedate)

url = 'https://www.ahnlab.com/kr/site/download/product/productEngineList.do'
chrome.get(url)
time.sleep(2)

#exe file download
elm = chrome.find_element_by_xpath('//*[@id="form"]/div[3]/table/tbody/tr[1]/td[4]/a')
elm.click()
time.sleep(2)
elm = chrome.find_element_by_xpath('//*[@id="form"]/div[3]/table/tbody/tr[2]/td[4]/a')
elm.click()
time.sleep(2)
elm = chrome.find_element_by_xpath('//*[@id="form"]/div[3]/table/tbody/tr[2]/td[5]/a[2]')
elm.click()
time.sleep(2)

exeurl = 'https://www.ahnlab.com/kr/site/download/product/popHashDown.do?seq=419'
chrome.get(exeurl)
ahnlab_exehash = chrome.find_element_by_xpath('//*[@id="hashList"]/table/tbody/tr[2]/td').text.capitalize()
time.sleep(2)
zipurl = 'https://www.ahnlab.com/kr/site/download/product/popHashDown.do?seq=420'
chrome.get(zipurl)
ahnlab_ziphash = chrome.find_element_by_xpath('//*[@id="hashList"]/table/tbody/tr[2]/td').text.capitalize()

# time.sleep(100)

exepath = f'{PROJECT_DIR}\download\\ahnlabengine_setup.exe'
apcpath = f'{PROJECT_DIR}\download\\ahnlabengine_apc.zip'
ahcpath = f'{PROJECT_DIR}\download\\ahnlabengine_apc.zip.ahc'

while(True) :
    if os.path.exists(exepath) and os.path.exists(apcpath) and os.path.exists(ahcpath):
        break
    time.sleep(30)
    print("wait........")

sig_exehash = subprocess.check_output(f'{PROJECT_DIR}\download\sigcheck64.exe' + " -h " + f'{PROJECT_DIR}\download\\ahnlabengine_setup.exe | find \"SHA256\"', shell=True).capitalize().strip()
sig_apchash = subprocess.check_output(f'{PROJECT_DIR}\download\sigcheck64.exe' + " -h " + f'{PROJECT_DIR}\download\\ahnlabengine_apc.zip | find \"SHA256\"', shell=True).capitalize().strip()

print("ahnlabZIPHash : " + sig_apchash.decode('utf-8')[8:])
print("ZIPfileHash   : " + ahnlab_ziphash)
print("ahnlabEXEHash : " + sig_exehash.decode('utf-8')[8:])
print("EXEfileHash   : " + ahnlab_exehash)

os.makedirs("E:\\" + enginedate)
shutil.move(ahcpath, "E:\\" + enginedate)
shutil.move(exepath, "E:\\" + enginedate)
shutil.move(apcpath, "E:\\" + enginedate)