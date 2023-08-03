var1 = "Python Programming"
var2 = "สวัสดีทุกท่าน"
print(var1)

print(var1[5])
print(var2[6])
print(var1[:6])
print(var1[-1])
print(var1[:10])

data_text = "I hate Python"
print(data_text.replace("hates", "love"))

อาหารไทย = "ต้มยำกุ้ง"
print(อาหารไทย)

# list in python
my_list = [1, 2, 3, "Apple", '4', 3.14]

# Empty list
my_emp_list = [100, "Fruit", "Food"]

# my_emp_list.insert('Beer', 2)

# delet member
del my_emp_list[:3]
# my_emp_list.remove("Fruit")


print(my_list[3])
print(my_list[-2])
print(my_list[:4])
print(my_emp_list)
print(my_list)

# array length
# print(len(my_list))

list1 = [6, 4, 3, 8, 12, 14]
list2 = [2, 3, 4, 9, 7, 5]
print(len(my_list))

# loop array member
for val in my_list:
    print(val)

print(list1 < list2)

sumdata = sum(list1)
print(sumdata)

profile = (("name", "Samit Koyom"), ("Age", "30"), ("Gender", "Male"))
print(profile[0][1])
print(profile[1][1])
print(profile[2][1])

for val in profile:
    print(val[1])

# Dictionary

dict_data = {
    'name':     'Zara',
    'age':      20,
    'gender':   'female'
}

print(dict_data)
print("My name is ", dict_data['name'])

dict_emp = {'id': 1, 'product': 'iPhone X'}

print(dict_emp)

# update value of dictionary
dict_emp['product'] = 'iPhone 8'
print(dict_emp)

# remove member all in dictinary
dict_emp.clear()
print(dict_emp)

# remove by key
del dict_data['name']
print(dict_data)

for value in dict_data.values():
    print(value)