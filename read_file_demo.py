def demo_reader():
    with open("flower.txt") as f:
        data = f.read()
        print(data)


def demo_readline():
    with open("flower.txt") as f:
        data = f.readline()
        print(data)
        data2 = f.readline()
        print(data2)


def demo_readlines():
    with open("flower.txt") as f:
        data = f.readlines()
        print(data)


def demo_readline2():
    with open("flower.txt") as f:
        for _ in range(3):
            print(f.readline(), end="")


def demo_readlines2():
    with open("flower.txt") as f:
        for line in f:
            print(line.capitalize(), end="")


# demo_reader()
# demo_readline()
# demo_readlines()
# demo_readline2()
# demo_readlines2()
