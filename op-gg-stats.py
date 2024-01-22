import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date
import boto3

class LOLStatsScraper:
    def __init__(self, url, bucket):
        self.url = url
        self.bucket = bucket
        self.s3 = boto3.client('s3')
    def configure_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def scrape_data(self):
        driver = self.configure_browser()

        # Navigate to the URL
        driver.get(self.url)

        # Wait a little bit to fully load the site
        time.sleep(2)

        # Get the page source after JavaScript execution
        page_source = driver.page_source
        df = self.extract_data(page_source)

        # Convert to CSV
        filename = f'{str(date.today())}-LoL_stats.csv'
        df.to_csv(filename, index=False)

        # Upload to S3
        self.s3.upload_file(filename, self.bucket, filename)

        # Quit the browser
        driver.quit()

    def extract_data(self, page_source):
        soup = BeautifulSoup(page_source, 'html.parser')
        table_columns = soup.find('table', class_='css-1eu6iti').find_all('tr')[0]
        columns = [i.text.strip() for i in table_columns]

        table_row = soup.find('table', class_='css-1eu6iti').find_all('tr')[1:]
        data = [[i.text.strip() for i in row] for row in table_row]

        df = pd.DataFrame(data, columns=columns)
        df.set_index('#', inplace=True)
        df.drop(columns=['KDA', 'CS', 'Gold'], inplace=True)

        return df

# URL and bucket name
url = "https://www.op.gg/statistics/champions?period=day&position=jungle&region=ph"
bucket = 'op.gg-league-data'

# Create an instance of the scraper
scraper = LOLStatsScraper(url, bucket)

# Start the scraping process
scraper.scrape_data()