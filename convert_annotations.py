import os
import cv2
import json, yaml
import pdb
import yaml
import random
from shutil import copyfile
from PIL import Image
from glob import glob
from scipy.io import loadmat

class VBBConverter():
    def __init__(self, dataset, config):
        config = config[dataset]
        vbb_dir = config["vbb_dir"]
        self.img_dir = config["img_dir"]
        ann_dir = config["ann_dir"]
        if not os.path.exists(self.img_dir):
            print("image path does not exist")
            return
        if not os.path.exists(vbb_dir):
            print("vbb path does not exist")
            return
        os.makedirs(ann_dir, exist_ok=True)
        self._set_basic_info()
        self._set_categories()
        self.img_save_path = os.path.join(self.img_dir, "test_with_labels")
        os.makedirs(self.img_save_path, exist_ok=True)
        for set_dir in sorted(glob(os.path.join(vbb_dir, "set*"))):
            set_name = set_dir.split("/")[-1]
            self._get_annotation(set_dir) # sets self.annotations and self.images
            print(set_dir)
        with open(os.path.join(ann_dir,"test.json"), "w") as jsonfile:
            json.dump(self._get_json_format(), jsonfile, sort_keys=True, indent=4)
        print(len(self.images))
        print(len(self.annotations))

    def _set_basic_info(self):
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
        self.annotations = []
        self.images = []
        self.img_id_cnt = 1
        self.ann_id_cnt = 1
        self.w = 640
        self.h = 512

    def _set_categories(self):
        with open("kaist_categories.json") as json_data:
            self.categories = json.load(json_data)["categories"]
            self.cat2id = {"person": 1, "person?": 2, "people": 3, "cyclist": 4}

    def _get_annotation(self, set_dir):
        set_name = set_dir.split('/')[-1]
        for anno_fn in sorted(glob(os.path.join(set_dir, "*.vbb"))):
            vbb = loadmat(anno_fn)
            nFrame = int(vbb['A'][0][0][0][0][0]) # number of frames
            obj_lists = vbb['A'][0][0][1][0]
            obj_lbl = [str(v[0]) for v in vbb['A'][0][0][4][0]]
            for frame_id, objs in enumerate(obj_lists):
                ran_num = random.random()
                if ran_num >= 0.02:
                    continue
                labels_exist = False
                bboxes = []
                for obj in objs[0]:
                    category = obj_lbl[obj[0][0][0]-1] # add class name to bbox
                    bbox = obj[1][0] # add x, y, w, h to bbox
                    self.annotations.append({
                        "segmentation": [],
                        "area": 0,
                        "iscrowd": 0,
                        "image_id" : self.img_id_cnt,
                        "bbox" : bbox.tolist(),
                        "category_id" : self.cat2id[category],
                        "id": self.ann_id_cnt
                    })
                    labels_exist = True
                    self.ann_id_cnt += 1
                if labels_exist:
                    vbb_name = anno_fn.split('/')[-1].split('.')[0]
                    old_file_name = vbb_name + '_I' + str(frame_id).zfill(5)+'.jpg'
                    new_file_name = set_name +'_' + old_file_name
                    self.images.append({
                                "date_captured" : "2009",
                                "file_name" : new_file_name,
                                "id" : self.img_id_cnt,
                                "license" : 1,
                                "url" : "",
                                "height" : self.h,
                                "width" : self.w
                            })
                    img_path = os.path.join(self.img_dir, set_name, old_file_name)
                    out_path = os.path.join(self.img_save_path, new_file_name)
                    copyfile(img_path, out_path)
                    self.img_id_cnt += 1


    def _get_json_format(self):
         return {
                "info": self.info,
                "images" : self.images,
                "licenses" : self.licenses,
                "type" : self.type,
                "annotations" : self.annotations,
                "categories" : self.categories
         }
