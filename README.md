# Data-Mining

This is a school based project for Web Scrapping using Selenium with OOP.



Parent Class is finance_yahoo_com(yahoo_finance_website)

Functions inlcude:
__init__(self,stocknum) 
sname()
It checks with the functions and stock/ETF entered, automate searching in Yahoo Finance Page.

dataSummary(self,stocknum)
It checks with css selector and xpath selector in html, creates dictionary for the data, convert the data in csv file for data summary page.

check_YahooFinance_site(self)
It checks whether the driver successfully go to correct code page with destructor


search(self)
Display search results in flexible 
Fix bugs for empty types for the stock entered

conversations(self)
Check with user comments and store them into dictionary according to time.
Use Textblob for sentiments, polarity analysis on text.
Use Pandas to transpose Dictionary to csv is data is found.


statistics(self)
Search for Stock Price History, Share Statistics, Dividends data and to csv

sustinfo(self,stocknum)
Sustainability data

userinterface(self)


