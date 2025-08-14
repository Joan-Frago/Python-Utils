import requests
import csv
from datetime import datetime,timedelta
import pytz
import sys
import os
import random
from openpyxl import load_workbook
from time import sleep,time
import mysql.connector
import json
import re

if sys.version_info < (3,9):
    from typing import List,Dict,Union
    ListType=List
    DictType=Dict
    UnionType=Union
else:
    ListType=list
    DictType=dict
    UnionType=lambda *args:args[0] | args[1]

class Logger:
    def __init__(self,
                 log_path:str="log/pylog.log"
                 ,enable_rotation=False
                 ,max_log_file_size=20000):
        self.log_file = log_path
        self.log_path = self.get_log_path()
        self.rotate_log = enable_rotation
        self.iFileThreshold=max_log_file_size # file size in kbs
        create_file(aFilePath=self.log_file)

    def get_log_path(self):
        return os.path.dirname(self.log_file)
    
    @staticmethod
    def on_register_func_call(func):
        def wrapper(self,*args,**kwargs):
            if self.rotate_log:
                self.log_file_rotation()
            return func(self,*args,**kwargs)
        return wrapper

    def get_last_log(self) -> int:
        """
        Scans through the log directory and returns
        the number of log files there are
        """
        iFunc=GetFuncName(self.get_last_log)
        try:
            if not os.path.exists(self.log_path):return 0
            all_logs=os.scandir(self.log_path)
            all_logs_lst=[i.name for i in all_logs]
            return len(all_logs_lst)
            
        except Exception as e:
            err=iFunc + ":" + str(sys.exc_info()) + ":" + str(e)
            raise Exception(err)
    
    def log_file_rotation(self):
        try:
            last_log_num=self.get_last_log()
            if last_log_num<=0:iLogFileName=self.log_file
            else:
                if last_log_num==1:
                    iLogFileName=self.log_file
                else:
                    iLogFileName=self.log_file.split("_")[0] if "_" in self.log_file else self.log_file
                    iLogFileName+="_"+str(last_log_num+1)
                iLogFileSize=get_file_size(aFile=iLogFileName)
                if iLogFileSize<self.iFileThreshold:
                    return
                else:
                    self.log_file=iLogFileName
        except Exception as e:
            raise Exception(e)

    @on_register_func_call
    def write_log(self, aLog:str, type_log:str = "ERROR   "):
        if not os.path.exists(self.log_file):
            try:
                os.makedirs(self.log_path,exist_ok=True)
                create_file(self.log_file)
            except Exception as e:
                err=f"Error creating log file: {str(e)} : {str(sys.exc_info())}"
                raise Exception(err)

        text = f"{datetime.now()} {type_log} {aLog}"
        writeFile(aFile=self.log_file,aContent=text,fileMode="a",newLine=True)

    def error(self,log:str):
        self.write_log(type_log="ERROR   ",aLog=log)
    def warning(self,log:str):
        self.write_log(type_log="WARNING ",aLog=log)
    def info(self,log:str):
        self.write_log(type_log="INFO    ",aLog=log)
    def debug(self,log:str):
        self.write_log(type_log="DEBUG   ",aLog=log)
    
    def exception_handler(self,exc_type,exc_value,exc_traceback):
        err="Unhandled Exception : "
        err+=str(exc_type)+" : "
        err+=str(exc_value)+" : "
        err+=str(exc_traceback)
        self.error(err)
    
    @staticmethod
    def get_logger_type(aLogger):
        if type(aLogger) == Logger:
            return aLogger
        else:
            logger=DefaultLogger()
            return logger

class DefaultLogger(Logger):
    def write_log(self,aLog:str="No output specified",type_log:str="ERROR   "):
        text = f"{datetime.now()} {type_log} {aLog}"
        print(text, file=sys.stdout, flush=True)

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
        else:
            final_time=str(round(self.finish_time,3))+" seconds"
        return final_time

class DataBase:
    def __init__(self,Host:str,User:str,Password:str,DataBase:str,buffered:bool=False):
        self.aHost = Host
        self.aUser = User
        self.aPassword = Password
        self.aDataBase = DataBase
        self.buffered = buffered
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
            self.cursor = self.connection.cursor(dictionary=True,buffered=self.buffered)
            # --------------------------------------------------------------------------------------------------#
            #                                                                                                   #
            #       UNREAD RESULT FOUND mysql                                                                   #
            #                                                                                                   #
            # The reason is that without a buffered cursor, the results are "lazily" loaded,                    #
            # meaning that "fetchone" actually only fetches one row from the full result set of the query.      #
            # When you will use the same cursor again, it will complain that you still have n-1 results         #
            # (where n is the result set amount) waiting to be fetched. However, when you use a buffered        #
            # cursor the connector fetches ALL rows behind the scenes and you just take one from the connector  #
            # so the mysql db won't complain.                                                                   #
            #                                                                                                   #
            # --------------------------------------------------------------------------------------------------#
        except Exception as e:
            err = "Error trying to connect to database : DataBase.connect func : "+str(e) + ":" + str(sys.exc_info())
            raise Exception(err)
    def close(self):
        try:
            if self.connection is not None: self.connection.close()
            if self.cursor is not None: self.cursor.close()
        except Exception as e:
            err = "Error trying to close data base : DataBase.close func : "
            err+=str(e) + ":" + str(sys.exc_info())
            raise Exception(err)
    def fetchdata(self):
        if self.cursor is None: return []
        try:
            data = self.cursor.fetchall()
            return data if isinstance(data, list) else []
        except Exception as e:
            raise Exception(e)
    def execute(self,aQuery,aParams=None,DebugMode=False) -> str | None:
        try:
            if DebugMode:
                for param in aParams:
                    aQuery=re.sub(pattern=r"%s",repl=str(param),string=aQuery,count=1)
                return aQuery
            if self.cursor is not None and self.connection is not None:
                if aParams: self.cursor.execute(aQuery,aParams)
                else: self.cursor.execute(aQuery)
                self.connection.commit()
        except Exception as e:
            err = "Error in DataBase.execute function: "+str(e) + ":" + str(sys.exc_info())
            raise Exception(err)
    def get_last_row_id(self):
        try:
            if self.cursor is None:
                err="In get_last_row_id function: "
                err+="Can't get the id of the last row fetched because "
                err+="there is no cursor initialized"
                raise Exception(err)
            
            return self.cursor.lastrowid
        except Exception as e:
            err="Error in get_last_row_id function: "
            err+=str(e)+" : "+str(sys.exc_info())
            raise Exception(e)
        

def clear_screen():
    try:
        os.system("clear")
    except OSError:
        os.system("cls")
    except Exception as e:
        print("Could not clear screen because of: "+str(e))
def wait(seconds:float):
    sleep(seconds)

def NormDate(aDate:str):
	"""
	Normalize a date coming from raw html form
	
	It must enter with the following format
	* 2023-12-20T15:29

	It must return with the following format
	* 2023-12-20 15:29
	"""
	if not "T" in aDate:
		return aDate
	iDate=aDate.replace("T"," ")
	return iDate

def get_file_size(aFile):
    try:
        iFileStats=os.stat(aFile)
        iFileSize=iFileStats.st_size
        iFileSize=iFileSize/1000
        return iFileSize
    except Exception as e:
        raise Exception(e)
def create_file(aFilePath:str):
    try:
        open(aFilePath,"x")
    except FileExistsError:
        pass
def string2bytes(aString:str) -> bytes:
    try:
        byte_str=aString.encode("utf-8")
        return byte_str
    except Exception as e:
        err="Int string2bytes function. Error: Could not "
        err+="encode the given string : "+str(e)+str(sys.exc_info())
        raise Exception(err)
def GetTime(aTimeZone:str="Europe/Madrid",accuracy:str="ml",is_string:bool=True) -> datetime | str:
    """
    ## Get the actual time

    * **aTimezone** defaults to Europe/Madrid, but can be set to any pytz.timezone
    * **accuracy** sets the accuracy for the time, defaults to milisecond:
        * milisecond --> "ml"
        * second --> "s"
        * minute --> "mn"
        * hour --> "h"
        * day --> "d"
        * month --> "m"
        * year --> "y"
        
    """
    # 2025-04-27 21:13:57.904277+02:00
    try:
        iTime=datetime.now(pytz.timezone(aTimeZone))
        
        if not is_string: return iTime
        
        iTime=str(iTime)
        match accuracy:
            case "ml":
                iTime=iTime[:-6]
            case "s":
                iTime=iTime[:-13]
            case "mn":
                iTime=iTime[:-16]
            case "h":
                iTime=iTime[:-19]
            case "d":
                iTime=iTime[:-22]
            case "m":
                iTime=iTime[:-25]
            case "y":
                iTime=iTime[:-28]
        return iTime
    except Exception as e:
        err="Error in GetTime func : "+str(e)+" : "+str(sys.exc_info())
        raise Exception(err)
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
            raise Exception("Please provide a path for file reading")
    except IOError as e:
        raise Exception(f"Could not read {aFile} contents due to {e}")
# Write a File
def writeFile(aFile:str,aContent:str|bytes,fileMode="w",newLine:bool=False):
    if newLine == True:
        if isinstance(aContent,bytes): aContent+=b'\n'
        else: aContent+='\n'

    try:
        if aFile != "":
            with open(aFile,fileMode) as file:
                file.write(aContent)
        else:
            raise IOError("No file path provided")
    except IOError as e:
        return f"Could not write to {aFile} due to: {e}"
# Get Json Data
def getJsonData(aUrl:str,aParams:list[tuple] | None=None,aAuth:tuple[str] | None=None,aHeaders:dict[str] | None=None) -> dict | list:
    """
    aParams --> list of tuples
    """
    try:
        response = requests.get(url=aUrl,params=aParams,auth=aAuth,headers=aHeaders)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error":str(response.status_code)
                    ,"reason":str(response.reason)
                    ,"description":str(response.text)}
    except Exception as e:
        return {"ERROR":str(e)}
# Post Json Data
def postJsonData(aUrl:str,aData:dict) -> dict:
    try:
        response = requests.post(url=aUrl,data=aData)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error":str(response.status_code)
                    ,"reason":str(response.reason)
                    ,"description":str(response.text)}
    except Exception as e:
        return {"ERROR":str(e)}
def putJsonData(aUrl:str,aData:dict,aAuth:tuple[str] | None=None,aHeaders:dict | None=None) -> dict:
    try:
        response = requests.put(url=aUrl,data=aData,headers=aHeaders,auth=aAuth)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error":str(response.status_code)
                    ,"reason":str(response.reason)
                    ,"description":str(response.text)}
    except Exception as e:
        return {"ERROR":str(e)}
# Read a CSV
def csv2Dict(aFile:str,aDelimiter=None) -> dict:
    try:
        csvDict={}
        with open(aFile,mode="r") as file:
            csv2dict = csv.DictReader(file,aDelimiter)
            for row in csv2dict:
                csvDict[str(row)]=row
        return csvDict
    except Exception as e:
        return {"error":str(e)}
def GetEpochTimestamp(aDate:tuple[int] |None=None):
    if aDate is None:
        iDate=datetime.now()
    else:
        iDate=datetime(aDate[0],aDate[1],aDate[2],aDate[3],aDate[4],aDate[5])
    iTs=datetime.timestamp(iDate)
    return iTs
# Convert Date to Timestamp
def Date2Timestamp(dateTime) -> float:
    timestamp = datetime.timestamp(dateTime)
    return timestamp
# Convert Timestamp to Date
def Timestamp2Date(timeStamp:int,timeZone=None):
    date = datetime.fromtimestamp(timeStamp,timeZone)
    return date
# Calculate the difference between two timestamp
def TimestampTimeDiff(aTimestamp,aTimestamp2=None) -> int:
    if aTimestamp2 is not None:
        timeDiff=aTimestamp2-aTimestamp
    else:
        iTime=datetime.now()
        iTs=int(datetime.timestamp(iTime))
        timeDiff = iTs - aTimestamp
    return timeDiff
# Calculate the difference between two date times
def DateTimeTimeDiff(dateTime) -> int:
    iTime = datetime.now()
    timeDiff = iTime - dateTime
    return timeDiff
# Check if a number is prime
def IsPrime(aNum:int) -> bool:
    try:
        for i in range(1, aNum):
            if aNum % i == 0 and i != aNum:
                return True
            else:
                return False
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
def loadExcel(aFile:str, aSheet:str = ""):
    wb = load_workbook(aFile)
    if wb is None: return None
    if aSheet != "":
        ws = wb[aSheet]
    else:
        ws = wb.active()
    return ws
# Calculate a random number
def random_number(aInterval:ListType[int]):
    num=random.randrange(start=aInterval[0],stop=aInterval[1])
    return num
# Get JSON data
def get_json_data(aJsonFileDir:str) -> dict:
    try:
        iJsonFile=readFile(aFile=aJsonFileDir)
        if not iJsonFile.strip(): # check if file is empty
            raise ValueError(f"JSON file {aJsonFileDir} is empty")
        iDic=json.loads(iJsonFile)
        return iDic
    except json.JSONDecodeError as e:
        raise Exception(f"Invalid JSON format in {aJsonFileDir}: {e}")
    except Exception as e:
        raise Exception(f"Error reading JSON file {aJsonFileDir}: {e}")
def dict2json(aDict:dict):
    iJson=json.dumps(aDict)
    return iJson

