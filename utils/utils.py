#!/usr/bin/python3

import requests
import csv
from datetime import datetime
import sys
import os
import random
from openpyxl import load_workbook

# Read a File
def readFile(aFile:str) -> str:
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
        aNewLine="\n"
    else:
        aNewLine=""
    try:
        if aFile != "":
            with open(aFile,fileMode) as file:
                file.write(f"{aContent}{aNewLine}")
        else:
            return "Please provide a path for file reading"
    except IOError as e:
        return f"Could not write to {aFile} due to {e}"
# Get Json Data
def getJsonData(aUrl:str,headers=None) -> any:
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
def postJsonData(aUrl:str,body:str) -> any:
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
def csv2Dict(aFile:str,aDelimiter=None) -> dict:
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
def Date2Timestamp(dateTime:str) -> float:
    timestamp = datetime.timestamp(dateTime)
    return timestamp
# Convert Timestamp to Date
def Timestamp2Date(timeStamp:int,timeZone=None):
    date = datetime.fromtimestamp(timeStamp,timeZone)
    return date
# Calculate the difference between two timestamp
def TimestampTimeDiff(timeStamp:int) -> int:
    iTime = datetime.now()
    iTs = datetime.timestamp(iTime)
    timeDiff = iTs - timeStamp
    return timeDiff
# Calculate the difference between two date times
def DateTimeTimeDiff(dateTime:int) -> int:
    iTime = datetime.now()
    timeDiff = iTime - dateTime
    return timeDiff
# Check if a number is prime
def IsPrime(aNum:int) -> bool:
    try:
        if isinstance(aNum,int):
            for i in range(1, aNum):
                if aNum % i == 0 and i != aNum:
                    return True
                else:
                    return False
        else:
            print("Please provide an int to check if number is prime")
    except Exception as e:
        print(f"Error cheking if number is prime: {e}")
# Calculate the factorial of a number
def Factorial(aNum:int) -> int:
    try:
        if aNum < 0:
            raise ValueError("Factorial is not defined for negative numbers.")
        if aNum == 0 or aNum == 1:
            return 1
        result = 1
        for i in range(2, aNum + 1):
            result *= i
        return result
    except Exception as e:
        print(f"Could not calculate the factorial of number {aNum}. Error: {e}")
# Load an excel file
def loadExcel(aFile:str, aSheet:str = "") -> any:
    wb = load_workbook(aFile)
    if aSheet != "":
        ws = wb[aSheet]
    else:
        ws = wb.active()
    return ws
