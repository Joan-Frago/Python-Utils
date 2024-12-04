import sys
import os
from datetime import datetime

# Import the module
sys.path.append(os.path.dirname(os.path.dirname("utils.py")))
from utils import *

iFile="testFile.txt"
iContent="djfaoijgjds ----- test -----"
writeFile(iFile,iContent,newLine=True)

outFile = readFile(iFile)
print(outFile)
