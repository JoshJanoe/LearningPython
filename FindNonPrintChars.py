#!python
from ast import List
import re
import pandas
from tkinter import *

###
# Non-Printing Character and Column Count Check Setup
###

# Checks to see if the user expected number of columns matches the actual number
def colCheck(df, expectedCols, standAlone=0):
	numColumns = len(df.columns)
	result = "\tColumns expected: " + str(expectedCols) + "\n\tColumns found: " + str(numColumns)	
	if expectedCols > 0:
		result += "\nColumn check complete"
		if expectedCols != numColumns: 
			result += "\nWARNING: Column count does not match"
		# 4. Otherwise returns nothing- indicating a good count.
		if standAlone == 0:
			result += "\n"+"-"*50
	return result	

# Determines name of column containing the bad character
def getColName(row, charCounter, df):
	commaCount = 0
	for c in row[:charCounter]:
		if c == ",":
			commaCount += 1
	colHeadings = list(df.columns)
	return colHeadings[commaCount]

# Converts bad character into a printable form
def pChar(char):
	return char.encode("ascii", "backslashreplace").decode()

# Determines how to update the counter if a bad character is found
def charCounterUpdate(counter):
	if counter == 0:
		return -1
	else:
		return -2	

def errorCheck(path, expectedCols=0):
	errorMessageString = ""
	colCheckString = ""
	totalErrors = 0
	# the range "\x20-\x7E" or " -~" covers printable part of ascii table
	regEx = ('[^ -~\\n\\r]')
	df = pandas.read_csv(path)
	if expectedCols > 0:
		#errorMessageString += colCheck(df,expectedCols)
		colCheckString += colCheck(df,expectedCols)

	# Check CSV for matches to RegEx
	with open(path) as csvIn:
		rowCounter = 0
		for row in csvIn:
			# Return an error with the line number of each match.
			badChar = None
			badCharFound = True
			charCounter = 0
			for char in row:
				regExCheck = re.search(regEx, str(char), re.A)
				if char == badChar:
					badCharFound = True				
				if badCharFound and regExCheck != None:
					colName = getColName(row,charCounter,df)
					errorMessageString  += ("\n\tUnprintable Character ("+ pChar(char)
									+ ") found on Row " + str(rowCounter+1)
									+ ", in Column \"" + str(colName) + "\"")
					badCharFound = False
					badChar = char
					totalErrors += 1
					charCounter += charCounterUpdate(charCounter)
				charCounter += 1
			rowCounter += 1
		# If no errors found return nothing but simple print statement
		if errorMessageString == "":
			errorMessageString += "No errors found!"
		errorMessageString += "\nTotal errors found in file: " + str(totalErrors)
		return colCheckString + errorMessageString

###
# GUI Setup
###

#gui code
root = Tk()	
root.title("Non Printable Character Check and Column Count Verify")	

# Variables
stdPad = 5
stdwidth = 30
filePath = StringVar()
filePath.set("")
badCharBoolCB = IntVar()
colCheckBoolCB = IntVar()
numCols = IntVar()
results = StringVar()

def clrScreen():
	readoutListBox.delete(0,END)

def locked(currState):
	if currState == 0:
		colEntry.config(state=DISABLED)
	if currState == 1:
		colEntry.config(state=NORMAL)

def updateText():
	errorList = results.get().split("\n")
	for line in errorList:
		readoutListBox.insert(END, line)
	readoutListBox.insert(END, "-"*50)

def runChecks():
	if filePath.get().__contains__("\""):
		readoutListBox.insert(END, "\nInvalid file path")
	else:
		readoutListBox.insert(END, "\n\nChecking file...")
		if badCharBoolCB.get() == 1 and colCheckBoolCB.get() == 1:
			results.set(errorCheck(filePath.get(), numCols.get()))
			updateText()
		if badCharBoolCB.get() == 1 and colCheckBoolCB.get() == 0:
			results.set(errorCheck(filePath.get()))
			updateText()
		if badCharBoolCB.get() == 0 and colCheckBoolCB.get() == 1:
			df = pandas.read_csv(filePath.get())
			results.set(colCheck(df,numCols.get(),1))
			updateText()
		if badCharBoolCB.get() == 0 and colCheckBoolCB.get() == 0:
			results.set("No options selected")
			updateText()

# Setup frames and objects
topFrame = LabelFrame(root, text="User input")
bottomFrame = LabelFrame(root, text="Tests Output/Results")
exitButton = Button(root, text="Exit Program", width=stdwidth, command=root.quit)
clearScreenButton = Button(root, text="Clear", width=stdwidth, command=clrScreen)

fileEntry = Entry(topFrame, bg="white", width=stdwidth*2, textvariable=filePath)
description = Label(topFrame, text="Enter file path")
badCharCB = Checkbutton(topFrame, text="Check for Non-Printable Characters", 
						width=stdwidth, variable = badCharBoolCB, anchor=W,
						onvalue=1, offvalue=0)
colCheckCB = Checkbutton(topFrame, text="Verify Number of Columns", 
						width=stdwidth, variable = colCheckBoolCB, 
						command=lambda: locked(colCheckBoolCB.get()), anchor=W,
						onvalue=1, offvalue=0)
expectedCols = Label(topFrame, text="Expected Number of Columns")
colEntry = Entry(topFrame, textvariable=numCols, state=DISABLED)
submitButton = Button(topFrame, width=stdwidth, text="Run Test", command=runChecks)

vScrollBar = Scrollbar(bottomFrame, orient=VERTICAL)
readoutListBox = Listbox(bottomFrame, yscrollcommand=vScrollBar.set, width=100, 
						bg="grey", fg="white")

vScrollBar.config(command=readoutListBox.yview)
readoutListBox.insert(END, "Click \"Run Test\" to begin")

badCharCB.select()
colCheckCB.deselect()

# Push objects onto window
topFrame.pack(padx=stdPad*2, pady=stdPad, ipady=stdPad, fill=X)
bottomFrame.pack(padx=stdPad*2, pady=stdPad/2, ipady=stdPad, fill=X)
clearScreenButton.pack(padx=stdPad*2, pady=stdPad*2, side=LEFT)
exitButton.pack(padx=stdPad*2, pady=stdPad*2, side=RIGHT)

fileEntry.grid(row=0, column=1, pady=stdPad, columnspan=2, padx=stdPad*3)
description.grid(row=0, column=0)
badCharCB.grid(row=1, column=0, pady=stdPad)
colCheckCB.grid(row=2, column=0, pady=stdPad)
expectedCols.grid(row=2, column=1, pady=stdPad, padx=stdPad*3)
colEntry.grid(row=2, column=2, pady=stdPad)
submitButton.grid(row=3, column=0, pady=stdPad, columnspan=3)

readoutListBox.grid(row=0, column=0, ipadx=stdPad, ipady=stdPad)
vScrollBar.grid(row=0,column=1, sticky=NS)

#main execution
root.mainloop()
