#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
import cv2 as cv
import pdb

def save_img(out_dir_set, dname, fn, i, frame):
    cv.imwrite('{}/{}_{}_{}.jpg'.format(
        out_dir_set, os.path.basename(dname),
        os.path.basename(fn).split('.')[0], i),
        frame)

out_dir = 'data/images'
if not os.path.exists(out_dir):
    os.makedirs(out_dir)
set_cnt = 1
for dname in sorted(glob.glob('data/set*')):
    set_name = dname.split("/")[1]
    out_dir_set = os.path.join(out_dir, set_name)
    if not os.path.exists(out_dir_set):
        os.makedirs(out_dir_set)
    for fn in sorted(glob.glob('{}/*.seq'.format(dname))):
        cap = cv.VideoCapture(fn)
        i = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            save_img(out_dir_set, dname, fn, i, frame)
            i += 1
        print(fn)
