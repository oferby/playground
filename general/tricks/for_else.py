# loop with condition without binary variable

# old way
numbers = [1, 2, 3, 4]
# numbers = [10, 2, 8, 4]
foundOdd = False

for number in numbers:
    if number % 2 != 0:
        foundOdd = True
        print("not all numbers are even")
        break

if not foundOdd:
    print("all numbers are even")

print("new way:")
for number in numbers:
    if number % 2 != 0:
        print("not all numbers are even")
        break

else:
    print("all numbers are even")
