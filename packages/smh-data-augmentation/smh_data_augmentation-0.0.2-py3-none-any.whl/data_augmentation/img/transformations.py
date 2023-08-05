# -*- coding: utf-8 -*-
"""Data augmentation functions.
"""

import numpy as np
import skimage
from skimage import transform
import skimage.filters
from skimage.filters import threshold_local
from skimage.util import random_noise
from skimage.restoration import denoise_bilateral



#
### Keep the points
#

def blur(img, points):
    """Apply bilateral filter
    """
    yield(
        np.clip(
            skimage.filters.gaussian(img.copy(),sigma=3.0, multichannel=True),
            -1,1
        ),
        points
    )

def noise(img, points):
    """Add gaussian noise
    """
    yield(
        random_noise(img.copy(), mode='gaussian', var=0.001),
        points
    )

def saltnpepper(img, points):
    """Add gaussian noise
    """
    yield(
        random_noise(img.copy(), mode='s&p', amount=0.05),
        points
    )

def threshold(img, points):
    """Add gaussian noise
    """
    yield(
        threshold_local(img.copy(), block_size=5, method='gaussian', offset=0, mode='reflect', param=None),
        points
    )


#
### Modify the points
#

def mirror(img, points=[]):
    """Vertical symmetry
    """
    _,width,*_ = img.shape
    if points!=[]:
        mirror_points = [
            (width-x, y)
            for x,y in points
        ]
    else:
        mirror_points = points
    yield (
        np.fliplr(img.copy()),
        mirror_points
    )


def rotation(img, points, angles=[-10,-5,5,10]):
    """Rotate an image around its center
    """
    h,w,*_ = img.shape
    center = (w//2, h//2)
    if points!=[]:
        points_origin = np.array(points)-np.array(center)
        points_origin[:,1] *= -1
    for angle in angles:
        # Rotate image
        rot_img = transform.rotate(img, angle, center=center)
        # Rotate points
        if points!=[]:
            rads = np.deg2rad(angle)
            sin_rads = np.sin(rads)
            cos_rads = np.cos(rads)
            rot_mat = np.array([[cos_rads, -sin_rads],[sin_rads, cos_rads]])  #Rotation matrix
            rot_points_origin = rot_mat.dot(points_origin.T).T
            rot_points_origin[:,1] *= -1
            rot_points = rot_points_origin + np.array(center)
        else:
            rot_points = points
        yield(rot_img, rot_points)


def resize(img, points, scales=[(1.5,1),(1,1.5)]):
    """Resize the image, change the aspect ratio
    """
    h,w,*_ = img.shape
    center = (w//2, h//2)
    if points!=[]:
        points_origin = np.array(points)-np.array(center)
        points_origin[:,1] *= -1
    for x_scale, y_scale in scales:
        scaled_img = skimage.transform.resize(img, output_shape=(int(h*y_scale), int(w*x_scale)))
        if points!=[]:
            s_h,s_w,*_ = scaled_img.shape
            scaled_center_img = np.array((s_w//2, s_h//2))
            scaled_points_origin = np.array(points_origin)* np.array([x_scale, y_scale])
            scaled_points_origin[:,1] *= -1
            scaled_points = scaled_points_origin + scaled_center_img
        else:
            scaled_points = points
        yield (scaled_img, scaled_points)
