'''
Created on Mar 4, 2020

@author: Chris Lynch

This class creates the user interface.
'''

from tkinter import *
from os import listdir
from MultiProcess import MultiProcess

import os


class GUI:
    def __init__(self):
        self.stockList = []
        self.soqlQueryList = []          
        self.root = Tk()
        self.root.title('Stock')
        self.root.resizable(width=FALSE, height=FALSE)
        self.root.geometry('{}x{}'.format(540, 810))
        self.addElements()
        self.root.mainloop()
        
    def addElements(self):
        #Adds all of the buttons in the gui
        self.savedStocksList = Listbox(self.root, selectmode=MULTIPLE, width=53, height=10)
        self.savedStocks = []
        for file in (listdir(os.path.abspath(os.curdir + '\\Stock Histories\\'))):
            self.savedStocks.append(file.split(".csv")[0])
        for item in self.savedStocks:
            self.savedStocksList.insert(END, item)
            
        self.savedStocksTitle = Label(self.root, text="Available Stocks", font=("Courier", 12)) 
        self.savedStocksTitle.place  (x = 100, y = 15) 
        self.savedStocksList.place(x= 100, y = 40)
        
        self.queriesTitle = Label(self.root, text="Selected Stocks", font=("Courier", 12)) 
        self.queriesTitle.place  (x = 100, y = 240) 
        
        self.selectedText = Text(self.root, width = 40, height = 10)
        self.selectedText.place(x = 100, y = 265)
        
        self.addAllButton =  Button(text = "Add All", command = lambda: self.addAllStocksMethod(self.selectedText))
        self.addAllButton.place(x = 180, y = 210)
       
        self.clearButton = Button(text = "Clear", command = lambda: self.clearText(self.selectedText,self.stockList))
        self.clearButton.place(x = 100, y = 435)
        
        
        self.executeButton = Button(text = "Execute", command = lambda: (self.executeQuery(resultText)))
        self.executeButton.place(x = 150, y = 435)
        
        
        self.stocksAddButton = Button(text = "Add Stocks", command = lambda: self.addsavedStocks(self.savedStocksList,self.savedStocks,self.selectedText)) 
        self.stocksAddButton.place(x = 100, y = 210)

        
        resultsTitle = Label(self.root, text="Results", font=("Courier", 12)) 
        resultsTitle.place  (x = 25, y = 465) 
        
        resultText = Text(self.root, width = 60, height = 17)
        resultText.place(x = 25, y = 490)
        
    def enterText(self, textArea,text):
        textArea.insert('1.0', str(text) + "\n")
    
    def clearText(self, textArea, stockList):
        textArea.delete('1.0', END)
        stockList.clear()
    
    def executeQuery(self, resultPane):
        stocks = self.selectedText.get("1.0", END).splitlines()

        #Removes blank stock if any
        if(stocks[-1] == " " or stocks[-1] == "\n" or stocks[-1] == ""):
            stocks.pop()
        #Calls the multiprocessing process to compute stocks.
        multiProcess = MultiProcess(stocks) 
        multiProcess.execute()
        print("Results: " + str(multiProcess.results))
        
        resultPaneText = ""
        for result in multiProcess.results:
            resultPaneText = resultPaneText + str(result) + "\n"
        
        #Prints results to result pane
        resultPane.insert("1.0", resultPaneText)
        

        
            
       
    
    def addAllStocksMethod(self, textArea):
    #Button to compute all stocks if needed.
        for item in self.savedStocks:
            textArea.insert(END, str(item) + "\n")
    def addsavedStocks(self, button, itemList, textArea):
        for item in button.curselection():
            textArea.insert(END, str(itemList[item]) + "\n")
            

               
    


