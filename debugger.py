import random


def sum_digit(n):
    s = str(n)
    t = 0
    for c in s:
        t += int(c)
    return t


def dice():
    for i in range(10):
        n = random.randint(1,6)
        print(n)

# print(sum_digit(12345))
dice()