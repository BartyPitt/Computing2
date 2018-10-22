from math import *
import numpy as np
from operator import add
print("hello")
for i in range(10):
    print (i)
class test:
    def __init__(self,a,b):
        self.a = a
        self.b = b
def testgen(x):
    for i in range (x):
        yield i**2
for i in testgen(4):
    print (i)

a = [1,2,3]
b = [2,3,4]
c = add(a,b)
print (c)
