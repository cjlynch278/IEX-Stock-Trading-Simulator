
'''
Created on Feb 4, 2020

@author: Chris Lynch

This class calculates all of the essential data to a csv.
This data will be used to determine wheter a stock is bought or sold.
This class also plots the data.
'''

import matplotlib.patches as mpatches
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
import matplotlib.pyplot as plt
import pandas as pd
register_matplotlib_converters()

from RSI import RSIClass
from BasicCalculations import Calculations
from StockData import StockData


class DataManipulate:
    def __init__(self, buyRange, sellRange, timeNow, stockName):
        self.stockName = stockName
        self.basicCalcs = Calculations(timeNow, stockName)
        self.buyRange = buyRange
        self.sellRange = sellRange

 
    def plotData(self, data, columnNames, stockName):
        nameList = ["Price", "Fifty Day Average", "Two Hundered Day Average", "Positive Range", "Negative Range"]
        dates = data.index
        locator = mdates.YearLocator()  # every month
        #Specify the format - %b gives us Jan, Feb...
        fmt = mdates.DateFormatter('%Y')
        fig = plt.gcf()
        fig.canvas.set_window_title(str(stockName))
        i = 0
        for name in columnNames:
            
            plt.plot(dates, data[name], label=nameList[i])

            i = i+ 1
        
        
        #Here I need to add a key for the "Buy Point" and "Sell Point". 
        #I get the existing labels and assign the returned tuple object. 
        #Handles is needed, labels is uesless, but necessary to assign the tuple object.
        #I manually create the buy and sell patch and add it to the existing legend
        handles, labels= plt.gca().get_legend_handles_labels()
        buyPatch = mpatches.Patch(color='red', label='Buy Point')
        sellPatch = mpatches.Patch(color='blue', label='Sell Point')
        handles.append(buyPatch)
        handles.append(sellPatch)
        plt.legend(handles = handles, loc='upper left')
        
        
        #Plot elements
        plt.title(str(stockName))
        plt.xlabel("Date")
        plt.ylabel("Price of Stock")
        X = plt.gca().xaxis
        X.set_major_locator(locator)
        X.set_major_formatter(fmt)
        return plt
    
    def addDatatoFrame(self, data, shortAverage, longAverage):
        i = 0
        fiftyAverages = []
        fiftyDayDerivative = []
        twoHundredAverages = []
        derivatives = []
        negRange = []
        posRange = []
        gain = []
        loss = []
        rsiData = []
        date = data.index
        
        rsi = RSIClass()
        
        #Calculates all data
        while i < int(len(data.index)):
            twoHundredAvg = self.basicCalcs.getXDayAverage(data, longAverage, date[i])
            derivative = self.basicCalcs.getDerivative(data, shortAverage, date[i], 'close')
            derivatives.append(derivative)
            fiftyAverages.append(self.basicCalcs.getXDayAverage(data, shortAverage, date[i]))
            fiftyDayDerivative.append(self.basicCalcs.get10DayDerivative(fiftyAverages))

            twoHundredAverages.append(self.basicCalcs.getXDayAverage(data, longAverage, date[i]))
            posRange.append(twoHundredAvg + (twoHundredAvg * self.sellRange))
            negRange.append(twoHundredAvg - (twoHundredAvg * self.sellRange))
            gainLoss = rsi.calculateGainsLosses(data, date[i])
            
            if(gainLoss < 0 ):
                loss.append(abs(gainLoss))
                gain.append(0)
            else:
                gain.append(gainLoss)
                loss.append(0)
            
            rsiData.append(rsi.calculateRSI(data, date[i], gain, loss, 14))
            i = i + 1
        
        newData = data.assign(FiftyDayAverage=fiftyAverages)
        newData = newData.assign(FiftyDayDerivative = fiftyDayDerivative)
        newData = newData.assign(TwoHundredDayAverage=twoHundredAverages)
        newData = newData.assign(Derivative = derivatives)
        newData = newData.assign(PositiveRange=posRange)
        newData = newData.assign(NegativeRange=negRange)
        newData = newData.assign(Gain = gain)
        newData = newData.assign(Loss = loss)
        newData = newData.assign(RSI = rsiData)
        return newData

    def readcsv(self, csvFileName):
        stockData = StockData()
        try: 
            data = pd.read_csv("Stock Histories/" + str(csvFileName) + ".csv", index_col='date', parse_dates=['date'])     
        except OSError as e:
            stockData.findStockData(str(csvFileName))
            data = pd.read_csv("Stock Histories/" + str(csvFileName) + ".csv", index_col='date', parse_dates=['date'])     

            
        
        return data

    