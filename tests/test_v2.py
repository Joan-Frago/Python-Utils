import sys
import os

# Import the module
sys.path.append(os.path.dirname(os.path.dirname("utils/utils.py")))
from utils import *

interval=[1,100]
random_num = random_number(interval)
print(random_num)

