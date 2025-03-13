import requests
import csv
from datetime import datetime,timedelta
import sys
import os
import random
from openpyxl import load_workbook
from time import sleep,time
import mysql.connector

class Logger:
    def __init__(self, log_path:str="log/pylog.log"):
        self.log_file = log_path
    
    @staticmethod
    def on_register_func_call(func):
        def wrapper(self,*args,**kwargs):
            self.log_file_rotation()
            return func(self,*args,**kwargs)
        return wrapper
    
    @staticmethod
    def calc_log_file_rotation(aFile):
        pass
    
    def log_file_rotation(self):
        date = GetTime()
        creation_time = datetime.fromtimestamp(os.path.getctime(self.log_file))
        time_diff = date - creation_time

        if time_diff > timedelta(days=7):
            # create new archived log files
            self.calc_log_file_rotation(aFile=self.log_file)

    def write_log(self, type_log:str = "ERROR", aLog:str = ""):
        if not os.path.exists(self.log_file):
            try:
                os.mkdir(self.log_file)
            except Exception as e:
                print(f"Error creating log file: {e}")
                sys.exit()

        text = f"{datetime.now()} {type_log} {aLog}"
        writeFile(aFile=self.log_file,aContent=text,fileMode="a",newLine=True)

    def error(self,log:str):
        self.write_log(type_log="ERROR   ",aLog=log)
    def warning(self,log:str):
        self.write_log(type_log="WARNING ",aLog=log)
    def info(self,log:str):
        self.write_log(type_log="INFO    ",aLog=log)
    
    def exception_handler(self,exc_type,exc_value,exc_traceback):
        err="Unhandled Exception : "
        err+=str(exc_type)+" : "
        err+=str(exc_value)+" : "
        err+=str(exc_traceback)
        self.error(err)

class Timer:
    def __init__(self):
        self.start_time = time()
        self.finish_time = None
    def stop(self):
        self.finish_time=time() - self.start_time

        if self.finish_time < 60:
            final_time = str(round(self.finish_time,3)) + " seconds"
        elif self.finish_time >= 60 and self.finish_time < 3600:
            final_time = self.finish_time / 60
            final_time = str(round(final_time,3)) + " minutes"
        elif self.finish_time >= 3600 and self.finish_time < 86400:
            final_time = self.finish_time / 3600
            final_time = str(round(final_time,3)) + " hours"
        elif self.finish_time >= 86400:
            final_time = self.finish_time / 86400
            final_time = str(round(final_time,3)) + " days"
        return final_time

class DataBase:
    def __init__(self,Host:str,User:str,Password:str,DataBase:str):
        self.aHost = Host
        self.aUser = User
        self.aPassword = Password
        self.aDataBase = DataBase
        self.connection = None
        self.cursor = None
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.aHost,
                user=self.aUser,
                password=self.aPassword,
                database=self.aDataBase
            )
            self.cursor = self.connection.cursor(dictionary=True)
        except Exception as e:
            err = str(e) + ":" + str(sys.exc_info())
            return err
        return ""
    def close(self):
        try:
            self.connection.close()
            self.cursor.close()
            return ""
        except Exception as e:
            err = str(e) + ":" + str(sys.exc_info())
            return err
    def fetchdata(self):
        if self.cursor is None: return []
        try:
            data = self.cursor.fetchall()
            return data if isinstance(data, list) else []
        except Exception as e:
            err = []
            err.append(str(e))
            return err
    def execute(self,aQuery,aParams=None):
        try:
            if aParams: self.cursor.execute(aQuery,aParams)
            else:
                self.cursor.execute(aQuery)
            self.connection.commit()
            return ""
        except Exception as e:
            err = str(e) + ":" + str(sys.exc_info())
            return err
            

def clear_screen():
    os.system("clear")
def wait(seconds:float):
    sleep(seconds)
def GetTime():
    return datetime.now()
def GetFuncName(aFunc):
    return aFunc.__name__

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
# Calculate a random number
def random_number(aInterval:list[2]):
    num=random.randrange(start=aInterval[0],stop=aInterval[1])
    return num
