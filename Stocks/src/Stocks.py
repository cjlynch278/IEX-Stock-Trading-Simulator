'''
Created on Sep 23, 2019

@author: Chris Lynch

This class uses all of the calculations to decide wheteher a stock will be bought or sold
'''



from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

from RSI import RSIClass
from BasicCalculations import Calculations
from DataManipulation import DataManipulate
from datetime import datetime
import os


class ComputeProfit:
    #CSV File name does not include the .csv file extension!!!
    #Thia is so that I can reuse the variable to name the graph
    #RSIBool determines if I should use RSI or not
    def __init__(self, bRange, sRange, stockName, shortAverage, longAverage, rsiBool,timeNow):
           
        # I need a variable that determines within what range to sell/buy a stockName. So if the average is 100$ and this variable is set to .1 (10%)
        # , then the algorithm will
        # buy the stockName when it's between 90 and 110. 
        
        self.timeNow = timeNow
        self.rsiBool = rsiBool
        self.sellRange = sRange
        self.buyRange = bRange
        self.basicCalcs = Calculations(timeNow, stockName)
        self.dataManipulations = DataManipulate(bRange, sRange, timeNow,stockName)
        self.plot = None 
        self.recordFile = open(str(os.path.abspath(os.curdir)) + '\\Archive\\'  + timeNow + '\\' + stockName + ' StocksRecord.csv', 'w')
        self.recordFile.write("Date,Stock Name,Action,Price\n")
        self.stockName = stockName
        self.profit = 0
        self.shortAverage = shortAverage
        self.longAverage = longAverage
        
    def  tradeCheck(self, dataFrame, dateToCheck):
        
        fiftyDayAvg = dataFrame.loc[dateToCheck.date()]['FiftyDayAverage']
        twoHundredAvg = dataFrame.loc[dateToCheck.date()]['TwoHundredDayAverage']
        derivative = dataFrame.loc[dateToCheck.date()]['Derivative']
        fiftyDayDerivative = dataFrame.loc[dateToCheck.date()]['FiftyDayDerivative']
        negativeRange = dataFrame.loc[dateToCheck.date()]['NegativeRange']
        
        #RSI        
        if(dataFrame.loc[str(dateToCheck.date())]['RSI'] < 30):
            return("Buy")
        if(dataFrame.loc[str(dateToCheck.date())]['RSI']  > 30):
            return ("Sell")
       
    
        regular = """
        if(
            (fiftyDayAvg >= negativeRange) &
            (fiftyDayAvg <= negativeRange + negativeRange*.025) &
            (fiftyDayDerivative > 0)
            ): 
            return ("Buy")
        if(
            (fiftyDayDerivative < -0.35) & 
           # (fiftyDayAvg > twoHundredAvg ) & 
            (derivative < 0)
             
            ):
            return ("Sell")   
        """ 
        trendyWay = """
        
        if(
            (fiftyDayAvg >= twoHundredAvg) &
            (fiftyDayAvg <= twoHundredAvg + twoHundredAvg*.025) &
            (fiftyDayDerivative > 0)& 
            (fiftyDayAvg < (twoHundredAvg + (twoHundredAvg * self.buyRange))) 
            ): 
            return ("Buy")
        if(
            (fiftyDayDerivative < -0.35) & 
           # (fiftyDayAvg > twoHundredAvg ) & 
            (derivative < 0)
             
            ):
            return ("Sell")   
            
        
        if(self.rsiBool):
            if(dataFrame.loc[str(dateToCheck.date())]['RSI'] < 30):
                return("Buy")
            if(dataFrame.loc[str(dateToCheck.date())]['RSI']  > 30):
                return ("Sell")
       
        
        
        if(
            (fiftyDayAvg > twoHundredAvg) & 
            (fiftyDayAvg < (twoHundredAvg + (twoHundredAvg * self.buyRange))) & 
            (derivative > 0)            
            ): 
            return ("Buy")
        if(
            (fiftyDayAvg > (twoHundredAvg - (twoHundredAvg * self.sellRange))) & 
            (fiftyDayAvg < twoHundredAvg ) & 
            (derivative < 0) 
            ):
            return ("Sell")   
        """
       
    def checkstockNames(self, dataFrame, plot,stockName):
        bought = False 
        #We're going to start i at 200 to let the 200 average be accurately calculated.
        i = 200
        date = dataFrame.index
        while i < int(len(dataFrame.index)):
            prevPrice = self.basicCalcs.getPrevPrice(dataFrame, date[i])
            if(self.tradeCheck(dataFrame, date[i]) == "Buy" and not bought):
                self.recordFile.write(str(date[i].date()) + "," + str(stockName) + ",Bought,-" + str(prevPrice) + "\n")
                plot.plot(date[i].date(), prevPrice, marker='o', markersize=12, color="red")
                
                bought = True
            if(self.tradeCheck(dataFrame, date[i]) == "Sell" and bought):
                self.recordFile.write(str(date[i].date()) + "," + str(stockName) + ",Sold," + str(prevPrice) + "\n")
                plot.plot(date[i].date(), prevPrice, marker='o', markersize=12, color="blue")
                bought = False
            i = i + 1

    def testCheck(self, data, plot, stockName):
        self.checkstockNames(data, plot,stockName)
        self.recordFile.close()        
        # print(self.getProfit())
    
    

    def run(self):
        
        data = self.dataManipulations.readcsv(str(self.stockName))
        data = self.dataManipulations.addDatatoFrame(data, self.shortAverage, self.longAverage)
        plot = self.dataManipulations.plotData(data, ['close', 'FiftyDayAverage', 'TwoHundredDayAverage', 'PositiveRange', 'NegativeRange' ]
                                        ,str(self.stockName))
        
        data.to_csv("Archive\\" + self.timeNow + '\\' + self.stockName + ' Calculated Output.csv' )
        self.testCheck(data, plot, str(self.stockName))
        self.recordFile.close()
        profit = self.basicCalcs.getProfit()
        self.profit = profit
        self.plot = plot
        return self
        return plot   
   





