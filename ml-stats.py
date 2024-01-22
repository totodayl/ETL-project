import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import boto3
from datetime import date

class MobileLegendsStatsScraper:
    def __init__(self, url, bucket):
        self.url = url
        self.bucket = bucket
        self.header = ['Hero', 'Win Percentage', 'Popularity', 'Ban Ratio']
        self.s3 = boto3.client('s3')

    def configure_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def scrape_data(self):
        browser = self.configure_browser()

        # Navigate to the URL
        browser.get(self.url)

        # Sleep to capture the data
        time.sleep(2)

        # Get the page source after JavaScript execution
        page_source = browser.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        print(soup)

        # Get the table data
        table = soup.find('div', class_='slotwrapper').find_all('li')
        data = [self.extract_row_values(row) for row in table]

        df = pd.DataFrame(data, columns=self.header)
        filename = f'{str(date)}-ML_stats.csv'

        # Save to CSV
        df.to_csv(filename, index=False)

        # Upload to S3
        self.s3.upload_file(filename, self.bucket, filename)

        # Quit the browser
        browser.quit()

    def extract_row_values(self, row):
        values = row.find_all('div')
        return [value.text.strip() for value in values]

# URL and bucket name
url = 'https://m.mobilelegends.com/en/rank'
bucket = 'scrape-testbucket'

# Create an instance of the scraper
scraper = MobileLegendsStatsScraper(url, bucket)

# Start the scraping process
scraper.scrape_data()
