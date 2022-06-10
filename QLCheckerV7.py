import csv
from importlib.resources import path
import pandas
import argparse
from pathlib import Path
import sys

def main():
	args = commandLineInput()
	if args.option == "badchars":
		errorCheck(args.path)
		sys.exit()
	elif args.option == "colcheck":
		colCount(args.path)
		sys.exit()
	else:
		print("ERROR: INVALID OPTION ENTRY")

#function to find any non-ascii characters
def errorCheck(path):
	# 1. take a csv file name with path as input.
	errorMessageArray = ["Searching file for errors.."]
	totalErrors = 0
	# 2. open the csv file and check for regex matches to [^\x00-\xff]
	with open(path) as csv_file:
		csvReader= csv.reader(csv_file, delimiter=",")
		rowCounter = 0
		for row in csvReader:
			colCounter = 0
			for col in row:
				# 3. return an error with the line number of each match.
				if isNotValid(col):
					badChar = None
					badCharFound = True		
					charCounter = 0
					for char in col:
						if char == badChar:
							badCharFound = True		
						if isNotValid(char) and badCharFound:
							errorMessage = "ERROR found on LINE " + str(rowCounter) + " in COLUMN " + str(colCounter)+ ", at character INDEX " + str(charCounter) + " - character: " + char.encode("ascii", "backslashreplace").decode()
							errorMessageArray.append(errorMessage)
							badCharFound = False
							badChar = char
							totalErrors += 1
							if charCounter == 0:
								charCounter -= 1
							else:
								charCounter -= 2	
						charCounter += 1
				colCounter += 1	
			rowCounter += 1			
		# 4. otherwise return nothing- indicating no errors were found.
		errorMessageArray.append("Total errors found in file: " + str(totalErrors))
	print(*errorMessageArray, sep="\n")

def isNotValid(text):
	decodedText = text.encode("ascii", "ignore").decode()
	if text != decodedText:
		return True
	else:
		return False


#function to determine the number of columns in a given CSV file
def colCount (path):
	# 1. Takes a csv filename and path and an integer as input.
	integer = input("How many columns are expected? ")
	# 2. Opens the file and counts the columns in the data.
	df = pandas.read_csv(path)
	numColumns = len(df.columns)
	# 3. Errors out if the count doesn't match the integer input from the command line.
	if (int(integer) != numColumns):
		print("ERROR: Column count does not match\n\tColumns expected: "
			+str(integer)+"\n\tColumns found: "+str(numColumns))
	# 4. Otherwise returns nothing- indicating a good count.
	else:
		print("Number of columns matches input number")
	print("Column count check complete")

def commandLineInput ():
	# Initialize parser
	parser = argparse.ArgumentParser(
        description="Locates bad characters or verifies the number of columns in provided CSV file")
		# Adding optional argument
	parser.add_argument(dest="option", 
                        nargs='?',
                        type=str,
                        help="<Required> script option.  choose \"badchars\" to check for bad characters, or \"colcheck\" to verify columns")
	# Adding optional argument
	parser.add_argument(dest="path", 
                        nargs='?',
                        type=str,
                        help="<Required> file's full path")
	# Adding optional argument
	parser.add_argument(dest="cols", 
                        nargs='?',
                        type=int,
                        help="<Required> file's full path")	
	args = parser.parse_args()
	return args

if __name__=="__main__":
    main()