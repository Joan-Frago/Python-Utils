import sys
import os
from datetime import datetime

# Import the module
sys.path.append(os.path.dirname(os.path.dirname("utils.py")))
from utils import Utils

# general variables
iFile = "tests/testFile.txt"
iContents = "hola\nhola\nhola  hola"
iUrl = "https://api.github.com/users/python"
body = {
    "name" : "Joan Frago",
    "age" : 18
}
headers = {
    "Authorization" : "The token goes here",
    "Accept" : "application/json"
}

# Read file and Write to file
"""
utils = Utils(iFile, iContents)


contents = utils.writeFile()

fileContents = utils.readFile()
print(fileContents)
"""

# Json Handling
"""
utils = Utils(aUrl=iUrl)
data = utils.getJsonData()
print(data)
"""

# CSV Handling
"""
iFile="tests/testCSV.csv"
delimiter=","
utils = Utils(iFile,adelimiter=delimiter)
dictCSV = utils.readCSV()
print(dictCSV)
"""

"""
# Converting date to timestamp.
dtTime = datetime.now()
utils = Utils(dateTime=dtTime)
timestamp = utils.Date2Timestamp()
print(timestamp)
"""
""" 
# Converting timestamp to date
utils = Utils(timestamp=timestamp)
date = utils.Timestamp2Date()
print(date)
 """
""" 
timestamp = 1710522818

# Calculate time Diff
utils = Utils(timeStamp=timestamp)
diff = utils.TimestampTimeDiff()
print(f"Difference in timestamp {diff}")

date = datetime.now()
utils = Utils(dateTime=date)
diff = utils.DateTimeDiff()
print(f"Difference in human date {diff}")
 """

