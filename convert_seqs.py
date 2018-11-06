#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
set 00~06: train set
set 07~10: test set
'''

import os
import glob
import cv2 as cv

def save_img(out_dir_set, set_name, file_name, frame_num ,frame):
    cv.imwrite('{}/{}_{}_{}.jpg'.format(
        out_dir_set, set_name, file_name, str(frame_num).zfill(5)),
        frame)

def convert_seqs(out_dir, config):
    train_dir = os.path.join(out_dir, "train")
    test_dir = os.path.join(out_dir, "test")
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    if not os.path.exists(train_dir):
        os.makedirs(train_dir)
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    img_cnt = 1
    for dname in sorted(glob.glob('data/set*')):
        set_name = dname.split("/")[1]
        train_set = config["TRAIN_SET"]
        test_set = config["TEST_SET"]

        if set_name in ["set"+str(x).zfill(2) for x in train_set]:
            out_dir_set = train_dir
        elif set_name in ["set"+str(x).zfill(2) for x in test_set]:
            out_dir_set = test_dir
        else:
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
