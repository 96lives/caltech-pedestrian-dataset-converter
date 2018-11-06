
from __future__ import division
from __future__ import print_function

import os
import cv2
import json, yaml
import pdb
import glob
from PIL import Image
from collections import OrderedDict
from pycocotools import mask as cocomask
from pycocotools import coco as cocoapi
from scipy.io import loadmat
from collections import defaultdict

TRAIN_SET= [0, 1, 2, 3, 4, 5, 6]
TEST_SET = [7, 8, 9, 10]

class Pedestrian():
    def __init__(self, datapath):
        self.info = {"year" : 2009,
                     "version" : "1.0",
                     "description" : "Dataset for pedestrain",
                     "contributor" : "P. Dollár, C. Wojek, B. Schiele and P. Perona",
                     "url" : "http://www.vision.caltech.edu/Image_Datasets/CaltechPedestrians/",
                     "date_created" : "2009"
                    }
        self.licenses = [{"id": 1,
                          "name": "Attribution-NonCommercial",
                          "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/"
                         }]
        self.type = "instances"
        self.datapath = datapath
        self.categories = [{"id": 1, "name": "person", "supercategory": "person"}]
        self.cat2id = {"person": 1}

        for s in ["train"]: # Later add train
            images = self._get_images(os.path.join(self.datapath, "images", s))
            annotations = self._get_annotation(os.path.join(self.datapath, "annotations"), s)
            json_data = {"info" : self.info,
                         "images" : images,
                         "licenses" : self.licenses,
                         "type" : self.type,
                         "annotations" : annotations,
                         "categories" : self.categories}
            with open(os.path.join(self.datapath, "annotations", s+".json"), "w") as jsonfile:
                json.dump(json_data, jsonfile, sort_keys=True, indent=4)


    def _get_images(self, img_dir):
        file_names = sorted(os.listdir(img_dir))
        w, h = self._get_img_size(img_dir, file_names[0])
        return self._img_list_to_dict(img_dir, file_names, w, h)

    def _get_img_size(self, img_dir, img_name):
        img = Image.open(os.path.join(img_dir, img_name))
        w, h = img.size
        img.close()
        return w, h

    def _img_list_to_dict(self, img_dir, file_names, w, h):
        id_cnt = 1
        res = []
        for f in file_names:
            res.append({"date_captured" : "2009",
                        "file_name" : f,
                        "id" : id_cnt,
                        "license" : 1,
                        "url" : "",
                        "height" : h,
                        "width" : w})
            id_cnt += 1
        return res

    def _get_annotation(self, anno_dir ,mode):
        dirs = None
        if mode == "test":
            dirs = TEST_SET
        else:
            dirs = TRAIN_SET
        res = []
        total_frame_cnt = 1
        annotations = []
        for set_num in dirs:
            set_dir = os.path.join(anno_dir, "set"+str(set_num).zfill(2))
            for anno_fn in sorted(glob.glob('{}/*.vbb'.format(set_dir))):
                vbb = loadmat(anno_fn)
                nFrame = int(vbb['A'][0][0][0][0][0]) # number of frames
                objLists = vbb['A'][0][0][1][0]
                annots = self.get_bboxes(objLists, total_frame_cnt)
                annotations.extend(annots)
                total_frame_cnt += nFrame
        return annotations

    def get_bboxes(self, objLists, total_frame_cnt):
        annotations = []
        for frame_id, obj in enumerate(objLists):
            if len(obj) > 0:
                for id, pos, occl, lock, posv in zip(
                        obj['id'][0], obj['pos'][0], obj['occl'][0],
                        obj['lock'][0], obj['posv'][0]):
                    annotations.append({"segmentation": [],
                                        "area": 0,
                                        "iscrowd": 0,
                                        "image_id" : frame_id + total_frame_cnt,
                                        "bbox" : pos.tolist()[0],
                                        "category_id" : 1,
                                        "id": frame_id + total_frame_cnt})
        return annotations


# test
def get_bboxes(data, img_name):
    imgs = data["images"]
    img_id = 0
    for img_dic in imgs:
        if img_dic["file_name"] == img_name:
            img_id = img_dic["id"]
            break
    annos = data["annotations"]
    bboxes = [x["bbox"] for x in annos if x["id"]==img_id]
    return bboxes

if __name__ == "__main__":

    datapath = "./data/"
    Pedestrian(datapath)
    json_dir = "./data/annotations/train.json"
    img_dir = "./data/images/train/set01_V004_00000.jpg"
    img_name = img_dir.split("/")[4]
    img = cv2.imread(img_dir)
    with open(json_dir) as f:
        data = json.load(f)
    bboxes = get_bboxes(data, img_name)
    for bbox in bboxes:
        x = int(bbox[0])
        y = int(bbox[1])
        w = int(bbox[2])
        h = int(bbox[3])
        cv2.rectangle(img,(x,y),(x+w,y+h), (255,0,0), 2)
    cv2.imshow("", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

