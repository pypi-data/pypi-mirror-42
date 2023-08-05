# -*- coding: utf-8 -*-
"""Perform data augmentation on images
"""


def generate_samples(img, transformations=[], points=[]):
    """Iterate over transformations and return the transformed image.

    Parameters
    ----------
    img:
        Opened image with skimage.io.imread()
    transformations: [function(img, points)]
        Function to augment the image.
    points: [(x int, y int)]
        Points to calculate the transformation.

    Returns
    -------
    img: generator of (transformed image, transformed points [(int, int)]).
    """
    if transformations==[]:  # Base case
        yield(img, points)
    else:  # Apply first transformation
        t_apply, *t_list = transformations
        # Branch with original sample
        yield from generate_samples(img, t_list, points)
        # Branch with transformed sample
        for (new_img, new_points) in t_apply(img, points):
            yield from generate_samples(new_img, t_list, new_points)
