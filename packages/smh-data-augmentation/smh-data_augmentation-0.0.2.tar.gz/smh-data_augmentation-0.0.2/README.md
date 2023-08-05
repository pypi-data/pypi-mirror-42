# Data Augmentator

## Description
This tool allows to generate modified data while keeping the statistical invariant, also known as data augmentation. It is useful to train machine learning models that need a huge amount of data and reduce the variance in predictions, see the [Bias–variance tradeoff](https://en.wikipedia.org/wiki/Bias%E2%80%93variance_tradeoff).  


## Features
### Images
  * Calculate new point positions.
  * Recalculate bounding boxes.
  * Command Line Interface
```bash
python3 -m data_augmentation.img -h
```


### TODO
* PIP package
* Other domains than images.


## Alternatives
This library is intented for internal uses of the lab so there could be others that fit better to your needs, see:
* [imgaug](https://github.com/aleju/imgaug)
