import pyodbc

con_string = 'driver=MySQL ODBC 5.3 Unicode Driver;' \
             'server=localhost;' \
             'database=pythonddata;' \
             'uid=root;' \
             'pwd=1234'


# print(con_string)
# print(pyodbc.connect(con_string))

# สร้างตารางด้วย python
def create_table():
    with pyodbc.connect(con_string) as con:
        sql_cmd = """
            create table person(
              id int PRIMARY KEY AUTO_INCREMENT,
              name varchar(255),
              weight float,
              height float
            )
        """

        try:
            con.execute(sql_cmd)
        except pyodbc.ProgrammingError:
            print('Aready have table')


# เพิ่มข้อมูลลงตาราง
def insert_data():
    with pyodbc.connect(con_string) as con:
        sql_cmd = """
            INSERT INTO person(name,weight,height)
            VALUES('Samit',60,165);
        """
        con.execute(sql_cmd)


# ดึงข้อมูลออกมาแสดง
def select_data():
    with pyodbc.connect(con_string) as con:
        sql_cmd = """
            SELECT * FROM person;
        """
        for row in con.execute(sql_cmd):
            print(row)


# เรียกใช้งานฟังก์ชันสร้างตาราง
# create_table()

# เรียกใช้ฟังก์ชันบันทึกข้อมูลลงตาราง
# insert_data()

# เรียกใช้ฟังชันดึงข้อมูลออกมาแสดง
select_data()
