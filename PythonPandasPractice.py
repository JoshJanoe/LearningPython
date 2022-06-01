### 'import pandas as pd" is often used
#from re import M
import pandas 
from datetime import date

### Part 1 - Opem File
path = '/bcs/lgnt/clientapp/jjjtest/input/cows.csv'
### df is often used as the variable name. short for DataFrame.
### ex: df = pd.read_csv(path)
cows = pandas.read_csv(path)
print(cows) # prints entire data set
print("---Full Data Set---\n")
# print(cows.head(3)) # prints first 3 entries
# print(cows.tail(3)) # prints last 3 entries

# Part 2a - Remove a Column
def dropColumn (df,columnName):
	df = df.drop(columnName, 1) # 0 for rows, 1 for columns
	print(df)
	print("---Colum Dropped/Removed---\n")

dropColumn(cows,'entry')

### Part 2b - Add a Column
# must use bracket notation when creating/naming new column 
def addColumn (df, newColumn, compColumn, result):
	df[newColumn] = compColumn == result
	print(df)
	print("---Column Added---\n")

addColumn(cows,'active', cows.status, "active")

### Part 2c - Add a row
#newCow = 20,Moobaca,20,3,m,???,???,?/?/??,active,not real
def addRow (df, newEntry, newName, newTag, newGen, newGender, 
			newMom, newDad, newBDay,newStatus, newNotes):
	newCows = pandas.DataFrame({'entry': [newEntry],
					'name': [newName],
					'tag': [newTag],
					'generation': [newGen],
					'gender': [newGender],
					'mother': [newMom],
					'father': [newDad],
					'birth/arrival date': [newBDay],
					'status': [newStatus],
					'notes': [newNotes]})
	df = df.append(newCows, sort=True, ignore_index=True)
	df = df.reindex(columns=['entry','name','tag',
				'generation','gender','mother',
				'father','birth/arrival date',
				'status','notes'])
	print(df)
	print("---New Row Added---\n")

addRow(cows, 20, 'Moobaca', 20, 3, 'm', '???','???','?/?/??','active','na')

### Part 3 - Sort by Remaining Column
def sortRows(df, sortBy):
	df = df.sort_values(by=[sortBy])
	print(df)
	print("---Table Sorted---\n")

#sortRows(cows,'status')

### Reading, Writing and Overwriting Files
### Reading in a file
### "a" allows Append, "w" allows overWriting
### will create a new file if specified file does not exist
# file = open(path, "a")
# newCow = "21,Moobaca,20,3,m,???,???,??/??/????,active,not real\n"
# file.write(newCow)
# print("\n---Added new line to file---\n")
