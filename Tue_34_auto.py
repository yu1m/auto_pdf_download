from selenium import webdriver
import chromedriver_binary
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import json


def to_panda_input(option,download_path):
    options=option
    options.add_argument('--incognito')
    options.add_argument('--headless')
    options.add_experimental_option("prefs",{
        "download.default_directory":download_path,
        "downloadd.prompt_for_download":False,
        "download.directory_upgrade":True,
        "plugins.plugins_disabled":["Chrome PDF Viewer"],
        "plugins.always_open_pdf_externally":True
    })
    url='https://panda.ecs.kyoto-u.ac.jp/portal/'
    driver=webdriver.Chrome(options=options)
    driver.get(url)
    driver.implicitly_wait(10)
    driver.find_element(By.ID,'loginLinks').click()
    sleep(1)
    return driver

def id_pass_get(filename):
    with open(filename) as f:
        json=json.load(f)
    ID=json['ID']
    PASSWORD=json['PASSWORD']
    return ID,PASSWORD

def id_pass_input(driver,ID,PASSWORD):
    id_input=driver.find_element(By.ID,'username')
    id_input.clear()
    id_input.send_keys(ID)
    pass_input=driver.find_element(By.ID,'password')
    pass_input.clear()
    pass_input.send_keys(PASSWORD)
    driver.find_element(By.CLASS_NAME,'btn-submit').click()
    sleep(1)

def to_classpage(driver):
    class_name=r"'[2022前期火４]確率統計解析及び演習(T1)'"
    driver.find_element(By.ID,'viewAllSites').click()
    url=driver.find_element(By.XPATH,f'//a[@title={class_name}]').get_attribute('href')
    driver.get(url)
    sleep(1)

def open_pdf(driver):
    button=driver.find_element(By.XPATH,"//a[contains(@title,'授業資料')]")
    button.click()
    sleep(1)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    driver.find_element(By.TAG_NAME,'tbody').find_elements(By.TAG_NAME,'tr')[-2].find_element(By.TAG_NAME,'a').click()
    driver.find_element(By.TAG_NAME,'tbody').find_elements(By.TAG_NAME,'tr')[-2].find_element(By.TAG_NAME,'a').click()
    sleep(2)


def main():
    #pdfの保存先を設定
    download_path='your own directory'
    
    #id,passwordをjsonファイルから取得
    ID=id_pass_get('your own file')
    PASSWORD=id_pass_get('your own file')
    
    #id,passwordの入力画面に移動
    driver=to_panda_input(Options(),download_path)

    #id,passwordを入力
    id_pass_input(driver,ID,PASSWORD)
    
    #授業のページに移動
    to_classpage(driver)
    
    #授業資料のページに移動しpdfを開く
    open_pdf(driver)
    
    driver.quit()
