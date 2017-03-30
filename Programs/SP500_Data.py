import bs4 as bs
import datetime as dt
import numpy as np
import os
import pandas as pd
import pandas_datareader.data as web
import pickle
import requests

def save_sp500_tickers():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    """
    The Wikipedia page gives the response, which contains source code. 
    Access the .text attribute of the response and turn to soup using BeautifulSoup. 
    BeautifulSoup turns source code into a BeautifulSoup object that can be treated like a typical Python object.
    print(soup)
    """
    table = soup.find('table', {'class': 'wikitable sortable'})
    """
    This is just one very specific solution.
    Find the table of stock data by simply searching for the wikitable sortable classes. 
    View the sourcecode in a browser first, then specify the table.
    To parse a different website's list of stocks, it may be in a table, or a list, or maybe something with div tags. 
    print(table)
    """
    
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)
        
    with open("sp500tickers.pickle","wb") as f:
        pickle.dump(tickers,f)
        
    return tickers

#save_sp500_tickers()

def get_data_from_yahoo(reload_sp500=False):
    
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle","rb") as f:
            tickers = pickle.load(f)
    
    if not os.path.exists('data/stock_dfs'):
        os.makedirs('data/stock_dfs')

    end = dt.date.today()
    years=5
    time_period=dt.timedelta(weeks=years*52)
    start=end-time_period

    
    for ticker in tickers:
        #print(ticker)
        # just in case your connection breaks, we'd like to save our progress!
        if not os.path.exists('data/stock_dfs/{}.csv'.format(ticker)):
            if ticker not in ['BRK.B','BF.B']:
                df = web.DataReader(ticker, "yahoo", start, end)
                df.to_csv('data/stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))

#get_data_from_yahoo()

def compile_data():
    with open("sp500tickers.pickle","rb") as f:
        tickers = pickle.load(f)

    main_df = pd.DataFrame()
    
    for count,ticker in enumerate(tickers):
        if ticker not in ['BRK.B','BF.B']:#
            #print(ticker) 
            df = pd.read_csv('data/stock_dfs/{}.csv'.format(ticker))
            df.set_index('Date', inplace=True)

            df.rename(columns={'Adj Close':ticker}, inplace=True)
            df.drop(['Open','High','Low','Close','Volume'],1,inplace=True)

            if main_df.empty:
                main_df = df
            else:
                main_df = main_df.join(df, how='outer')

            if count % 10 == 0:
                print(count)
    print(main_df.head())
    main_df.to_csv('sp500_joined_closes.csv')


#compile_data()