# open file
f = open("mydata.txt", "a")
print(f.name, f.mode)


# read all file
def read_all():
    f = open("mydata.txt","r")
    data = f.read()
    print(data)
    f.close()


# read line file
def read_line():
    f = open("mydata.txt", "r")
    data = f.readline()
    print(data)
    f.close()


# read line specify line number
def read_line_with_number():
    f = open("mydata.txt", "r")
    for i in range(2,5):
        print(f.readline())
    f.close()


def readline_list():
    f = open("mydata.txt", "r")
    for line in f:
        print(line,end="")
    f.close()

# read_all()
# read_line()
# read_line_with_number()
readline_list()