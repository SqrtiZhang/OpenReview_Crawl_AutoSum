from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import re
import io 
import os
import sys
import pandas as pd
import time
from tqdm import tqdm

def del_special_ch(str1):
    a = re.findall(r'[^\*"/:?\\|<> !\-\(\)]',str1,re.S) 
    a = "".join(a)
    return a


if __name__ == "__main__":
    
    options = Options()
    options.add_argument("--headless")
    browser = webdriver.Chrome(service=Service("./chromedriver.exe"), options=options)
    browser.get('https://openreview.net/')
    search_key = sys.argv[1]

    time.sleep(10)
    browser.find_element(By.XPATH, '//*[@id="navbar"]/form/div/input').send_keys(search_key)
    browser.find_element(By.XPATH, '//*[@id="navbar"]/form/div/input').send_keys(Keys.ENTER)

    time.sleep(10)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    pages = set()
    for link in soup.find_all('a',href=re.compile("content=all")):
        try:
            pages.add(int(link.text))
        except:
            continue

    links = []
    names = []
    for page in pages:
        browser.find_element(By.XPATH, "//a[contains(@href, 'page={}')]".format(page)).click()
        time.sleep(3)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        for pdf in soup.find_all('h4'):
            link = pdf.find_all('a', class_='pdf-link')
            name = pdf.text
            if link:
                links.append(link[0].get('href'))
                names.append(name)   

    df = pd.DataFrame()
    df['name'] = names
    df['url'] = links
    
    df['file_name'] = ""
    # pdf_dir = r"C:\Users\zhangyongting\Desktop\work\openreview\pdf"
    pdf_dir = sys.argv[2]
    df['path'] = [pdf_dir] * len(links)

    with tqdm(total=len(links)) as pbar:

        for i in range(len(links)):
            file_name = del_special_ch(names[i]) + ".pdf"
            file_path = os.path.join(pdf_dir, file_name)
            df.loc[i, 'file_name'] = file_name
            if os.path.exists(file_path):
                pbar.update(1)
                continue

            result = requests.get("https://openreview.net/" + links[i])
            pdf_content = io.BytesIO(result.content)
            with open(file_path, 'wb') as file:  
                file.write(pdf_content.read())
            pbar.update(1)
    
    df.to_csv("crawl.csv")