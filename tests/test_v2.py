import sys
import os

# Import the module
sys.path.append(os.path.dirname(os.path.dirname("utils/utils.py")))
from utils import *

factOfNum = Factorial(10)
print(factOfNum)
