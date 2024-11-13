class Utils:
    def __init__(self, afile:None, acontent:None):
        self.afile = afile
    
    # Read a File
    def readFile(self):
        with open(self.afile,"r") as file:
            content=file.read()
        return content
    
    # Write a File
    def writeFile(self):
        with open(self.afile,"w") as file:
            file.write(self.acontent)
            