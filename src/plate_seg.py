import cv2
import numpy as np
import copy
import matplotlib.pyplot as plt
from typing import Callable, List


def binarize(frame):
    a = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(a, 254, 255, cv2.THRESH_BINARY)
    return cv2.bitwise_not(thresh)


def reject_non_numbers(frame):
    contours, hierarchy = cv2.findContours(
        frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    b = np.zeros((*frame.shape, 1), np.uint8)

    for contour in contours:
        ar = cv2.contourArea(contour)
        pr = cv2.arcLength(contour, True)

        if 5000.0 < ar < 20000.0 and 350 < pr < 700:
            cv2.fillPoly(b, pts=[contour], color=1)

    return cv2.bitwise_and(frame, b)


def cut(frame):
    h, w = frame.shape

    to_remove = []
    removed = False
    for i in range(w):
        for j in range(h):
            if frame[j][i] != 255:
                if removed:
                    to_remove.pop()
                    removed = False
        else:
            removed = True
            to_remove.append(i)

    if removed:
        to_remove.pop()

    output = np.delete(frame, to_remove, 1)

    h, w = output.shape
    to_remove = []

    for i in range(h):
        for j in range(w):
            if output[i][j] != 255:
                break
        else:
            to_remove.append(i)

    return np.delete(output, to_remove, 0)


def split_numbers(frame):
    h, w = frame.shape

    print(frame)
    lines = []
    for i in range(w):
        for j in range(h):
            if frame[j][i] != 255:
                break
        else:
            lines.append(i)

    frames = []
    for i in range(len(lines) - 1):
        frames.append(frame[:, lines[i]:lines[i + 1]])

    return frames


def apply_pipe(pipe, input_image):
    output_image = input_image
    for f in pipe:
        output_image = f(output_image)
    return output_image


pipe = [
    binarize,
    reject_non_numbers,
    cv2.bitwise_not,
    cut
]

plate = cv2.imread('./res/plate.png')
p = apply_pipe(pipe, plate)


plt.figure()
plt.imshow(p, cmap='gray')

a = split_numbers(p)


for frame in a:
    print(frame)
    plt.figure()
    plt.imshow(frame, cmap='gray')

plt.show()
