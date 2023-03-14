#yahoo_finance.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Source: https://stackoverflow.com/questions/53657215/running-selenium-with-headless-chrome-webdriver
# Source: https://stackoverflow.com/questions/47751529/how-do-i-suppress-console-cmd-error-messages-in-python
chrome_options = Options()
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument('--hide-scrollbars')
chrome_options.add_argument('blink-settings=imagesEnabled=false')

class yahoo_finance_website(object):
    def __init__(self, link):
        self.url = link
        self.connection()
    
    def check_YahooFinance_site(self):
        # This function needs to be overrided by student's program
        # The function returns True if this is YahooFinance site
        # Otherwise it returns False 
        print("This is Demo program")
        return False

    def connection(self):
        self.driver = webdriver.Chrome("chromedriver.exe",options=chrome_options)
        self.driver.get(self.url)
    
    def __del__(self):
        print("Destructor is executed!!!")
        self.driver.close()
    
    def __str__(self):
        return "(Demo) This is Yahoo Finance."


if __name__ == '__main__':
    asg2_obj = yahoo_finance_website('https://finance.yahoo.com')
    print(asg2_obj)
    
    if asg2_obj.check_YahooFinance_site():
        print("This is Yahoo finance (confirmed by Selenium)")
    else:
        print("This is NOT Yahoo finance (confirmed by Selenium)")