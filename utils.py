import requests
import csv
from datetime import datetime

class Utils:
    def __init__(self, afile:str = None, acontent:str = None, aUrl:str = None, headers:dict = None, body:dict = None, dateTime = None, timeStamp:str = None, timeZone = None, adelimiter:str = None):
        self.afile = afile
        self.acontent = acontent
        self.aUrl = aUrl
        self.headers = headers
        self.body = body
        self.dateTime = dateTime
        self.timeStamp = timeStamp
        self.timeZone = timeZone
        self.adelimiter = adelimiter

    # Read a File
    def readFile(self):
        try:
            if self.afile != "":
                with open(self.afile,"r") as file:
                    content=file.read()
                return content
            else:
                return "Please provide a path for file reading"
        except IOError as e:
            return f"Could not read {self.afile} contents due to {e}"

    # Write a File
    def writeFile(self):
        try:
            if self.afile != "":
                with open(self.afile,"w") as file:
                    file.write(self.acontent)
            else:
                return "Please provide a path for file reading"
        except IOError as e:
            return f"Could not write to {self.afile} due to {e}"

    def getJsonData(self):
        try:
            response = requests.get(self.aUrl, self.headers)
            if response.status_code == 200:
                data = response.json()
            else:
                return f"Error: {response.status_code}"
            return data
        except Exception as e:
            return f"ERROR: {e}"
        
    def postJsonData(self):
        try:
            response = requests.post(self.aUrl, json=self.body)
            if response.status_code == 200:
                data = response.json()
            else:
                return f"Error: {response.status_code}"
            return data
        except Exception as e:
            return f"ERROR: {e}"
    
    def readCSV(self):
        try:
            csvDict = []
            with open(self.afile,mode="r") as file:
                csv2dict = csv.DictReader(file,self.adelimiter)
                for row in csv2dict:
                    csvDict.append(row)
            return csvDict

        except Exception as e:
            return e
    
    def Date2Timestamp(self):
        timestamp = int(datetime.timestamp(self.dateTime))

        return timestamp

    def Timestamp2Date(self):
        date = datetime.fromtimestamp(self.timeStamp,tz=self.timeZone)
        return date

    def TimestampTimeDiff(self):
        iTime = datetime.now()
        utils = Utils(dateTime=iTime)
        iTime = utils.Date2Timestamp()
        timeDiff = iTime - self.timeStamp

        return timeDiff
    
    def DateTimeDiff(self):
        iTime = datetime.now()
        timeDiff = iTime - self.dateTime

        return timeDiff    