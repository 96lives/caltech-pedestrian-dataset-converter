
from __future__ import division
from __future__ import print_function

import os
import cv2
import json, yaml
import numpy as np
import glob
from PIL import Image
from collections import OrderedDict
from pycocotools import mask as cocomask
from pycocotools import coco as cocoapi
from scipy.io import loadmat

SET_INDEX = [
    "00", "01", "02", "03", "04", "05"
    "06", "07", "08", "09", "10"
]


class Pedestrian():
    """
        Caltech Pedestrian data class to convert annotations to COCO Json format
    """
    def __init__(self, datapath="./data/annotations/", imageres="480p"):
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
        '''
        self.seqs = yaml.load(open(os.path.join(self.datapath, "Annotations", "db_info.yml"),
                                   "r")
                             )["sequences"]
        self.categories = [{"id": seqId+1, "name": seq["name"], "supercategory": seq["name"]}
                              for seqId, seq in enumerate(self.seqs)]
        [{'id': 1, 'name': 'bear', 'supercategory': 'bear'}, {...}, ...   ]
        self.cat2id = {cat["name"]: catId+1 for catId, cat in enumerate(self.categories)}
        {"bear": 1, "blackswan": 2, ...}
        '''
        for s in SET_INDEX:
            set_dir = os.path.join(self.datapath, "set"+s)
            imlist = os.listdir(set_dir)
            images, annotations = self.get_image_annotation_pairs(set_dir)
            json_data = {"info" : self.info,
                         "images" : images,
                         "licenses" : self.licenses,
                         "type" : self.type,
                         "annotations" : annotations,
                         "categories" : self.categories}

            with open(os.path.join(set_dir, "set{}.json".format(s)), "w") as jsonfile:
                json.dump(json_data, jsonfile, sort_keys=True, indent=4)


    def get_image_annotation_pairs(self, set_dir):
        images = []
        annotations = []

        for anno_fn in sorted(glob.glob('{}/*.vbb'.format(set_dir))):
            images.append({"date_captured" : "2016",
                           "file_name" : impath[1:], # remove "/"
                           "id" : imId+1,
                           "license" : 1,
                           "url" : "",
                           "height" : mask.shape[0],
                           "width" : mask.shape[1]})
            vbb = loadmat(anno_fn)
            nFrame = int(vbb['A'][0][0][0][0][0]) # number of frames
            objLists = vbb['A'][0][0][1][0]
            '''
            objLists[fn][0]: contains data of certain objects in frame 'fn'
            objLists[fn][0][0]: contains data of one object in frame 'fn'
            objLists[fn][0][0][1][0]: array of [x, y, w, h]
            '''


        pass


    def __get_image_annotation_pairs__(self, image_set):
        images = []
        annotations = []
        for imId, paths in enumerate(image_set):
            impath, annotpath = paths[0], paths[1]
            print (impath)
            name = impath.split("/")[3]
            img = np.array(Image.open(os.path.join(self.datapath + impath)).convert('RGB'))
            mask = np.array(Image.open(os.path.join(self.datapath + annotpath)).convert('L'))
            if np.all(mask == 0):
                continue

            segmentation, bbox, area = self.__get_annotation__(mask, img)
            images.append({"date_captured" : "2016",
                           "file_name" : impath[1:], # remove "/"
                           "id" : imId+1,
                           "license" : 1,
                           "url" : "",
                           "height" : mask.shape[0],
                           "width" : mask.shape[1]})
            annotations.append({"segmentation" : segmentation,
                                "area" : np.float(area),
                                "iscrowd" : 0,
                                "image_id" : imId+1,
                                "bbox" : bbox,
                                "category_id" : self.cat2id[name],
                                "id": imId+1})
        return images, annotations

if __name__ == "__main__":
    datapath = "./data/annotations"
    Pedestrian(datapath)

    # test
    from PIL import Image
    from pycocotools import coco; c = coco.COCO(datapath+'/Annotations/480p_trainval.json')
    Image.fromarray(c.annToMask(c.loadAnns([255])[0])*255).show()
