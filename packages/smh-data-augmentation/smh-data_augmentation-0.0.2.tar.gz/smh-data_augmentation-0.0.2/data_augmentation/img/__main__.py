# -*- coding: utf-8 -*-
"""CLI interface
Example of how to use the library for img augmentation.
"""


import argparse
from collections import defaultdict
import csv
import os

import skimage

from . import transformations
from . import utils
from .generate_samples import generate_samples
from .utils import wh_bboxes2points, points2wh_bboxes


IMG_EXTENSIONS = (  # File extensions to consider as images
    '.jpg',
    'jpeg',
    '.png'
)

IMG_TRANSFORMATIONS = [
    lambda img, points: transformations.resize(img, points, scales=[ (1.5,1), (1,1.5) ]),  # x3
    lambda img,points: transformations.rotation(img, points, angles=[-7.5, 7.5,]), # x3
    transformations.noise,  # x2
    transformations.mirror, # x2
]

def check_arguments():
    """Create a parser and check command arguments.

    Return
    ------
    retval: {in_img_path, in_csv, out_img_path, out_csv}
        Dictionary with command arguments. If present, directories or
    """
    # Command arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--in_img",
        type=str,
        help="Directory containing the input images.",
        default='.',
        action="store"
    )
    parser.add_argument(
        "--in_csv",
        type=str,
        help="(Optional) CSV file with the annotations.",
        # default='annotations.csv',  # NOT DEFAULT, flag behaviour
        action="store"
    )
    parser.add_argument(
        "--out_img",
        type=str,
        help="Directory to store the new images.",
        default='augmented',
        action="store"
    )
    parser.add_argument(
        "--out_csv",
        type=str,
        help="(Optional) CSV file with the new annotations.",
        default='augmented/annotations.csv',
        action="store"
    )
    args = parser.parse_args()
    # CHECKS
    # IN dataset folder musts exist
    if not os.path.isdir(args.in_img):
        print("ERROR: cannot find directory {}".format(args.in_img))
        exit(0)
    args.in_img = os.path.abspath(args.in_img)
    if args.in_csv:
        # IN CSV file must exist
        args.in_csv = os.path.abspath(args.in_csv)
        if not os.path.exists(args.in_csv):
            print("ERROR: cannot find file {}".format(args.in_csv))
            exit(0)
    # OUT dataset folder must not exist
    if os.path.isdir(args.out_img):
        print("ERROR: directory exists {}".format(args.out_img))
        exit(0)
    args.out_img = os.path.abspath(args.out_img)
    if args.in_csv and args.out_csv:
        # OUT csv must not exist
        args.out_csv = os.path.abspath(args.out_csv)
        if os.path.exists(args.out_csv):
            print("ERROR: file exists {}".format(args.in_csv))
            exit(0)
    return args


def get_img_paths(in_img):
    """
    Parameters
    ----------
    in_img: str
        Path of the original images

    Return
    ------
    retval: [str]
        Absolute paths of original images
    """
    img_paths = []
    for (path, subdirs, files) in os.walk(args.in_img):
            if files:
                for f in files:
                    if f.lower().endswith( IMG_EXTENSIONS ):
                        img_paths.append(os.path.join(path, f))
    return img_paths


def get_bboxes(img_paths, in_csv):
    """
    Parameters
    ----------
    img_paths: [str]
        Images absolute paths.
    in_csv: str
        CSV path with the bounding boxes.

    Retval
    ------
    retval: { img_path:[bbox]}
        Absolute path of the image with its associated bounding-boxes.
        img_paths comes from the directory plus the CSV.
    """
    # Create index
    retval = defaultdict(
        lambda:[],
        {img_path:[] for img_path in img_paths}
    )
    if in_csv:
        try:
            csv_path = os.path.dirname(os.path.abspath(in_csv))
            with open(in_csv) as fd:
                csv_annotations = csv.DictReader(fd)
                for row in csv_annotations:
                    if os.path.isabs(row['path']):  # path is absolute
                        img_path = row['path']
                    else:  # path is relative to CSV
                        img_path = os.path.join(
                            csv_path,
                            row['path']
                        )
                    img_path = os.path.normpath(img_path)  # Cannonical form
                    retval[img_path].append({  # Bbox in the image
                        'x': round(float(row['x'])),
                        'y': round(float(row['y'])),
                        'width': round(float(row['width'])),
                        'height': round(float(row['height']))
                    })
        except Exception as e:
            print("ERROR: {}".format(e))
    return retval

if __name__=='__main__':
    args = check_arguments()
    # PRE-CONDITIONS
    try:  # Output directory exists
        print("INFO: creating directory for augmented images {}".format(args.out_img))
        os.mkdir(args.out_img)
    except:
        print("ERROR: could not create directory {}".format(args.out_img))
    if args.in_csv:
        try:  # Output CSV exists
            print("INFO: creating file for augmented annotations {}".format(args.out_csv))
            open(args.out_csv,'w').close()
        except:
            print("ERROR: could not create file {}".format(args.out_csv))
    img_paths = get_img_paths(args.in_img)  # Load img filepaths from dir
    img_bboxes = get_bboxes(img_paths, args.in_csv)  # {img_path: [bbox]}
    # Perform actual data augmentation
    out_bboxes = []  # transformed bboxes
    for img_path, bboxes in img_bboxes.items():
        print("INFO: Augmenting image: {}".format(img_path))
        img_path_name, img_path_extension = os.path.splitext(
            os.path.basename(img_path)
        )
        # TODO: this function can be parallelized
        for aug_id,(aug_img, aug_points) in enumerate(
            generate_samples(
                skimage.exposure.equalize_hist(
                    skimage.io.imread(img_path)
                ),
                IMG_TRANSFORMATIONS,
                utils.wh_bboxes2points(bboxes)
        )):
            aug_img_path = os.path.join(
                args.out_img,
                "{}_{:06}{}".format(img_path_name, aug_id, img_path_extension)
            )
            print("\tINFO: Saving augmented image {}".format(aug_img_path))
            skimage.io.imsave(aug_img_path, aug_img)
            for aug_bbox in utils.points2wh_bboxes(aug_points):
                aug_bbox['path'] = os.path.basename(aug_img_path)
                out_bboxes.append(aug_bbox)
    if args.in_csv:  # Save augmented bboxes CSV
        print("INFO: writing bboxes CSV {}".format(args.out_csv))
        with open(args.out_csv, 'w+') as fd:
            writer = csv.DictWriter(fd, fieldnames=out_bboxes[0].keys())
            writer.writeheader()
            for out_bbox in out_bboxes:
                writer.writerow(out_bbox)
