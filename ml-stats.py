from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date
import time

url = 'https://m.mobilelegends.com/en/rank'
df = []
header = ['Hero', 'Win Percentage','Popularity', 'Ban Ratio']


options = webdriver.ChromeOptions()
options.add_argument('--headless')

browser = webdriver.Chrome(options=options)
browser.get(url)


#need to sleep to capture the data
time.sleep(2)
page_source = browser.page_source
soup = BeautifulSoup(page_source, 'html.parser')

#get the date of the data
stats_date = soup.find('li', class_ = 'time').text.strip()

#get the table data
table = soup.find('div', class_ = 'slotwrapper').find_all('li')

for row in table:
    x = row.find_all('div')
    mt = []
    for value in x:
        mt.append(value.text.strip())
    df.append(mt)

df = pd.DataFrame(df, columns=header)





