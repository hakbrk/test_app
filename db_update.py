import pandas as pd
import yfinance as yf
from datetime import datetime
import dateutil.relativedelta
from tqdm import tqdm_notebook
from selenium import webdriver
from pandas.io.html import read_html
import time
from selenium.webdriver.chrome.options import Options
import mysql.connector

def update_db():
    engine = mysql.connector.connect(
    host="us-cdbr-east-06.cleardb.net",
    user="b299c42f0fdf61",
    passwd="fcdc6acd",
    database="heroku_826bb11c8d537f8"
    )
    cursor = engine.cursor()
    # df = pd.DataFrame()
    # query = """SELECT DISTINCT ticker FROM equity_history"""
    # answer = pd.read_sql_query(query, engine)
    # tick_list = answer['ticker'].tolist()
    tick_list = ['Brent', 'NE', 'PACD', 'SDRL', 'VAL', 'RIG', 'DO']
    # print(tick_list)
    for tick in tick_list:
        equity_data = pd.DataFrame()
        if tick == 'Brent':
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            i = 0
            for i in range(0,2):
                try:
                    driver = webdriver.Chrome(options=chrome_options)
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
                    break
                except:
                    driver.quit()
                    i += 1
                    print(f"Still trying {2-i} more times.")
        else:
            equity_data = yf.download(tick, start=(datetime.today()-dateutil.relativedelta.relativedelta(months=28)).strftime('%Y-%m-%d'), end=datetime.today().strftime('%Y-%m-%d')).rename_axis('trade_date')
            equity_data = equity_data.rename(columns={"Close": "close"})
            equity_data = equity_data['close'].reset_index().set_index('trade_date')
            
        if not equity_data.empty:
            # First part of the insert statement
            insert_init = """insert into equity_history
                    (trade_date, ticker, close)
                    values
                    """
            # Add values for all days to the insert statement
            if tick == 'BZ':
                tick = 'Brent'
            vals = ",".join(["""('{}', '{}', '{}')""".format(
                str(trade_date),
                tick,
                row.close
            ) for trade_date, row in equity_data.iterrows()])

            # Handle duplicates - Avoiding errors if you've already got some data in your table
            insert_end = """ on duplicate key update
                close=close;"""

            # Put the parts together
            query = insert_init + vals + insert_end

            # Fire insert statement
            cursor.execute(query)
    print ('The database was updated')

# update_db()