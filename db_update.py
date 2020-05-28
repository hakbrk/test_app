# import pandas as pd
# import yfinance as yf
# from datetime import datetime
# import dateutil.relativedelta
# from sqlalchemy import create_engine
# from tqdm import tqdm_notebook
# from selenium import webdriver
# from pandas.io.html import read_html
# import time
# from selenium import webdriver
# import os

# engine = create_engine('mysql+mysqlconnector://b299c42f0fdf61:fcdc6acd@us-cdbr-east-06.cleardb.net/heroku_826bb11c8d537f8')
# chrome_options = webdriver.ChromeOptions()
# chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--no-sandbox")
# driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

# query = """SELECT DISTINCT ticker FROM equity_history"""
# answer = pd.read_sql_query(query, engine)
# symb_list = answer['ticker'].tolist()
# print(symb_list)

# def import_yahoo(symbol):
#     equity_data = pd.DataFrame()
#     if symbol == 'Brent':
#         i = 0
#         for i in range(0,2):
#             try:
#                 chrome_options = webdriver.ChromeOptions()
#                 chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
#                 chrome_options.add_argument("--headless")
#                 chrome_options.add_argument("--disable-dev-shm-usage")
#                 chrome_options.add_argument("--no-sandbox")
#                 driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
#                 # driver = webdriver.Chrome(options=chrome_options)
#                 url = "https://markets.businessinsider.com/commodities/historical-prices/oil-price/usd?type=brent"
#                 driver.get(url)
#                 time.sleep(3)  
#                 table = driver.find_element_by_xpath('//*[@id="historic-price-list"]/div/div[2]/table/..')
#                 #table = driver.find_element_by_xpath('//*[@id="historic-price-list"]/div/div[2]/table/')
#                 table_html = table.get_attribute('innerHTML')
#                 equity_data = read_html(table_html)[0]
#                 equity_data = equity_data.set_index(pd.DatetimeIndex(equity_data['Date'])).drop(['Date'], axis=1).rename_axis('trade_date')
#                 equity_data = equity_data.rename(columns={"Closing Price": "close"})
#                 equity_data = equity_data['close'].reset_index().set_index('trade_date')
#                 driver.quit()
#             except:
#                 driver.quit()
#                 i += 1
#                 print(f"Still trying {2-i} more times.")

#     else:
#         equity_data = yf.download(symbol, start=(datetime.today()-dateutil.relativedelta.relativedelta(months=28)).strftime('%Y-%m-%d'), end=datetime.today().strftime('%Y-%m-%d')).rename_axis('trade_date')
#         equity_data = equity_data.rename(columns={"Close": "close"})
#         equity_data = equity_data['close'].reset_index().set_index('trade_date')
    
#     if not equity_data.empty:
#         # First part of the insert statement
#         insert_init = """insert into equity_history
#                 (trade_date, ticker, close)
#                 values
#                 """
#         # Add values for all days to the insert statement
#         if symbol == 'BZ':
#             symbol = 'Brent'
#         vals = ",".join(["""('{}', '{}', '{}')""".format(
#             str(trade_date),
#             symbol,
#             row.close
#         ) for trade_date, row in equity_data.iterrows()])

#         # Handle duplicates - Avoiding errors if you've already got some data in your table
#         insert_end = """ on duplicate key update
#             close=close;"""

#         # Put the parts together
#         query = insert_init + vals + insert_end

#         # Fire insert statement
#         engine.execute(query)

# for symb in symb_list:
#     import_yahoo(symb)

import pandas as pd
import yfinance as yf
import numpy as np
from datetime import datetime
import dateutil.relativedelta
from sqlalchemy import create_engine
from tqdm import tqdm_notebook
from selenium import webdriver
from pandas.io.html import read_html
import time
# from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import os
import mysql.connector
from webdriver_manager.chrome import ChromeDriverManager

GOOGLE_CHROME_PATH = '/testappjhawk/.apt/usr/bin/google_chrome'
CHROMEDRIVER_PATH = '/testappjhawk/.chromedriver/bin/chromedriver'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.binary_location = GOOGLE_CHROME_PATH
engine = create_engine('mysql+mysqlconnector://b299c42f0fdf61:fcdc6acd@us-cdbr-east-06.cleardb.net/heroku_826bb11c8d537f8')
# chrome_options = Options()
# chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--no-sandbox")


query = """SELECT DISTINCT ticker FROM equity_history"""
answer = pd.read_sql_query(query, engine)
symb_list = answer['ticker'].tolist()
print(symb_list)

def import_yahoo(symbol):
    equity_data = pd.DataFrame()
    if symbol == 'Brent':
        i = 0
        for i in range(0,2):
            try:
                # driver = webdriver.Chrome(options=chrome_options)
                # driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
                driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
                url = "https://markets.businessinsider.com/commodities/historical-prices/oil-price/usd?type=brent"
                driver.get(url)
                time.sleep(3)  
                table = driver.find_element_by_xpath('//*[@id="historic-price-list"]/div/div[2]/table/..')
                #table = driver.find_element_by_xpath('//*[@id="historic-price-list"]/div/div[2]/table/')
                table_html = table.get_attribute('innerHTML')
                equity_data = read_html(table_html)[0]
                equity_data = equity_data.set_index(pd.DatetimeIndex(equity_data['Date'])).drop(['Date'], axis=1).rename_axis('trade_date')
                equity_data = equity_data.rename(columns={"Closing Price": "close"})
                equity_data = equity_data['close'].reset_index().set_index('trade_date')
                driver.quit()
            except:
                driver.quit()
                i += 1
                print(f"Still trying {2-i} more times.")

    else:
        equity_data = yf.download(symbol, start=(datetime.today()-dateutil.relativedelta.relativedelta(months=28)).strftime('%Y-%m-%d'), end=datetime.today().strftime('%Y-%m-%d')).rename_axis('trade_date')
        equity_data = equity_data.rename(columns={"Close": "close"})
        equity_data = equity_data['close'].reset_index().set_index('trade_date')
    
    if not equity_data.empty:
        # First part of the insert statement
        insert_init = """insert into equity_history
                (trade_date, ticker, close)
                values
                """
        # Add values for all days to the insert statement
        if symbol == 'BZ':
            symbol = 'Brent'
        vals = ",".join(["""('{}', '{}', '{}')""".format(
            str(trade_date),
            symbol,
            row.close
        ) for trade_date, row in equity_data.iterrows()])

        # Handle duplicates - Avoiding errors if you've already got some data in your table
        insert_end = """ on duplicate key update
            close=close;"""

        # Put the parts together
        query = insert_init + vals + insert_end

        # Fire insert statement
        engine.execute(query)

for symb in symb_list:
    import_yahoo(symb)