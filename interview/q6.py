# you are traveler on 2d grid
# how many routes to target
# if you can only move down and right

size = [3, 5]
target = [1, 2]
start = [0, 0]


def check_next(position):
    if position == target:
        return 1
    if position[1] < size[1]:
        right = check_next([position[0], position[1] + 1])
    else:
        right = 0
    if position[0] < size[0]:
        down = check_next([position[0] + 1, position[1]])
    else:
        down = 0
    return right + down


print(check_next(start))
