import os
import cv2
import json, yaml
import pdb
import yaml
from PIL import Image
from glob import glob
from scipy.io import loadmat

class VBBConverter():
    def __init__(self, dataset, config):
        config = config[dataset]
        vbb_dir = config["vbb_dir"]
        img_dir = config["img_dir"]
        ann_dir = config["ann_dir"]
        if not os.path.exists(img_dir):
            print("image path does not exist")
            return
        if not os.path.exists(vbb_dir):
            print("vbb path does not exist")
            return
        os.makedirs(ann_dir, exist_ok=True)
        self._set_basic_info()
        self._set_categories()

        for set_dir in sorted(glob(os.path.join(vbb_dir, "set*"))):
            set_name = set_dir.split("/")[-1]
            self._get_images(img_dir, set_name)
            self._get_annotation(set_dir)
            json_data = self._get_json_format()
            with open(os.path.join(ann_dir, set_name + ".json"), "w") as jsonfile:
                json.dump(json_data, jsonfile, sort_keys=True, indent=4)

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

    def _set_categories(self):
        with open("categories.json") as json_data:
            self.categories = json.load(json_data)["categories"]
        self.cat2id = {"person": 1, "people": 2}

    def _get_images(self, img_dir, set_name):
        img_dir = os.path.join(img_dir, set_name)
        file_names = sorted(os.listdir(img_dir))
        if len(os.listdir(img_dir)) == 0:
            return []
        w, h = self._get_img_size(img_dir, file_names[0])
        self.images =  self._img_list_to_dict(img_dir, file_names, w, h)

    def _get_img_size(self, img_dir, img_name):
        img = Image.open(os.path.join(img_dir, img_name))
        w, h = img.size
        img.close()
        return w, h

    def _img_list_to_dict(self, img_dir, file_names, w, h):
        id_cnt = 1
        res = []
        for f in file_names:
            res.append({
                "date_captured" : "2009",
                "file_name" : f,
                "id" : id_cnt,
                "license" : 1,
                "url" : "",
                "height" : h,
                "width" : w
            })
            id_cnt += 1
        return res

    def _get_annotation(self, set_dir):
        total_frame_cnt = 1
        annotations = []
        for anno_fn in sorted(glob(os.path.join(set_dir, "*.vbb"))):
            vbb = loadmat(anno_fn)
            nFrame = int(vbb['A'][0][0][0][0][0]) # number of frames
            objLists = vbb['A'][0][0][1][0]
            annots = self._get_bboxes(objLists, total_frame_cnt)
            annotations.extend(annots)
            total_frame_cnt += nFrame
        self.annotations = annotations

    def _get_bboxes(self, objLists, total_frame_cnt):
        annotations = []
        for frame_id, obj in enumerate(objLists):
            obj = obj[0]
            for bbox in obj:
                bbox = bbox[1]
                annotations.append({
                        "segmentation": [],
                        "area": 0,
                        "iscrowd": 0,
                        "image_id" : frame_id + total_frame_cnt,
                        "bbox" : bbox.tolist()[0],
                        "category_id" : 1,
                        "id": frame_id + total_frame_cnt
                    })
        return annotations

    def _get_json_format(self):
         return {
                "info": self.info,
                "images" : self.images,
                "licenses" : self.licenses,
                "type" : self.type,
                "annotations" : self.annotations,
                "categories" : self.categories
         }
'''
        for frame_id, obj in enumerate(objLists):
            if len(obj) > 0:
                for id, pos, occl, lock, posv in zip(
                        obj['id'][0], obj['pos'][0], obj['occl'][0],
                        obj['lock'][0], obj['posv'][0]):
                    annotations.append({
                        "segmentation": [],
                        "area": 0,
                        "iscrowd": 0,
                        "image_id" : frame_id + total_frame_cnt,
                        "bbox" : pos.tolist()[0],
                        "category_id" : 1,
                        "id": frame_id + total_frame_cnt
                    })'''

