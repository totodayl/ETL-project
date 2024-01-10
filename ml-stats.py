from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import s3_upload


url = 'https://m.mobilelegends.com/en/rank'
df = []
header = ['Hero', 'Win Percentage','Popularity', 'Ban Ratio']

#Configure the driver to headless
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
filename = f'{stats_date}-lol_stats.csv'
bucket = 'mobile-legends-data'

df.to_csv(filename, index=False)

#upload the file to s3
s3_upload.upload_file(filename,bucket, filename)





