import cv2
import numpy as np
from pomdp.robot import bot
import pomdp.robot.worlds as worlds
import time

font = cv2.FONT_HERSHEY_SIMPLEX
render = True
wait_time = 300
supervised = False


def callback(t):
    global wait_time
    if t == 0:
        wait_time = 1
    else:
        wait_time = t


world, goal_loc = worlds.get_world(1)
if render:
    window_name = "Image"
    cv2.namedWindow(window_name)
    cv2.moveWindow(window_name, 80, 80)
    cv2.createTrackbar("Wait time", window_name, 20, 100, callback)

x = worlds.x
y = worlds.y

robot = bot.Robot()


def get_reward():
    x1, y1 = goal_loc[0]
    x2, y2 = goal_loc[1]

    if robot.sensors[4] and (x1 - 11 <= x <= x2 + 11) and (y1 - 11 <= y <= y2 + 11):
        return 1000
    return -1


def get_new_position(action):
    global x, y
    if action == 0 and x > 10 and np.array_equal(world[y, x - 11], [0, 0, 0]):
        x -= 1
    elif action == 1 and y > 10 and np.array_equal(world[y - 11, x], [0, 0, 0]):
        y -= 1
    elif action == 2 and x < 390 and np.array_equal(world[y, x + 11], [0, 0, 0]):
        x += 1
    elif action == 3 and y < 390 and np.array_equal(world[y + 11, x], [0, 0, 0]):
        y += 1


def clean_position():
    global world
    world[y, x] = [0, 0, 0]


r = 0
turns = 0
while True:

    robot.update_sensors([world, [y, x]])

    if render:
        img = world.copy()
        sensors = robot.sensors
        cv2.line(img, (x, y), (x - sensors[0] - 10, y), (125, 125, 125), 1)
        cv2.line(img, (x, y), (x, y - sensors[1] - 10), (125, 125, 125), 1)
        cv2.line(img, (x, y), (x + sensors[2] + 10, y), (125, 125, 125), 1)
        cv2.line(img, (x, y), (x, y + sensors[3] + 10), (125, 125, 125), 1)
        cv2.circle(img, (x, y), 10, (255, 0, 0), -1)
        left = 'Left: ' + str(sensors[0])
        up = 'Up: ' + str(sensors[1])
        right = 'Right: ' + str(sensors[2])
        down = 'Down: ' + str(sensors[3])
        found = "Found: " + str(sensors[4])
        x_str = "X: " + str(x)
        y_str = "Y: " + str(y)
        cv2.putText(img, left, (10, 420), font, 0.5, (0, 0, 255), 1)
        cv2.putText(img, up, (10, 440), font, 0.5, (0, 0, 255), 1)
        cv2.putText(img, right, (10, 460), font, 0.5, (0, 0, 255), 1)
        cv2.putText(img, down, (10, 480), font, 0.5, (0, 0, 255), 1)
        cv2.putText(img, found, (10, 500), font, 0.5, (0, 0, 255), 1)
        cv2.putText(img, 'Reward: ' + str(r), (100, 420), font, 0.5, (0, 0, 255), 1)
        cv2.putText(img, x_str, (100, 440), font, 0.5, (0, 0, 255), 1)
        cv2.putText(img, y_str, (100, 460), font, 0.5, (0, 0, 255), 1)
        cv2.putText(img, 'Turns: ' + str(turns), (100, 480), font, 0.5, (0, 0, 255), 1)
        cv2.imshow(window_name, img)

    if supervised:
        bot_actions = robot.get_actions_values()
        k = cv2.waitKey(0)
        print('key:', k)
        if k == 113:
            break
        if 80 < k < 85:
            action = k - 81
        else:
            continue
    else:
        turns += 1
        if turns == 1000:
            break
        action, actions = robot.take_action()
        cv2.waitKey(wait_time)

    get_new_position(action)
    r = get_reward()

if render:
    if not supervised:
        cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print(r)
