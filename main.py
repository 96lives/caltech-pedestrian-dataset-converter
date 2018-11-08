import yaml
import pdb
import cv2
import json
import os
from convert_seqs import convert_seqs
from convert_annotations import VBBConverter
import argparse

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

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", \
                        choices=["caltech_pedestrian", "kaist_pedestrian"],
                        default="caltech_pedestrian")
    parser.add_argument("--config", default="./config.yaml")
    return parser.parse_args()

if __name__ == "__main__":

    args = get_args()
    config = yaml.load(open(args.config))
    print("Converting videos...")
    #convert_seqs(args.dataset, config)
    print("Finished converting videos!")
    print("Converting annotations...")
    VBBConverter(args.dataset, config)
    print("Finished converting annotations!")
    '''
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
    '''
