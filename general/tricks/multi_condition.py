score = 1
time = 100
found = False

list_of_conditions = [score < 10, time < 255, not found]

if (all(list_of_conditions)):
    print("all conditions are true")
else:
    print("not all conditions are true")

