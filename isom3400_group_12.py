"""
@course: ISOM3400 L1
@Group number: 12
@Group member: MAN, Chee Yan (20690722)
@Group member: MAN, Chun Kit (20600284)
@Group member: NGUYEN, Le Cam Van (20519019)
@Group member: SO, Hing Kiu (20688949)
@Group member: TAM, Jessie Hoi Ying (20697990)
"""
#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from yahoo_finance import yahoo_finance_website
import numpy as np
import csv
from textblob import TextBlob
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd
import pytz

#%%
class finance_yahoo_com(yahoo_finance_website):

    def __init__(self, stocknum):
        yahoo_finance_website.__init__(self, 'https://finance.yahoo.com')
        self.stocknum = stocknum
        self.endProgram = False
        self.width = 44
        self.option = {"1": 'Extract Summary Page', "2":'Extract Conversation Page', "3":'Extract Statistic Page', "4":'Extract Sustainability Page',"5":'Search for another stock code',"6":'Exit'}

    # Extract the code of the stock using sname() for further uses
    def sname(self):
        stock=self.driver.find_element_by_css_selector("#quote-header-info > div.Mt\(15px\) > div.D\(ib\).Mt\(-5px\).Mend\(20px\).Maw\(56\%\)--tab768.Maw\(52\%\).Ov\(h\).smartphone_Maw\(85\%\).smartphone_Mend\(0px\) > div.D\(ib\) > h1").text
        stock=stock.split('(')[1][:-1]
        return stock

    def dataSummary(self,stocknum):
        self.driver.get(f"https://finance.yahoo.com/quote/{obj.sname()}")
        filename=self.stocknum.replace('.','')+'.csv'
        try:
            # Wait until the page is fully loaded
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="quote-summary"]/div[1]/table/tbody/tr[7]/td[2]/span')))  
            
            # Locate the data using Xpath
            data_close=self.driver.find_element_by_xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[1]/td[2]/span')
            data_volume=self.driver.find_element_by_xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[7]/td[2]/span')
            data_beta=self.driver.find_element_by_xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[2]/td[2]/span')
            data_pe=self.driver.find_element_by_xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[3]/td[2]/span')
            data_low=self.driver.find_element_by_xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[6]/td[2]')
            data_date=self.driver.find_element_by_xpath('//*[@id="quote-market-notice"]/span')
            data_price=self.driver.find_element_by_xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div/span[1]')
            # Use datetime for current time and date
            now=datetime.now()
            
            # Creating a dictionary to store the data
            dataSum={}
            dataSum['Price']=data_price.text
            dataSum['Volume']=data_volume.text
            dataSum['Previous Close']=data_close.text
            dataSum['Beta']=data_beta.text
            dataSum['PE']=data_pe.text
            dataSum['52 Week Low']=data_low.text.split('-')[0]
            dataSum['52 Week High']=data_low.text.split('-')[1]
            dataSum['Time']=now.strftime("%H:%M:%S")
            dataSum['Date']=now.date()
                                
            fieldnames=['Date','Time','Price','Volume','Previous Close','Beta','PE','52 Week Low','52 Week High']
            with open(filename,'w') as f:
                csv_writer=csv.DictWriter(f,fieldnames=fieldnames)
                csv_writer.writeheader()
                csv_writer.writerow(dataSum)
                
        except Exception:
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['No information is found.'])
    
    def check_YahooFinance_site(self):
        try:
            assert "Yahoo Finance" in self.driver.title
            return True

        except:
            self.endProgram = True
            return False
    
    def search(self):
        try:
            while True:
                # Enter stocknum in the search bar
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "yfin-usr-qry")))
                element = self.driver.find_element_by_id("yfin-usr-qry")
                element.clear()
                element.send_keys(self.stocknum)
                # If no suggestion is found in the search bar, ask the user to enter again
                WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="result-quotes-0"]/div[1]/div[1]')))
                # set the initial values
                last = 0
                stock_list = []
                type_list = []
                no_equity = True
                time.sleep(2)
                # generate a list of suggested codes and the corresponding type
                for i in range(0,6):
                    try:
                        if self.driver.find_element_by_xpath(f'//*[@id="result-quotes-{i}"]/div[1]/div[1]').text != "":
                            last = i
                    except:
                        break
                    if self.driver.find_element_by_xpath(f'//*[@id="result-quotes-{i}"]/div[1]/div[1]').text == "PRIVATE":
                            stock_list.append(self.driver.find_element_by_xpath(f'//*[@id="result-quotes-{i}"]/div[1]/div[2]').text[0:20])
                            type_list.append("PRIVATE")
                    else:
                            stock_list.append(self.driver.find_element_by_xpath(f'//*[@id="result-quotes-{i}"]/div[1]/div[1]').text)
                            type_list.append(self.driver.find_element_by_xpath(f'//*[@id="result-quotes-{i}"]/div[2]/span').text)
                            if "Equity" in type_list[i]:
                                no_equity = False
                
                # if no equity is found, ask the user to enter again
                if no_equity:
                    self.stocknum = input('Error. No equity is found. Please input again: ')
                    continue
                
                # if there is only one suggestion and it's an exact match to the stock code, directly go to the page of that stock
                elif stock_list[last] == self.stocknum and last == 0:
                    choice_button = self.driver.find_element_by_xpath('//*[@id="result-quotes-0"]/div[1]/div[1]')
                    choice_button.click()
                    break

                # interface listed all suggestions from the search bar
                print("##################################################")
                print("## {} ##".format("".center(self.width)))
                print("## {} ##".format(f"Select a stock(e.g. 1 for {stock_list[0]}).".center(self.width)))
                print("## {} ##".format("".center(self.width)))
                print("## {} ##".format("0. Search for another stock".ljust(self.width)))
                choice_num = 1
                for i in range(0,last+1):
                    choice_display = str(choice_num) +". " + stock_list[i] + " (" + type_list[i] + ")"
                    print("## {} ##".format(choice_display.ljust(self.width)))
                    choice_num +=1
                print("## {} ##".format("".center(self.width)))
                print("##################################################\n")
                
                # enter 0 if none of the suggestion is suitable/ enter a choice in 1-6
                while True:
                    try:
                        choice = int(input("Please enter your choice:"))
                        if choice == 0:
                            break
                        choice -=1
                        choice_button = self.driver.find_element_by_xpath(f'//*[@id="result-quotes-{choice}"]/div[1]/div[1]')
                        if 'Equity' not in type_list[choice] and choice in [1,2,3,4,5,6]:
                            raise RuntimeError
                    except RuntimeError:
                        print("Error. Only equity is accepted. Please try again.")
                    except:
                        print("Error. invalid input. Please try again.")
                    else:
                        break
                
                # Go to the required page
                self.stocknum = stock_list[choice]
                choice_button.click()
                break
        
        # Ask the user to enter again
        except:
            self.stocknum = input('Please input a stock code (e.g. 0700.HK/0700): ')
            self.search()
            
    def conversations(self):
        try:
            # go to conversation page
            self.driver.get(f"https://finance.yahoo.com/quote/{obj.sname()}/community")
            
            # wait for elements to load
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="canvass-0-CanvassApplet"]/div/ul/li[*]/div/div[1]/span')))
            
            # extract elements required
            name = self.driver.find_elements_by_xpath('//*[@id="canvass-0-CanvassApplet"]/div/ul/li[*]/div/div[1]/button')
            date = self.driver.find_elements_by_xpath('//*[@id="canvass-0-CanvassApplet"]/div/ul/li[*]/div/div[1]/span')
            comment = self.driver.find_elements_by_xpath('//*[@id="canvass-0-CanvassApplet"]/div/ul/li[*]/div/div[2]/div[1]')
            like = self.driver.find_elements_by_xpath('//*[@id="canvass-0-CanvassApplet"]/div/ul/li[*]/div/div[*]/div[2]/button[1]')
            dislike = self.driver.find_elements_by_xpath('//*[@id="canvass-0-CanvassApplet"]/div/ul/li[*]/div/div[*]/div[2]/button[2]')
            analysisPol = []
            analysisSub = []

            #changing elements into text
            for index,item in enumerate(name):
                name[index] = item.text

            for index,item in enumerate(like):
                like[index] = item.text

            for index,item in enumerate(dislike):
                dislike[index] = item.text

            # source: https://stackoverflow.com/questions/47082673/add-days-in-datetime-and-convert-to-string-format-in-python    
            for index, i in enumerate(date):             
                # days ago in date
                if "days ago" in i.text:
                    for word in i.text.split():
                        if word.isdigit():
                            numbers= int(word)
                            realtimedata = datetime.today()-timedelta(days=numbers)
                            date[index] = realtimedata.strftime("%I""%p"","" %d"","" %b"" %Y")
                # minutes ago in date
                elif "minutes ago" in i.text:
                    for word in i.text.split():
                        if word.isdigit():
                            numbers= int(word)
                            realtimedata = datetime.today()-timedelta(minutes=numbers)
                            realtimedata = realtimedata.astimezone(pytz.timezone('Etc/GMT+8'))
                            date[index] = realtimedata.strftime("%I""%p"","" %d"","" %b"" %Y")

                # 1 minute ago in date
                elif "1 minute ago" in i.text:
                    numbers = 1
                    realtimedata = datetime.today()-timedelta(minutes=numbers)
                    realtimedata = realtimedata.astimezone(pytz.timezone('Etc/GMT+8'))
                    date[index] = realtimedata.strftime("%I""%p"","" %d"","" %b"" %Y")
                    
                # hours ago in date
                elif "hours ago" in i.text:
                    for word in i.text.split():
                        if word.isdigit():
                            numbers= int(word)
                            realtimedata = datetime.today()-timedelta(hours=numbers)
                            realtimedata = realtimedata.astimezone(pytz.timezone('Etc/GMT+8'))
                            date[index] = realtimedata.strftime("%I""%p"","" %d"","" %b"" %Y")
                
                # 1 hour ago in date
                elif "hour ago" in i.text:
                    numbers = 1
                    realtimedata = datetime.today()-timedelta(hours=numbers)
                    realtimedata = realtimedata.astimezone(pytz.timezone('Etc/GMT+8'))
                    date[index] = realtimedata.strftime("%I""%p"","" %d"","" %b"" %Y")

                # months ago in date
                elif "months ago" in i.text:
                    for word in i.text.split():
                        if word.isdigit():
                            numbers= int(word)
                            realtimedata = datetime.today()-relativedelta(months=numbers)
                            date[index] = realtimedata.strftime("%I""%p"","" %d"","" %b"" %Y")
                
                # 1 month ago in date
                elif "last month" in i.text:
                    numbers = 1
                    realtimedata = datetime.today()-relativedelta(months=numbers)
                    date[index] = realtimedata.strftime("%I""%p"","" %d"","" %b"" %Y")

                # yesterday in date
                elif "yesterday" in i.text:
                    numbers = 1
                    realtimedata = datetime.today()-timedelta(days=numbers)
                    date[index] = realtimedata.strftime("%I""%p"","" %d"","" %b"" %Y")

                # last year in date
                elif "last year" in i.text:
                    numbers = 1
                    realtimedata = datetime.today()-relativedelta(years=numbers)
                    date[index] = realtimedata.strftime("%I""%p"","" %d"","" %b"" %Y")
                
                # years ago in date
                elif "years ago" in i.text:
                    for word in i.text.split():
                        if word.isdigit():
                            numbers= int(word)
                            realtimedata = datetime.today()-relativedelta(years=numbers)
                            date[index] = realtimedata.strftime("%I""%p"","" %d"","" %b"" %Y")

                # seconds ago in date
                elif "seconds ago" in i.text:
                    numbers = 1
                    realtimedata = datetime.today()-relativedelta(seconds=numbers)
                    realtimedata = realtimedata.astimezone(pytz.timezone('Etc/GMT+8'))
                    date[index] = realtimedata.strftime("%I""%p"","" %d"","" %b"" %Y")   
                    
                # error is found
                else:
                    print("Error detected.")

            # textblob
            # source: https://stackabuse.com/sentiment-analysis-in-python-with-textblob/
            for i in comment:
                # polarity of each comment
                analysisPol.append(round(TextBlob(i.text).polarity,4))
                #subjectivity of each comment
                analysisSub.append(round(TextBlob(i.text).subjectivity,4))
            
            # create dictionary for all elements
            dictionary = {'Name': name, 'Time': date, 'Polarity': analysisPol, 'Subjectivity': analysisSub, 'Like' : like, 'Dislike' : dislike }
        
        except:
            # create a csv file and save nothing
            conversations_filename = self.stocknum.replace('.','')+'_Conversation.csv'

            # Source: https://www.programiz.com/python-programming/csv
            with open(conversations_filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['No information is found.'])
        
        # save data in csv file if information is found
        else:            
            # pandas dataframe        
            df = pd.DataFrame.from_dict(dictionary, orient='index')
            df = df.transpose()

            conversations_filename = self.stocknum.replace('.','')+'_Conversation.csv'
            
            # put pandas dataframe to csv file
            df.to_csv(conversations_filename, index = False)
            
            # if there is no likes/dislike, fill it with 0
            df = pd.read_csv(conversations_filename)
            df['Like'].fillna(0,inplace=True)
            df['Dislike'].fillna(0,inplace=True)

            # skip lines and update csv file
            # source: https://stackoverflow.com/questions/39114382/pandas-insert-alternate-blank-rows
            nans = np.where(np.empty_like(df.values), np.nan, np.nan)
            data = np.hstack([nans, df.values]).reshape(-1, df.shape[1])
            df = pd.DataFrame(data, columns=df.columns)
            df.to_csv(conversations_filename, index = False) 
     
    def statistics(self):
        try:
            # direct to Statistics page using a link
            self.driver.get(f"https://finance.yahoo.com/quote/{obj.sname()}/key-statistics")
            # create dictionaries for the statistics
            stockPriceHistory_dict = {'Beta (5Y Monthly)':'', '52-Week Change':'', 'S&P500 52-Week Change':'', 
                                        '52 Week High':'', '52 Week Low':'', '50-Day Moving Average':'', '200-Day Moving Average':''}

            shareStatistics_dict = {'Avg Vol (3 month)':'', 'Avg Vol (10 day)':'', 'Shares Outstanding':'', 'Float':'', 
                                        'Percentage Held by Insiders':'', 'Percentage Held by Institutions':'', 
                                        'Shares Short':'', 'Short Ratio':'', 'Short Percentage of Float':'', 
                                        'Short Percentage of Shares Outstanding':'', 'Shares Short (prior month)':''}

            dividendsSplits_dict = {'Forward Annual Dividend Rate':'', 'Forward Annual Dividend Yield':'', 
                                        'Trailing Annual Dividend Rate':'', 'Trailing Annual Dividend Yield':'', 
                                        '5 Year Average Dividend Yield':'', 'Payout Ratio':'', 'Dividend Date':'', 
                                        'Ex-Dividend Date':'', 'Last Split Factor':'', 'Last Split Date':''}

            # setting for WebDriverWait
            wait50 = WebDriverWait(self.driver, 50)
            presnece = EC.presence_of_element_located

            # collect data and save in csv file
            # collect data from Statistics page
            # section: stock price history
            for iStock, kStock in enumerate(list(stockPriceHistory_dict.keys())):
                xpathStock = '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[2]/div/div[1]/div/div/table/tbody/tr[' + str(iStock+1) + ']/td[2]'
                wait50.until(presnece((By.XPATH, xpathStock)))
                stockPriceHistory_dict[kStock] = self.driver.find_element_by_xpath(xpathStock).text

            # section: share statistics
            for iShare, kShare in enumerate(list(shareStatistics_dict.keys())):
                xpathShare = '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[2]/div/div[2]/div/div/table/tbody/tr[' + str(iShare+1) + ']/td[2]'
                wait50.until(presnece((By.XPATH, xpathShare)))
                shareStatistics_dict[kShare] = self.driver.find_element_by_xpath(xpathShare).text

            # section: dividends & splits
            for iDiv, kDiv in enumerate(list(dividendsSplits_dict.keys())):
                xpathDiv = '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[2]/div/div[3]/div/div/table/tbody/tr[' + str(iDiv+1) + ']/td[2]'
                wait50.until(presnece((By.XPATH, xpathDiv)))
                dividendsSplits_dict[kDiv] = self.driver.find_element_by_xpath(xpathDiv).text
            
            # amend the format of data displayed
            dicts = [stockPriceHistory_dict, shareStatistics_dict, dividendsSplits_dict]

            for dict in dicts:
                for k, v in dict.items():
                    # extract the last character of the value
                    last_char = v[-1]

                    # check whether the last character is the percentage symbol
                    # convert percentage into decimal number if yes
                    if last_char == '%':
                        v_num = float(v[:len(v)-1])
                        v_new = v_num / 100 
                        dict[k] = str(v_new)

                    # check whether the last character is capital M
                    # convert million into number if yes
                    elif last_char == 'M':
                        v_num = float(v[:len(v)-1])
                        v_new = int(v_num * 1000000)
                        dict[k] = str(v_new)

                    # check whether the last character is capital B
                    # convert billion into number if yes
                    elif last_char == 'B':
                        v_num = float(v[:len(v)-1])
                        v_new = int(v_num * 1000000000)
                        dict[k] = str(v_new)

                    # check whether the value is N/A
                    # convert N/A into nan if yes
                    elif v == 'N/A':
                        v_new = np.nan
                        dict[k] = str(v_new)          

        # execute if the page does not have any information
        except:
            # create a csv file and save nothing
            statistics_filename = self.stocknum.replace('.', '') + '_statistics.csv'

            # Source: https://www.programiz.com/python-programming/csv
            with open(statistics_filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['No information is found.'])
        
        # save data in csv file if information is found
        else:
            dict_titles = ['Stock Price History', 'Share Statistics', 'Dividends Splits']

            # create a csv file
            statistics_filename = self.stocknum.replace('.', '') + '_statistics.csv'
        
            with open(statistics_filename, 'w') as file:

                writer_title = csv.writer(file)
                
                for iDict in range(len(dicts)):
                    # the title of the dictionary
                    writer_title.writerow([dict_titles[iDict]])

                    # the corresponding data of the section
                    statistics_fieldnames = list(dicts[iDict].keys())
                    writer_data = csv.DictWriter(file, fieldnames=statistics_fieldnames)
                    writer_data.writeheader()
                    writer_data.writerow(dicts[iDict])

        return False

    def sustinfo(self,stocknum):
        self.driver.get(f"https://finance.yahoo.com/quote/{obj.sname()}/sustainability")
        # Save the file name first   
        filename = self.stocknum.replace('.', '') + '_sustainability.csv'

        # if no sust info is found, create a csv file and save nothing. Otherwise save the sust info  
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="Col1-0-Sustainability-Proxy"]/section/div[1]/div/div[1]/div/div[2]/div[1]')))
        except:
            # Source: https://www.programiz.com/python-programming/csv
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['No information is found.'])
        else:
            data_total=self.driver.find_element_by_xpath('//*[@id="Col1-0-Sustainability-Proxy"]/section/div[1]/div/div[1]/div/div[2]/div[1]')
            data_type=self.driver.find_element_by_xpath('//*[@id="Col1-0-Sustainability-Proxy"]/section/div[1]/div/div[1]/div/div[3]/div/span')
            data_percentile=self.driver.find_element_by_xpath('//*[@id="Col1-0-Sustainability-Proxy"]/section/div[1]/div/div[1]/div/div[2]/div[2]/span/span')
            data_ers=self.driver.find_element_by_xpath('//*[@id="Col1-0-Sustainability-Proxy"]/section/div[1]/div/div[2]/div/div[2]/div[1]')
            data_srs=self.driver.find_element_by_xpath('//*[@id="Col1-0-Sustainability-Proxy"]/section/div[1]/div/div[3]/div/div[2]/div[1]')
            data_grs=self.driver.find_element_by_xpath('//*[@id="Col1-0-Sustainability-Proxy"]/section/div[1]/div/div[4]/div/div[2]/div[1]')
            data_mclevel=self.driver.find_element_by_xpath('//*[@id="Col1-0-Sustainability-Proxy"]/section/div[2]/div[2]/div/div/div/div[1]/div')

            # Make a dictionary with all required info                       
            sustinfo={}
            sustinfo['Total']=data_total.text
            sustinfo['Type']=data_type.text
            sustinfo['Percentile']=data_percentile.text.split(next(filter(str.isalpha, data_percentile.text)))[0]
            sustinfo['ERS']=data_ers.text
            sustinfo['SRS']=data_srs.text
            sustinfo['GRS']=data_grs.text
            sustinfo['mclevel']=data_mclevel.text

            # generate the required csv file
            fieldnames=['Total','Type','Percentile','ERS','SRS','GRS','mclevel']         
            with open(filename,'w') as file:
                csv_writer=csv.DictWriter(file,fieldnames=fieldnames)
                csv_writer.writeheader()
                csv_writer.writerow(sustinfo)
        return False


    def userinterface(self):
        while not self.endProgram:
            # menu page
            menuoption = ""
            
            while not menuoption in self.option.keys():
                print("##################################################")
                print("## {} ##".format("".center(self.width)))
                print("## {} ##".format(f"Stock {obj.sname()}: Please select service.".center(self.width)))
                print("## {} ##".format("".center(self.width)))
                for k,v in self.option.items():
                    print("## {}. {} ##".format(k,v.ljust(self.width-len(str('.  ')))))
                print("## {} ##".format("".center(self.width)))
                print("## {} ##".format("#"*self.width))
                menuoption = input("Enter the option: ")

            else:
              # extract data summary page
                if menuoption == "1":
                    del self.option[menuoption]
                    self.endProgram = self.dataSummary(stocknum)
                    print('Summary Page is Extracted!')
                    input("Press Enter to continue...")

              # extract conversation page
                elif menuoption == "2":
                    del self.option[menuoption]
                    
                    self.endProgram = self.conversations()
                    print('Conversation Page is Extracted!')
                    input("Press Enter to continue...")

              # extract statistic page     
                elif menuoption == "3":
                    del self.option[menuoption]
                    self.endProgram = self.statistics()
                    print('Statistic Page is Extracted!')
                    input("Press Enter to continue...")

              # extract sustainability page     
                elif menuoption == "4":
                    del self.option[menuoption]
                    self.endProgram = self.sustinfo(stocknum)
                    print('Sustainability Page is Extracted!')
                    input("Press Enter to continue...")
              
              # search for another stock
                elif menuoption == "5":
                    self.option = {"1": 'Extract Summary Page', "2":'Extract Conversation Page', "3":'Extract Statistic Page', "4":'Extract Sustainability Page',"5":'Search for another stock code',"6":'Exit'}
                    self.stocknum = input('Please input a stock code (e.g. 0700.HK/0700): ')
                    self.driver.get("https://finance.yahoo.com")
                    self.endProgram = self.search()
                    obj.sname()
                    print(f'Searched for stock code {self.stocknum}')
                    input("Press Enter to continue...")
              
              # program ends      
                elif menuoption == "6":
                    self.endProgram = True

        print("Bye!")
        input("Press Enter to end the program...")
        
stocknum = input('Please input a stock code (e.g. 0700.HK/0700): ')
obj = finance_yahoo_com(stocknum)
#%%
obj.search()
#%%
obj.sname()
obj.check_YahooFinance_site()
# %%
obj.userinterface()