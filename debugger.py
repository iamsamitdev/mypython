import random


def sum_digit(n):
    s = str(n)
    return sum(int(c) for c in s)


def dice():
    for _ in range(10):
        n = random.randint(1,6)
        print(n)

# print(sum_digit(12345))
dice()