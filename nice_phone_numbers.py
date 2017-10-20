import Mymodule

# รับค่าเบอร์โทรจากผู้ใช้
phone = ""
while True:
    try:
        if phone != 'exit':
            phone = input("Enter your phone number : ")
            print("Your phone number is ", phone)
            print(Mymodule.interpet(Mymodule.sum_phone_digit(phone)))
        else:
            break
    except ValueError:
        print("ป้อนเบอร์ไม่ถูกต้อง")
        continue

print("Aready exit!!!")
print("OK")

