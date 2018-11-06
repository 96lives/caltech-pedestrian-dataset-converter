Caltech Pedestrian Dataset Converter
============================

# Requirements

- OpenCV 3.0+ (with Python binding)
- Python 2.7+, 3.4+, 3.5+
- NumPy 1.10+
- SciPy 0.16+

# Caltech Pedestrian Dataset

```
$ sh download_and_convert.sh
```

Each `.seq` movie is separated into `.jpg` images. Each image's filename is consisted of `{set**}_{V***}_{frame_num}.jpg`. According to [the official site](http://www.vision.caltech.edu/Image_Datasets/CaltechPedestrians/), `set06`~`set10` are for test dataset, while the rest are for training dataset. The `.seq.` is donwnloaded at `./data` directory and the converted images are in `./data/images` directory, divided into `test` and `train` folders. You can split your own `test` and `train` by modifying the `./config.yaml`. The coco-format converted annotation is stored at `./data/annotations`.

(Number of objects: 346621)

# Draw Bounding Boxes

```
$ python tests/test_plot_annotations.py
```
