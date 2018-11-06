#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
set 00~06: train set
set 07~10: test set
'''

import os
import glob
import cv2 as cv
import pdb

TRAIN_SET = [0 , 1]
#TRAIN_SET = [0, 1, 2, 3, 4, 5 ,6]
#TEST_SET = [7, 8 ,9, 10]
#TRAIN_SET = ["00", "01", "02", "03", "04", "05", "06"]
#TEST_SET = ["07", "08", "09", "10"]

def save_img(out_dir_set, set_name, file_name, frame_num ,frame):
    cv.imwrite('{}/{}_{}_{}.jpg'.format(
        out_dir_set, set_name, file_name, str(frame_num).zfill(5)),
        frame)

out_dir = 'data/images'
if not os.path.exists(out_dir):
    os.makedirs(out_dir)
img_cnt = 1
for dname in sorted(glob.glob('data/set*')):
    set_name = dname.split("/")[1]
    if set_name in ["set"+str(x).zfill(2) for x in TRAIN_SET]:
        out_dir_set = os.path.join(out_dir, "train")
    else:
        out_dir_set = os.path.join(out_dir, "test")
        continue

    if not os.path.exists(out_dir_set):
        os.makedirs(out_dir_set)
    for fn in sorted(glob.glob('{}/*.seq'.format(dname))):
        _, set_name, file_name = fn.split("/")
        file_name = file_name.split(".")[0]
        cap = cv.VideoCapture(fn)
        frame_num = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            save_img(out_dir_set, set_name, file_name, frame_num, frame)
            frame_num += 1
        print(fn)
