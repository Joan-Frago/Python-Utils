import requests
import csv
from datetime import datetime

# Read a File
def readFile(aFile:str):
    try:
        if aFile != "":
            with open(aFile,"r") as file:
                content=file.read()
            return content
        else:
            return "Please provide a path for file reading"
    except IOError as e:
        return f"Could not read {aFile} contents due to {e}"
# Write a File
def writeFile(aFile:str,aContent:str,fileMode="w",newLine:bool=False):
    if newLine == True:
        newLine="\n"
    try:
        if aFile != "":
            with open(aFile,fileMode) as file:
                file.write(f"{aContent}{newLine}")
        else:
            return "Please provide a path for file reading"
    except IOError as e:
        return f"Could not write to {aFile} due to {e}"
# Get Json Data
def getJsonData(aUrl:str,headers=None):
    try:
        response = requests.get(aUrl,headers)
        if response.status_code == 200:
            data = response.json()
        else:
            return f"Error: {response.status_code}"
        return data
    except Exception as e:
        return f"ERROR: {e}"
# Post Json Data
def postJsonData(aUrl:str,body:str):
    try:
        response = requests.post(aUrl,body)
        if response.status_code == 200:
            data = response.json()
        else:
            return f"Error: {response.status_code}"
        return data
    except Exception as e:
        return f"ERROR: {e}"
# Read a CSV
def readCSV(aFile:str,aDelimiter=None):
    try:
        csvDict = []
        with open(aFile,mode="r") as file:
            csv2dict = csv.DictReader(file,aDelimiter)
            for row in csv2dict:
                csvDict.append(row)
        return csvDict
    except Exception as e:
        return e
# Convert Date to Timestamp
def Date2Timestamp(dateTime:str):
    timestamp = datetime.timestamp(dateTime)
    return timestamp
# Convert Timestamp to Date
def Timestamp2Date(timeStamp:int,timeZone=None):
    date = datetime.fromtimestamp(timeStamp,timeZone)
    return date
# Calculate the difference between two timestamp
def TimestampTimeDiff(timeStamp:int):
    iTime = datetime.now()
    iTs = datetime.timestamp(iTime)
    timeDiff = iTs - timeStamp
    return timeDiff
# Calculate the difference between two date times
def DateTimeDiff(dateTime):
    iTime = datetime.now()
    timeDiff = iTime - dateTime
    return timeDiff