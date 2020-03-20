'''
Created on Sep 19, 2019

@author: Chris Lynch

This class handles calculating derivatives, averages, and profits of a given database.
'''

# rom iexfinance import get_historical_data

from datetime import timedelta 
import pandas as pd
import os  
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


class Calculations:
    
    def __init__(self,timeNow, stockName):
        self.stockName = stockName
        self.timeNow = timeNow
                
    def getPrevPrice(self, dataFrame, date):
        # A more accurate way to get the derivative would be to use the current price.
        # However to avoid api overusage I'm going to use the last recorded price in the dataframe.
        tempFrame = dataFrame.loc[str(date.date()) : str(date.date() + timedelta(days=3))]   
        return float(tempFrame.iloc[0]['close'])
    
    def getDerivative(self, dataFrame,  timeDeltaX, dateToCheck, columnName):
        XDaysAgo = dateToCheck - timedelta(days=timeDeltaX)
        priceRange = dataFrame.loc[str(XDaysAgo.date()) : str(dateToCheck.date())]
        oldPrice = priceRange.iloc[0][str(columnName)]
        currentPrice = priceRange.iloc[-1][str(columnName)]
        derivative = (currentPrice - oldPrice) / timeDeltaX
        return float(derivative)
    
    def get10DayDerivative(self, data):
        try:
            return ((data[len(data) - 1] - data[len(data) - 11]) / data[len(data) - 6]) * 100
        
        #Will Trigger when no data yet present
        except Exception as e:
            return 0 
        
    def getXDayAverage(self, dataBase, timeDeltaX, endDate): 
        startDate = endDate - timedelta(days=timeDeltaX)  
        dataBaseRange = dataBase.loc[str(startDate.date()) : str(endDate.date())]
        return dataBaseRange["close"].mean() 

    def getProfit(self):
        data = pd.read_csv(str(os.path.abspath(os.curdir)) + '\\Archive\\'  + self.timeNow + '\\' + self.stockName + ' StocksRecord.csv', index_col='Date')
        profit = data['Price'].sum()
        if(len(data) == 0 ):
            return 0
        if str(data.iloc[-1]['Action']) == 'Bought':
            profit = profit - float(data.iloc[-1]['Price'])
           
        return round(profit, 2)
    
    
    
    
    
    