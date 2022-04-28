# You're given a list of n integers arr[0..(n-1)].
# You must compute a list output[0..(n-1)] such that,
# for each index i (between 0 and n-1, inclusive),
# output[i] is equal to the product of the three largest elements out of
# arr[0..i] (or equal to -1 if i < 2, as arr[0..i] then includes fewer than three elements).

import math


# Add any extra import statements you may need here


# Add any helper functions you may need here


def findMaxProduct(arr):
    # Write your code here
    result = [-1, -1]
    max_3 = arr[0:3]
    result.append(arr[0] * arr[1] * arr[2])
    for i in range(3, len(arr)):
        max_3.append(arr[i])
        max_3 = sorted(max_3)
        max_3 = max_3[1:4]
        result.append(max_3[0]*max_3[1]*max_3[2])

    return result

    # These are the tests we use to determine if the solution is correct.


# You can add your own at the bottom.

def printInteger(n):
    print('[', n, ']', sep='', end='')


def printIntegerList(array):
    size = len(array)
    print('[', end='')
    for i in range(size):
        if i != 0:
            print(', ', end='')
        print(array[i], end='')
    print(']', end='')


test_case_number = 1


def check(expected, output):
    global test_case_number
    expected_size = len(expected)
    output_size = len(output)
    result = True
    if expected_size != output_size:
        result = False
    for i in range(min(expected_size, output_size)):
        result &= (output[i] == expected[i])
    rightTick = '\u2713'
    wrongTick = '\u2717'
    if result:
        print(rightTick, 'Test #', test_case_number, sep='')
    else:
        print(wrongTick, 'Test #', test_case_number, ': Expected ', sep='', end='')
        printIntegerList(expected)
        print(' Your output: ', end='')
        printIntegerList(output)
        print()
    test_case_number += 1


if __name__ == "__main__":
    arr_1 = [1, 2, 3, 4, 5]
    expected_1 = [-1, -1, 6, 24, 60]
    output_1 = findMaxProduct(arr_1)
    check(expected_1, output_1)

    arr_2 = [2, 4, 7, 1, 5, 3]
    expected_2 = [-1, -1, 56, 56, 140, 140]
    output_2 = findMaxProduct(arr_2)
    check(expected_2, output_2)
