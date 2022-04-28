# It takes you 1 minute to eat all of the pieces of candy in a bag
# (irrespective of how many pieces of candy are inside), and as soon as you finish,
# the bag mysteriously refills. If there were x pieces of candy in the bag at
# the beginning of the minute, then after you've finished you'll find that floor(x/2) pieces are now inside.
# You have k minutes to eat as much candy as possible. How many pieces of candy can you eat?

import math


# Add any extra import statements you may need here


# Add any helper functions you may need here


def maxCandies(arr, k):
    # Write your code here
    result = 0
    arr = sorted(arr, reverse=True)

    while (k > 0):
        result += arr[0]
        k -= 1
        arr[0] = math.floor(arr[0] / 2)

        for i in range(len(arr) - 1):
            if arr[i] < arr[i + 1]:
                tmp = arr[i + 1]
                arr[i + 1] = arr[i]
                arr[i] = tmp
            else:
                break

    return result


# These are the tests we use to determine if the solution is correct.
# You can add your own at the bottom.

def printInteger(n):
    print('[', n, ']', sep='', end='')


test_case_number = 1


def check(expected, output):
    global test_case_number
    result = False
    if expected == output:
        result = True
    rightTick = '\u2713'
    wrongTick = '\u2717'
    if result:
        print(rightTick, 'Test #', test_case_number, sep='')
    else:
        print(wrongTick, 'Test #', test_case_number, ': Expected ', sep='', end='')
        printInteger(expected)
        print(' Your output: ', end='')
        printInteger(output)
        print()
    test_case_number += 1


if __name__ == "__main__":
    n_1, k_1 = 5, 3
    arr_1 = [2, 1, 7, 4, 2]
    expected_1 = 14
    output_1 = maxCandies(arr_1, k_1)
    check(expected_1, output_1)

    n_2, k_2 = 9, 3
    arr_2 = [19, 78, 76, 72, 48, 8, 24, 74, 29]
    expected_2 = 228
    output_2 = maxCandies(arr_2, k_2)
    check(expected_2, output_2)

    # Add your own test cases here
