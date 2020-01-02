import os
import cv2 as cv
import numpy as np

import time
start = time.time()

path = "./images"
img_list = os.listdir(path)

for img_file in img_list:
    img = cv.imread("images/"+img_file)
    original_img = cv.imread("images/"+img_file)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    ret, thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)

    # noise removal
    kernel = np.ones((3, 3), np.uint8)
    opening = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel, iterations=1)

    # sure background area
    sure_bg = cv.dilate(opening, kernel, iterations=6)

    # Finding sure foreground area
    dist_transform = cv.distanceTransform(opening, cv.DIST_L2, 5)
    ret, sure_fg = cv.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)

    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv.subtract(sure_bg, sure_fg)

    # Marker labelling
    ret, markers = cv.connectedComponents(sure_bg)

    # Add one to all labels so that sure background is not 0, but 1
    markers = markers + 1
    # markers[unknown == 255] = 0

    markers = cv.watershed(img, markers)

    # img[markers == -1] = [255, 0, 0]
    img[markers != 1] = [100, 255, 255]

    # cv.imshow("unknown", unknown)
    # cv.imshow("sure_fg", sure_fg)
    # cv.imshow("sure_bg", sure_bg)
    # cv.imshow("result", img)
    # cv.waitKey(0)

    img = cv.addWeighted(img, 0.3, original_img, 0.6, 0)
    cv.imwrite("result/"+img_file,img)

print("time :", time.time() - start)