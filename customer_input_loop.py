a = []
while True:
    b = input('ร้านค้า\nเพิ่ม[a] แสดง[s] ออกจากระบบ[x] : ')
    b = b.lower()
    if b == 'a':
        c = input('ป้อนรายการลูกค้า : ')
        a.append(c)
        print('***ข้อมูลได้เข้าสู่ระบบแล้ว')
    elif b == 's':
        print('{0:-<6}{0:-<10}{0:-<10}'.format(""))
        print('{0:-<6}{1:<10}{2:10}'.format('รหัส', 'ชื่อ', 'จังหวัด'))
        print('{0:-<6}{0:-<10}{0:-<10}'.format(""))
        for d in a:
            e = d.split(":")
            print('{0[0]:<6}{0[1]:<10}({0[2]:10})'.format(e))
            continue
    elif b == 'x':
        break
print('ทำคำสั่งถัดไป')