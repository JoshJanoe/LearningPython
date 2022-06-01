import pandas

# Part 1 - Opem File
path = '???/????/????/cows.csv'
cows = pandas.read_csv(path)
print(cows) # prints entire data set
print("\n")
# print(cows.head(3)) # prints first 3 entries
# print(cows.tail(3)) # prints last 3 entries

# Part 2 - Remove a Column
cows = cows.drop('entry', 1) # 0 for rows, 1 for columns
print(cows)
print("\n")

# Part 2b - Add a Column
cows['active'] = cows.status == "active"
print(cows)
print("\n")

# Part 3 - Sort by Remaining Column
cows = cows.sort_values(by=['status'])
print(cows)
print("\n")
