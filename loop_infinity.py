count = 1
sum_data = 0

while True:

    try:
        number_input = input('Input number %d : ' % count)
        if number_input != 'exit':
            sum_data += int(number_input)
        else:
            break
        count += 1
    except ValueError:
        print('Please enter a number')
        continue

print('Sumary value is ',sum_data)
print('Exit Now!!')