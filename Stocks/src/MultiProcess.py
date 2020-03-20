'''
Created on Mar 9, 2020

@author: Chris Lynch

The multiprocessing is handled in this class.
'''
from Stocks import  ComputeProfit
import os
from datetime import datetime
import json

from multiprocessing import Pool

class MultiProcess:
    def __init__(self, stockNamesList):
        self.stockNamesList = stockNamesList
        self.instances = []
        self.now = str(datetime.now().strftime("%Y%m%d %H%M%S"))
        self.results = []
        self. profits = []
        self.plots = []
        try:
            os.makedirs(str(os.path.abspath(os.curdir)) + '\\Archive\\' + self.now)
        except Exception as e:
            print(str(e))

    
    def helper(self,stock):
        instance = self.runOne(stock)
        
        self.results.append(instance)
        self.results.append(instance.profit)
        self.plots.append(instance.plot)
        return str("Profit for " + str(instance.stockName) + " is " + str(instance.profit))
    

    def execute(self):
        #This pool creates all of the needed processes with the stockName List variable.
        pool = Pool(processes = len(self.stockNamesList))        
        self.results = pool.map(self.helper, self.stockNamesList)
        print('done')
    
    
    def runOne(self,stockName):                  
        data = {}
        data["Original Stocks"] = []
        instance = ComputeProfit(.07,.07, str(stockName), 50, 250, False, self.now)
        self.plot = instance.run()
        
        print("Profit for " + str(stockName) + " is " + str(instance.profit))
        self.profit = instance.profit

        instance.plot.show()
        
        return instance
    
    
