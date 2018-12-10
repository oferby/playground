import cv2
import numpy as np

img = np.zeros((700, 400, 3), np.uint8)
cv2.rectangle(img, (0, 0), (397, 400), (0, 255, 0), 3)
x = 360
y = 150


def type_1():
    goal_loc = [(370, 30), (380, 40)]
    cv2.rectangle(img, goal_loc[0], goal_loc[1], (0, 0, 255), -1)
    cv2.line(img, (0, 200), (200, 200), (0, 255, 0), 3)
    cv2.line(img, (280, 0), (280, 280), (0, 255, 0), 3)
    return img, goal_loc


def type_2():
    goal_loc = [(300, 300), (310, 310)]
    cv2.rectangle(img, goal_loc[0], goal_loc[1], (0, 0, 255), -1)
    return img, goal_loc


worlds_dict = {
    1: type_1,
    2: type_2
}


def get_world(type):
    func = worlds_dict[type]
    return func()
