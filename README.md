# Data-Mining
The code is using Selenium library and Yahoo Finance API to extract information about a stock from Yahoo Finance website. The information is then stored in a csv file. The code includes the following classes/functions:

finance_yahoo_com(yahoo_finance_website): This class is used to extract the data. There are several functions in this class:

* `sname`(): Extract the code of the stock using xpath() method for further uses.
* `dataSummary(stocknum)`: This function extracts the data for a given stock code and then saves it to a csv file.
* `check_YahooFinance_site()`: This function checks whether the browser is in Yahoo Finance page or not.
* `search()`: This function searches the inputted stock code and, if found, goes to the required page.
* `conversations()`: This function extracts and saves in a csv file the analysis of the conversations about the stock on the Yahoo Finance website.
* `statistics()` : Search for Stock Price History, Share Statistics, Dividends data and to csv
* `sustinfo()`: Search for Sustainability data



Other libraries imported are:

* `webdriver (Selenium)`: A tool that controls a web browser through Python programs to automate website testing.
* `yahoo_finance_website`: A Yahoo Finace API to get stock data.
* `numpy`: A Python library used for working with arrays.
* `csv`: A module that implements classes to read and write tabular data in CSV (Comma Separated Values) format.
* `textblob`: A Python library for processing textual data.
* `time`: A library that provides various time-related functions.
* `datetime`: A module supplied by Python that provides classes to work with dates and times.
* `relativedelta`: A class in dateutil module that is used to generate relative data.
* `pandas`: A software library for data manipulation and analysis.
* `pytz`: A Python module that is used to work with timezone information provided by the Olson Database.


## Selenium with financial data on Yahoo Finance Documentation

This program uses selenium to extract financial data from Yahoo Finance. It also includes class inheritance, web scraping, and sentiment analysis.

### Requirements
* [Selenium](https://selenium-python.readthedocs.io/)
* [yahoo_finance](https://pypi.org/project/yahoo-finance/)
* Numpy
* Pandas
* TextBlob

### Usage
1. Make sure the required packages and Python have been properly installed.
2. Run the program.
3. Type `stocknum` (e.g. 0700.HK/0700) in the terminal.
4. Enter the integer corresponding to the webpage to be extracted.
5. Wait for the program to extract the data and save it into a csv file.

### Program Logic
1. Import necessary libraries.
2. Create a `yahoo_finance_website` class that automates a web browser to retrieve website content using the Yahoo Finance website's URL.
3. Create a `finance_yahoo_com` class that inherits the methods and attributes of `yahoo_finance_website`. Additionally, `finance_yahoo_com` contains member variables to store and manipulate input data.
4. Define `sname()` to extract the required stock code for further extraction from Yahoo Finance's website.
5. Define `dataSummary(self,stocknum)` to extract financial data from a summary web page and save it in a csv file.
6. Define `check_YahooFinance_site()` to check if the current web page is Yahoo Finance's site.
7. Define `search()` to search Yahoo Finance for a stock code to extract financial data.
8. Define `conversations()` to extract users' comments' time, their sentiment polarity score, and create a csv file to save the data.
9. Use `if __name__ == "__main__":` to run the program.




## This is a school based project for Web Scrapping using Selenium with OOP
## Interface
1. `dataSummary`: allows users to extract the data summary page for the specified stock;
2. `conversations`: allows users to extract the conversations page for the specified stock;
3. `statistics`: allows users to extract the statistics page for the specified stock; and
4. `sustinfo`: allows users to extract the sustainability page for the specified stock.

In addition, there is a function to start the program, called userinterface.

#### How to use
After importing this class, create an object and run the function `userinterface()`. The program will display a menu for the user to select one of four options, as well as an option to exit the program. The options correspond to the four functions listed above. Once a function is selected, the program will extract the relevant data and save the output as a CSV file. The output file can then be found in the working directory.

#### Example inputs and outputs
For example, if the user inputs 0700 as the stock code, the output files will be named '0700_summary.csv', '0700_conversations.csv', '0700_statistics.csv', and '0700_sustainability.csv'.

If the user selects option `1`, the output file will contain the `data summary page` for the specified stock code.

If the user selects option `2`, the output file will contain the `conversations page` for the specified stock code.

If the user selects option `3`, the output file will contain the `statistics page` for the specified stock code.

If the user selects option `4`, the output file will contain the `sustainability page` for the specified stock code.

If the user selects option `5`, they will be prompted to input another stock code.

If the user selects option `6`, the program will end.
