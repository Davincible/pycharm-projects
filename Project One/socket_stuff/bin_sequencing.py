from bitstring import BitStream, ReadError
from math import sqrt
from bisect import bisect_left
# add multiple channels
# time different addition methods


def slice(data, channels=2):
    print("Original data: {}, type: {}".format(data, type(data)))
    data = str(data).encode()
    data_array = BitStream(data)
    channel_options = []
    for i in range(1, round(sqrt(data_array.len))):
        if data_array.len % i is 0:
            channel_options.insert(bisect_left(channel_options, i), i)
            channel_options.insert(bisect_left(channel_options, int(data_array.len / i)), int(data_array.len / i))
    print("channel options:", channel_options)
    channels = takeClosest(channel_options, channels)
    print("Chanels:", channels)
    output = {}
    for channel in range(1, channels + 1):
        output[channel] = BitStream()

    while data_array.pos < data_array.len:
        # print('reading:', data_array.pos, data_array.len)
        # left.append('0b' + data_array.read('bin:1'))
        # right.append('0b' + data_array.read('bin:1'))

        for channel in range(1, channels + 1):
            try:
                output[channel].append('0b' + data_array.read('bin:1'))
            except ReadError as e:
                print("ReadError on pos {}, for length {}".format(data_array.pos, data_array.len))
                print("Error:", e)
                break

    print("Original binary:", data_array.bin)
    for channel in output:
        print(output[channel].bin)
    return output

def takeClosest(myList, myNumber):
    """
    Assumes myList is sorted. Returns closest value to myNumber.

    If two numbers are equally close, return the smallest number.
    """
    pos = bisect_left(myList, myNumber)
    if pos == 0:
        return myList[0]
    if pos == len(myList):
        return myList[-1]
    before = myList[pos - 1]
    after = myList[pos]
    if after - myNumber < myNumber - before:
       return after
    else:
       return before

slice(input('message: '), int(input('channels: ')))