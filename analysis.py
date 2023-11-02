import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import sys
import time
from pywinauto.keyboard import send_keys
import pywinauto
from bs4 import BeautifulSoup
import os

def upload(file_dir, file_name):
    app=pywinauto.Desktop()
    dlg = app["打开"]
    dlg["Toolbar3"].click()
    send_keys(file_dir)
    send_keys("{VK_RETURN}")
    dlg["文件名(&N):Edit"].type_keys(file_name)
    dlg["打开(&O)"].click()
    time.sleep(5)


def analysis(soup):
    result = {}
    keys = ["总结", "方法", "结论"]
    contents = soup.find_all(name='div',attrs={"class":'ml-[28px] mt-[12px] mb-[12px]'})
    for i, content in enumerate(contents):
        result[keys[i]] = content.text
    return result

if __name__  == "__main__":
    options = Options()
    # options.add_argument("--headless")
    browser = webdriver.Chrome(service=Service("./chromedriver.exe"), options=options)
    browser.get('https://paper.iflytek.com/')
    time.sleep(5)

    # user
    browser.find_element(By.XPATH, '//*[@id="loginName"]').send_keys(sys.argv[1])
    # password
    browser.find_element(By.XPATH, '//*[@id="password"]').send_keys(sys.argv[2])

    browser.find_element(By.XPATH, '//*[@id="login_button"]').click()
    time.sleep(5)
    
    browser.find_element(By.XPATH, "//*[contains(text(),'论文研读')]").click()
    time.sleep(5)
    df = pd.read_csv(sys.argv[3])

    if os.path.exists('analysis.csv'):
        results = pd.read_csv('analysis.csv', index_col=0)
    else:
        results = pd.DataFrame()
    for i, row in df.iterrows():
        if i < len(results):
            continue
        browser.find_element(By.XPATH, "//*[contains(text(),'上传文献')]").click()
        time.sleep(3)
        browser.find_element(By.XPATH, "//*[contains(text(),'浏览')]").click()
        time.sleep(1)
      
        upload(row['path'], row['file_name'])
        time.sleep(5)
        
        browser.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[6]/div/div/footer/span/div/button[1]').click()
        time.sleep(10)
        try:
            browser.find_element(By.XPATH, "//*[contains(text(),'{}')]".format(row['file_name'])).click()
            time.sleep(20)

            soup = BeautifulSoup(browser.page_source, 'html.parser')
            result = analysis(soup)
            result['name'] = row['name']
        except:
            result = {}
        results.loc[len(results)] = result
        pd.DataFrame(results).to_csv("analysis.csv")
        try:
            browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div/div[1]/div/button').click()
        except:
            continue
        time.sleep(2)

    pd.DataFrame(results).to_csv("analysis.csv")

