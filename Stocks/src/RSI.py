'''
Created on Jan 30, 2019

@author: Chris Lynch

This class calculates the RSI of a stock.

Step 1: 
    Find the trade setup."
        Can be indicated by the swing highs and lows
        Being above the 200 day moving average
        
Momentum
    Momentum = V - Vx
      Where V = Latest price
      Vx = Closing price
      x = Number of days ago (usually 10)
      
RSI
    a Momentum indicator
    Incicator oscilates from 0 -100
        30 oversold
        70 overbought
    
    RSI = 100 - [100/(1 + (Average of Upward Price Change/ Average of downward price change)]
     During bearish conditions, the RSI peaks at 50 rather than 70, indicating bearing conditions
    RSI Swing Rejections
        Bearish Swings
        
'''

 
from statistics import mean
from datetime import timedelta 


class RSIClass:
    #I'm thinking time delta should be a number of days to look back from (Usually 14)
    def calculateGainsLosses(self, data, today):
        #When getting yesterday's date, we can't simply get the day before, because that might be a weekend.
        #  To workaroudn, I will get a range of the last 3 days and get the second to last element of the array
        #  THis will return the previous day
        previousDate  = today - timedelta(days=3)
        dataSet = data.loc[str(previousDate.date()) : str(today.date())]
        #try catch needed for first day
        try:
            yesterdaysPrice = dataSet.iloc[-2]['close']
        except:
            return 0
        
        todaysPrice = data.loc[str(today.date())]['close']
        return todaysPrice - yesterdaysPrice
        
    
    #TimeSpan should usually be 14
    def calculateRSI(self, data, today, gain, loss, timeSpan):        
        gainData = gain[-timeSpan:]
        lossData = loss[-timeSpan:]
        
        averageGain = mean(gainData)
        averageLoss = mean(lossData)
        if(averageLoss == 0):
            return 0 
        rsi = 100- (100/(1 + (averageGain / averageLoss)))
       
        return rsi
    def __init__(self):   
        pass
        
        
        
        
        