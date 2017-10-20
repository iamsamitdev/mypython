import pyodbc

con_string = 'driver=MySQL ODBC 5.3 Unicode Driver;' \
             'server=localhost;database=pythontestdb;' \
             'uid=root;pwd=1234'


def create_table():
    with pyodbc.connect(con_string) as con:
        sql_cmd = """
            create table person(
              id int PRIMARY KEY AUTO_INCREMENT,
              gender char(1),
              weight float,
              height float
            )
        """
        try:
            con.execute(sql_cmd)
        except pyodbc.ProgrammingError:
            print('Aready have tabble')


def insert_data():
    with pyodbc.connect(con_string) as con:
        sql_cmd = """
           insert into person(gender, weight, height)
           VALUES('M', 54, 180)
        """
        con.execute(sql_cmd)


def select_data():
    with pyodbc.connect(con_string) as con:
        sql_cmd = """
            select * from person;
         """
        for row in con.execute(sql_cmd):
            # print(row)
            print(row[1], row[2], row[3])


if __name__ == '__main__':
    #create_table()
    insert_data()
    select_data()
