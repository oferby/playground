import random

drow = 0
success = 0

total = 0

for j in range(100):
    for i in range(1000):
        while True:
            dice = random.randint(1, 6)
            if dice != 3:
                dice = random.randint(1, 6)
                drow += 1
                if dice == 3:
                    success += 1
                break

    val = success / drow
    print(val)
    total += val

print('after 100 tries: ', str(total / 100))
