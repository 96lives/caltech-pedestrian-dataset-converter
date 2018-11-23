import os
import cv2
import json, yaml
import pdb
import yaml
from PIL import Image
from glob import glob
from scipy.io import loadmat

TRAIN_SET = ["set00", "set01", "set02", "set03", "set04", "set05"]
TEST_SET = ["set06", "set07", "set08", "set09", "set10", "set11"]

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
        self._get_images(img_dir)

        for set_dir in sorted(glob(os.path.join(vbb_dir, "set*"))):
            self._get_annotation(set_dir)
        with open(os.path.join(ann_dir, set_name + ".json"), "w") as jsonfile:
            json.dump(self._get_json_format(), jsonfile, sort_keys=True, indent=4)

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
        self.name2id = {}
        self.images = []
        self.annotations = []

    def _set_categories(self):
        with open("kaist_categories.json") as json_data:
            self.categories = json.load(json_data)["categories"]
            self.cat2id = {"person": 1, "person?": 2, "people": 3, "cyclist": 4}

    def _get_images(self, img_dir):
        file_names = sorted(os.listdir(img_dir))
        if len(os.listdir(img_dir)) == 0:
            return []
        w, h = self._get_img_size(img_dir, file_names[0])
        self.images.extend(self._img_list_to_dict(img_dir, file_names, w, h))

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
            self.name2id[f]=id_cnt
            id_cnt += 1
        return res

    def _get_annotation(self, set_dir):
        total_frame_cnt = 1
        set_name = set_dir.split('/')[-1]
        for file_name in sorted(glob(os.path.join(set_dir, "*.vbb"))):
            vbb_name = file_name.split('/')[-1].split('.')[0]
            vbb = loadmat(file_name)
            nFrame = int(vbb['A'][0][0][0][0][0]) # number of frames
            obj_lists = vbb['A'][0][0][1][0]
            obj_lbl = [str(v[0]) for v in vbb['A'][0][0][4][0]]
            for frame_id, objs in enumerate(obj_lists):
                bboxes = []
                for obj in objs[0]:
                    bbox = [obj_lbl[obj[0][0][0]-1]] # add class name to bbox
                    bbox.append(obj[1][0]) # add x, y, w, h to bbox
                    bboxes.append(bbox)
                    vbb_name = file_name.split('/')[-1].split('.')[0]
                    img_name = set_name+'_'+vbb_name + '_I' + str(frame_id).zfill(5)+'.jpg'
                    import pdb
                    pdb.set_trace()
                    if self.name2id.get(img_name) is None:
                        continue
                    self.annotations.append({
                            "segmentation": [],
                            "area": 0,
                            "iscrowd": 0,
                            "image_id" : self.name2id[img_name],
                            "bbox" : obj[1][0].tolist(),
                            "category_id" : self.cat2id[obj_lbl[obj[0][0][0]-1]],
                            "id": self.name2id[img_name]
                        })


    def _get_bboxes(self, set_name, vbb_name, objLists, obj_lbl, total_frame_cnt):
        annotations = []
        cnt = 0
        for frame_id, obj in enumerate(objLists):
            obj = obj[0]
            for bbox in obj:
                bbox = bbox[1]
                name = set_name+'_'+vbb_name+'_I'+str(cnt).zfill(5)+'.jpg'
                if self.name2id.get(name) is None:
                    continue
                import pdb
                pdb.set_trace()
                annotations.append({
                        "segmentation": [],
                        "area": 0,
                        "iscrowd": 0,
                        "image_id" : self.name2id[name],
                        "bbox" : bbox.tolist()[0],
                        "category_id" : self.cat2id[obj_lbl[bbox[0][0][0]-1]],
                        "id": self.name2id[name]
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

