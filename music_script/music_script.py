import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import chromedriver_autoinstaller
import subprocess
import shutil
import pyautogui
import requests
import json

def get_secret_key() -> dict:
    with open("secret.json", "r") as secret:
        key = json.load(secret)
    
    key_list = {}
    key_list['ID'] = key["ID"]
    key_list['PW'] = key["PW"]

    return key_list

try:
    shutil.rmtree(r"C:\chrometemp")  # remove Cookie, Cache files
except FileNotFoundError:
    pass

try:
    subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 '
                     r'--user-data-dir="C:\chrometemp"')   # Open the debugger chrome
    
except FileNotFoundError:
    subprocess.Popen(r'C:\Users\binsu\AppData\Local\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 '
                     r'--user-data-dir="C:\chrometemp"')

option = Options()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
#option.add_argument('--start-fullscreen')

chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
try:
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
    
except:
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
driver.implicitly_wait(10)

# driver.get(
#     url='https://accounts.google.com/signin/v2/identifier?service=youtube&uilel=3&passive=true&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Dko%26next%3Dhttps%253A%252F%252Fwww.youtube.com%252F&hl=ko&ec=65620&flowName=GlifWebSignIn&flowEntry=ServiceLogin')
driver.get('https://accounts.google.com/ServiceLogin?continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Ffeature%3D__FEATURE__%26hl%3Dko%26action_handle_signin%3Dtrue%26next%3Dhttps%253A%252F%252Fmusic.youtube.com%252F%26app%3Ddesktop&uilel=3&passive=true&service=youtube&ltmpl=music&hl=ko"')
driver.maximize_window()

# Google login page
pyautogui.write(get_secret_key()['ID'])    # Fill in your ID or E-mail
pyautogui.press('tab', presses=3)   # Press the Tab key 3 times
pyautogui.press('enter')
time.sleep(3)   # wait a process
pyautogui.write(get_secret_key()['PW'])   # Fill in your PW
pyautogui.press('enter')
time.sleep(7)   # wait a process
pyautogui.press('esc')

#driver.get('https://music.youtube.com/')

data = {"who": "ningpop"}
is_first_song = True
while True:
    try:
        response = requests.get('http://127.0.0.1:8000/music/get_music', params=data, timeout=5)
        response.encoding = 'UTF-8'
        music = response.text
        time.sleep(1)

        if len(music) != 0:
            try:
                # 검색
                driver.find_element_by_xpath('//*[@id="layout"]/ytmusic-nav-bar/div[2]/ytmusic-search-box').click()
                driver.find_element_by_tag_name('input').send_keys(music)
                pyautogui.press('enter')

                time.sleep(2)

                # 음악 추가
                more = driver.find_element_by_xpath('//*[@id="contents"]/ytmusic-responsive-list-item-renderer')
                hover = ActionChains(driver).move_to_element(more)
                hover.perform()
                driver.find_element_by_xpath('/html/body/ytmusic-app/ytmusic-app-layout/div[3]/ytmusic-search-page/ytmusic-tabbed-search-results-renderer/div[2]/ytmusic-section-list-renderer/div[2]/ytmusic-shelf-renderer[1]/div[2]/ytmusic-responsive-list-item-renderer/ytmusic-menu-renderer/tp-yt-paper-icon-button').click()
                driver.find_element_by_xpath('/html/body/ytmusic-app/ytmusic-popup-container/tp-yt-iron-dropdown/div/ytmusic-menu-popup-renderer/tp-yt-paper-listbox/ytmusic-menu-service-item-renderer[2]').click()

                # 검색창 비우기
                driver.find_element_by_xpath('/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-nav-bar/div[2]/ytmusic-search-box/div/div[1]/tp-yt-paper-icon-button[2]').click()
                time.sleep(1)
            except:
                # 홈으로 가기
                driver.find_element_by_xpath('/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-nav-bar/div[1]/a').click()
        time.sleep(10)
    except:
        print('서버를 확인해주세요.')
        break

driver.quit()