#!python
import os
import argparse
import re
import pandas

# ADD CODE FOR A BETTER VISUAL REPRESENTATION OF BAD CHARACTERS

# Code revised by KS to decreased processing time from 2n^2 to n^2 by eliminating extra loop over each column before looping over characters

# NOTES on ASSERT:
# Errors out if the count doesn't match the integer input from the command line.
# assert is a simple boolean
# using assert() makes it always true
# following statement applies if NOT true

# Run speed found to be comparable over ~1000 line CSV with or without separated out functions
# Command used for speed tests:  "time python <thisScriptFilePath> <testFile> -o colcheck -c 14"


def main():
	args = commandLineInput()
	assert os.path.isfile(args.path)
	if args.option == "badchars":
		errorCheck(args.path)
	elif args.option == "colcheck":
		errorCheck(args.path, args.cols)
	else:
		print("ERROR: INVALID OPTION ENTRY")

# Function to find any non-ascii characters
# Also verifies column count if specified by user
def errorCheck(path, expectedCols=0):
	errorMessageString = ""
	totalErrors = 0
	# the range "\x20-\x7E" or " -~" covers printable part of ascii table
	regEx = ('[^ -~\\n\\r]')
	df = pandas.read_csv(path)
	colCheck(df,expectedCols)

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
		assert errorMessageString != "", "No Errors Found"
		print("Total errors found in file: " + str(totalErrors) + errorMessageString)

# Checks to see if the user expected number of columns matches the actual number
def colCheck(df, expectedCols):
	numColumns = len(df.columns)
	result = "\tColumns expected: " + str(expectedCols) + "\n\tColumns found: " + str(numColumns)	
	if expectedCols != 0:
		print("Column check complete")
		assert expectedCols == numColumns, "Column count does not match\n"+result
		# 4. Otherwise returns nothing- indicating a good count.
		print(result+"\n"+"-"*60)

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

def commandLineInput():
	# Initialize parser
	parser = argparse.ArgumentParser(description="Locates bad characters or verifies the number of columns in provided CSV file")
	# Adding required argument
	parser.add_argument(dest="path",
						nargs='?',
						type=str,
						help="<Required> input file's full path")
	# Adding optional argument
	parser.add_argument('-o', dest="option",
						default="badchars",
						nargs='?',
						type=str,
						help="<Optional> option.  choose \"badchars\" to check for bad characters, or \"colcheck\" to verify columns")
	# Adding optional argument
	parser.add_argument('-c', dest="cols",
						nargs='?',
						type=int,
						help="<Optional> column count")
	parser.add_argument('-v', "--version",
						action="version",
						version="QL Data Checker 0.9.1",
						help="Show program version")
	# Adding optional argument
	args = parser.parse_args()
	return args

if __name__ == "__main__":
	main()
