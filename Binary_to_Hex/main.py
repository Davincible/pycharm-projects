user_input = input("What binary code do you want to convert?: ")

binhexdict = {
    '0000': '0',
    '0001': '1',
    '0010': '2',
    '0011': '3',
    '0100': '4',
    '0101': '5',
    '0110': '6',
    '0111': '7',
    '1000': '8',
    '1001': '9',
    '1010': 'A',
    '1011': 'B',
    '1100': 'C',
    '1101': 'D',
    '1110': 'E',
    '1111': 'F'}


input_list = [None, None, None, None]
output_list = []
index = 0
try:
    for i in user_input:
        if i == ' ':
            index = 0
            for i in range(len(input_list)):
                input_list[i] = None
            continue
        else:
            input_list[index] = i
            index += 1
            if index == 4:
                output_list.append(binhexdict[''.join(input_list)])
except (KeyError, IndexError):
    print("Invalid Input")
    quit()

print(''.join(output_list))
