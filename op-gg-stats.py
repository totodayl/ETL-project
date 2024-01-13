from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date
import s3_upload


# get todays date
today = date.today()
url = "https://www.op.gg/statistics/champions?period=day&position=jungle&region=ph"

#bucket name
bucket = 'op.gg-league-data'

# Use a headless browser
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)

# Navigate to the URL
driver.get(url)

# Get the page source after JavaScript execution
page_source = driver.page_source
df = []
columns = []
soup = BeautifulSoup(page_source, 'html.parser')
table_columns = soup.find('table', class_ = 'css-1eu6iti').find_all('tr')[0]
for i in table_columns:
    columns.append(i.text.strip())

table_row = soup.find('table', class_ = 'css-1eu6iti').find_all('tr')[1:]
for row in table_row:
    mt = []
    for i in row:
        mt.append(i.text.strip())
    df.append(mt)

df = pd.DataFrame(df,columns = columns)
df.set_index('#', inplace= True)
df.drop(columns=['KDA', 'CS', 'Gold'], inplace= True)

#converting to csv
filename = f'{str(today)}-LoL_stats.csv'
df.to_csv(filename, index=False)

#upload to s3
s3_upload.upload_file(filename,bucket, filename)

driver.quit()
