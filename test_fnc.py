# create new function


def printme(str_data):
    "This is comment in function"
    print(str_data)
    return


def sumdata(data1, data2):
    print(int(data1) // int(data2))
    return


# default parameter in function
def printinfo(name="Anynomous", age="30"):
    print("Hello ", name, " your age is ", age)
    return


# variable-length in function
def printinfo2(name="Anynomous", *number):
    print("Hello ", name)
    for val in number:
        print(val)
    return


# lambda function
sum_value = lambda d1, d2: d1 + d2
print("Sum data = ", sum_value(8, 2))

# call to funciton printme()
# 1. call in console
# 2. call in project file
# 3. call from exteranal modul

printme("Hello Python")
printme(str_data="Welcome to python function")
sumdata(3, 5)
sumdata(data2=5, data1=30)
printinfo()
printinfo(name="สามิตร")
printinfo2("Samit", 10, 20, 30, 40)
