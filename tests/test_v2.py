import sys
import os
from datetime import datetime
import random

# Import the module
sys.path.append(os.path.dirname(os.path.dirname("utils/utils.py")))
from utils import *

"""iFile="testFile.txt"
iContent="djfaoijgjds ----- test -----"
writeFile(iFile,iContent,newLine=True)

outFile = readFile(iFile)
print(outFile)"""

num = random.randint(1,100000)
prime = IsPrime(num)
print(prime)
