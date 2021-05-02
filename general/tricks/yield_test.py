def generate_number(limit):
    for num in range(1, limit + 1):
        yield num * 11


numbers = generate_number(1000)

for i in range(10):
    print(i, ": ", next(numbers))
