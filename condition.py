# input_data = int(input("Enter nubmer :"))
#
# if input_data >= 10:
#     print("Large number")
# else:
#     print("Normal nubmer")

data = int(input("Enter your scroe: "))

if data >= 80 and data <= 100:
    print("Grade A")
elif data >= 70 and data <= 79:
    print("Grade B")
elif data <= 0:
    print("Invalid value")


# loop while
count = 1
while count <= 10:
    if count % 2 == 0:
        print("Good luck")
    else:
        print("Line ", count)
    count += 1

x = 1

