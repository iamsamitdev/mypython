# load from module
# import CalRectangleArea # method 1
# from CalRectangleArea import squre, parallelogram  # method 2
# from CalRectangleArea import * # method 3
# import math
# import sys

# load form package
import CalcArea
print(CalcArea.squre(30,10))
print(CalcArea.triangle(30,10))

# from CalcArea import CalRectangleArea as CRA

# print(CalRectangleArea.squre(10, 30)) # call method 1
# print(squre(10, 30))  # call method 2 and method 3
# print(parallelogram(5, 10))  # call method 2 and method 3
# print(CRA.squre(10, 60))  # call method 4
# print(dir(CRA))
# print(dir(math))
# print(sys.path)