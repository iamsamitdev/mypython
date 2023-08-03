# open file
f = open("mydata.txt", "a")
print(f.name, f.mode)


# read all file
def read_all():
    with open("mydata.txt","r") as f:
        data = f.read()
        print(data)


# read line file
def read_line():
    with open("mydata.txt", "r") as f:
        data = f.readline()
        print(data)


# read line specify line number
def read_line_with_number():
    with open("mydata.txt", "r") as f:
        for _ in range(2,5):
            print(f.readline())


def readline_list():
    with open("mydata.txt", "r") as f:
        for line in f:
            print(line,end="")

# read_all()
# read_line()
# read_line_with_number()
readline_list()