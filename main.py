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

PROJECT_DIR = str(os.path.dirname(os.path.abspath(__file__)))
DOWNLOAD_DIR = f'{PROJECT_DIR}\download'
driver_path = f'{PROJECT_DIR}/lib/webDriver/'

usb_drive = 'E:\\'

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

# login ~ enter download page
url = 'https://mycompany.ahnlab.com/'
chrome.get(url)
time.sleep(1.5) 

elm = chrome.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[1]/div[1]/button[1]/span[1]')
elm.click()
time.sleep(1)

elm = chrome.find_element_by_id('id')
elm.send_keys('') 
elm = chrome.find_element_by_id('password')
elm.send_keys('') 

elm.send_keys(Keys.ENTER)
time.sleep(1)

url = 'https://mycompany.ahnlab.com/download'
chrome.get(url)
time.sleep(1) 

elm = chrome.find_element_by_xpath('/html/body/div/div/div/div[3]/div[2]/div/div[4]/div[1]/span')
elm.click()

time.sleep(1) 

elm = chrome.find_element_by_xpath('//*[@id="k-panelbar-item-default-.0"]/div/div/div/div/table/tbody/tr[1]/td[1]/span[3]')
enginedate = elm.text.replace('.', '')

print(enginedate)

#exe, zip, ahc file download
print("open zip ahc")
elm = chrome.find_element_by_xpath('/html/body/div/div/div/div[3]/div[2]/div/div[4]/div[1]/span/p') # zip ahc open
elm.click()
elm.click()
time.sleep(0.5)

print("download zip file")
elm = chrome.find_element_by_xpath('/html/body/div/div/div/div[3]/div[2]/div/div[4]/div[1]/div/div/div/div/table/tbody/tr[1]/td[2]/a[1]/button') # zip down
elm.click()
time.sleep(0.5)

print("download ahc file")
elm = chrome.find_element_by_xpath('/html/body/div/div/div/div[3]/div[2]/div/div[4]/div[1]/div/div/div/div/table/tbody/tr[1]/td[2]/a[2]/button') # ahc down
elm.click()
time.sleep(0.5)

print("open hash")
elm = chrome.find_element_by_xpath('/html/body/div/div/div/div[3]/div[2]/div/div[4]/div[1]/div/div/div/div/table/tbody/tr[1]/td[2]/button') # ahc
elm.click()
time.sleep(0.5)

ahnlab_ziphash = chrome.find_element_by_xpath('/html/body/div/div/div/div[3]/div[2]/div/div[5]/div[2]/div[2]/table/tbody/tr[2]/td').text
time.sleep(0.5)

print("hash close")
elm = chrome.find_element_by_xpath('/html/body/div/div/div/div[3]/div[2]/div/div[5]/div[2]/div[3]/button') # hash close
elm.click()
time.sleep(0.5)

print("open exe")
elm = chrome.find_element_by_xpath('/html/body/div/div/div/div[3]/div[2]/div/div[4]/div[2]/span/p') # exe open
elm.click()
time.sleep(0.5)

print("download exe file")
elm = chrome.find_element_by_xpath('/html/body/div/div/div/div[3]/div[2]/div/div[4]/div[2]/div/div/div/div/table/tbody/tr[1]/td[2]/a/button') # exe
elm.click()
time.sleep(0.5)

print("open hash")
elm = chrome.find_element_by_xpath('/html/body/div/div/div/div[3]/div[2]/div/div[4]/div[2]/div/div/div/div/table/tbody/tr[1]/td[2]/button') # hash click
elm.click()
time.sleep(0.5)

ahnlab_exehash = chrome.find_element_by_xpath('/html/body/div/div/div/div[3]/div[2]/div/div[5]/div[2]/div[2]/table/tbody/tr[2]/td').text

print(  'zip SHA256: ' + ahnlab_ziphash, 
        'exe SHA256: ' + ahnlab_exehash)

print("hash close")
elm = chrome.find_element_by_xpath('/html/body/div/div/div/div[3]/div[2]/div/div[5]/div[2]/div[3]/button') # hash close
elm.click()
time.sleep(1)

# download and check file download complete.

exepath = f'{PROJECT_DIR}\download\\ahnlabengine_setup.exe'
apcpath = f'{PROJECT_DIR}\download\\ahnlabengine_apc.zip'
ahcpath = f'{PROJECT_DIR}\download\\ahnlabengine_apc.zip.ahc'

print("download process....")    
while(True) :
    if os.path.exists(exepath) and os.path.exists(apcpath) and os.path.exists(ahcpath):
        break
    time.sleep(10)

# check hash SHA256
sig_exehash = subprocess.check_output(f'{PROJECT_DIR}\download\sigcheck64.exe' + " -h " + f'{PROJECT_DIR}\download\\ahnlabengine_setup.exe | find \"SHA256\"', shell=True).strip()
sig_apchash = subprocess.check_output(f'{PROJECT_DIR}\download\sigcheck64.exe' + " -h " + f'{PROJECT_DIR}\download\\ahnlabengine_apc.zip | find \"SHA256\"', shell=True).strip()

print("ahnlabZIPHash : " + (sig_apchash.decode('utf-8')[8:]).capitalize())
print("ZIPfileHash   : " + (ahnlab_ziphash).capitalize())
print("ahnlabEXEHash : " + (sig_exehash.decode('utf-8')[8:]).capitalize())
print("EXEfileHash   : " + (ahnlab_exehash).capitalize())

# file move to USB
os.makedirs(usb_drive + enginedate)
shutil.move(ahcpath, usb_drive + enginedate)
shutil.move(exepath, usb_drive + enginedate)
shutil.move(apcpath, usb_drive + enginedate)
