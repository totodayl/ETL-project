from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date

# get todays date
today = date.today()
url = "https://www.op.gg/statistics/champions?position=jungle&region=ph&period=week&tier=all"

# Use a headless browser
options = webdriver.ChromeOptions()
options.add_argument('--headless')
browser = webdriver.Chrome(options=options)

# Navigate to the URL
browser.get(url)

# Get the page source after JavaScript execution
page_source = browser.page_source
df = []
columns = []
soup = BeautifulSoup(page_source, 'html.parser')
table_columns = soup.find('table', class_ = 'css-1eu6iti ek4t1l70').find_all('tr')[0]
for i in table_columns:
    columns.append(i.text.strip())

table_row = soup.find('table', class_ = 'css-1eu6iti ek4t1l70').find_all('tr')[1:]
for row in table_row:
    mt = []
    for i in row:
        mt.append(i.text.strip())
    df.append(mt)

df = pd.DataFrame(df,columns = columns)
df.set_index('#', inplace= True)
df.drop(columns=['KDA', 'CS', 'Gold'], inplace= True)
print(type(today))
print(df)
    