#!python
import pandas
import argparse
import sys
import re

### Code revised by KS to decrease processing time from 2n^2 to n^2 by eliminating extra loop over each column before looping over characters

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
	with open(path) as csvIn:
		rowCounter = 0
		for row in csvIn:
			# 3. return an error with the line number of each match.
			badChar = None
			badCharFound = True		
			charCounter = 0
			for char in row:
				#the range "\x20-\x7E" or " -~" covers printable part of ascii table	
				regEx = ('[^ -~\\n\\r]')
				regExCheck = re.search(regEx, str(char), re.A)
				if char == badChar:
					badCharFound = True		
				if badCharFound and regExCheck != None:
					errorMessage = "ERROR found on LINE " + str(rowCounter) + ", at INDEX " + str(charCounter) + " - character: " + char.encode("ascii", "backslashreplace").decode()
					errorMessageArray.append(errorMessage)
					badCharFound = False
					badChar = char
					totalErrors += 1
					if charCounter == 0:
						charCounter -= 1
					else:
						charCounter -= 2	
				charCounter += 1
			rowCounter += 1		
		# 4. otherwise return nothing- indicating no errors were found.
		errorMessageArray.append("Total errors found in file: " + str(totalErrors))
	print(*errorMessageArray, sep="\n")

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
