'''
Created on Sep 19, 2019

@author: Chris Lynch

This class pulls the stock history data from IEXFinance
'''
#cjlynch278 token: 
#API Token: pk_6a90b473fae24ec4ac70e5b5f3ec14a8 
#sk_4851ebe7c1994d1180c85cd7404038ea
#sk_b4a9b4c419a9435db9252a77200f68cf
#pk_5f00f23d191844df9a0ab596c28d7b0e 
from iexfinance import *
from iexfinance.stocks import get_historical_data
from datetime import datetime

class StockData:
    def __init__(self):
        #I have many keys for IEX finance that have a API limit.
        self.keys = ["pk_6a90b473fae24ec4ac70e5b5f3ec14a8","sk_4851ebe7c1994d1180c85cd7404038ea","sk_b4a9b4c419a9435db9252a77200f68cf", 
             "pk_5f00f23d191844df9a0ab596c28d7b0e"]
        self.token = 'sk_4851ebe7c1994d1180c85cd7404038ea'
        pass
    
    def findStockData(self, stockName):
        startDate = datetime.strptime( '2015-01-01', "%Y-%m-%d")
        endDate = datetime.strptime( '2020-01-01', "%Y-%m-%d")
        #To avoid hitting the api limit, the keys are cycled through until it finds one that has api calls available.
        for key in self.keys:
            try:
                self.token = key
                data = get_historical_data(str(stockName), str(startDate.date()), str(endDate.date()), token = self.token, output_format = 'pandas')
                print("success")
                break
            except Exception as e:
                print("Message Limit Hit: " + str(e))
                
        data.to_csv("C:\\Users\\310290474\\eclipse-workspace\\Stocks\\src\\Stock Histories\\" + str(stockName) + '.csv')
        



