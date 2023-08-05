# -*- coding: utf-8 -*-
"""Translation utils to go from bounding boxes to points an backwards.
Data Types:
- bbox: (xmin:int, ymin:int, xmax:int, ymax:int)
- wh_bbox: {x:int, y:int, width:int, height:int}
"""



def _bbox2points(xmin,ymin,xmax,ymax):
    """Get the corners of a bbox. Points than define it.
    """
    return([
        (xmin, ymin),
        (xmax, ymin),
        (xmin, ymax),
        (xmax, ymax)
    ])


def _points2bbox(points):
    """Calculate the smallest bbox that contains the points.
    NOTE: When performing transformations, the bboxes have to be recalculated.

    Parameters
    ----------
    points: [(x int, y int)]
        list of x,y points.

    Return
    ------
    retval: (x int,y int,x int,y int)
        bbox
    """
    xs, ys = zip(*points)
    return(min(xs), min(ys), max(xs), max(ys))


def bboxes2points(bboxes):
    """Convert bboxes to a list of points.

    Parameters
    ----------
    bboxes: [(int, int, int, int)]
        List of bboxes.

    Return
    ------
    retval: [(int, int)]
        List of points (4*bboxes)
    """
    bboxes_points = [_bbox2points(*bbox) for bbox in bboxes]
    # Here I have a list of bboxes corners, flatten all.
    return [point for bbox_points in bboxes_points for point in bbox_points]


def points2bboxes(points, ppbbox=4):
    """Transform a list of points into bboxes.

    Parameters
    ----------
    points: [(x int,y int)]
        List of (x,y) points
    ppbbox: int
        Points per bounding box (usually 4).

    Return
    ------
    retval: [(int*ppbbox)]
        List of bboxes containing the points.
    """
    bboxes_points = [
        points[x:x+ppbbox]
        for x in range(0,len(points), ppbbox)
    ]
    return [_points2bbox(ps) for ps in bboxes_points]


def wh_bboxes2points(wh_bboxes):
    """Transform width-height-bboxes to points.

    Parameters
    ----------
    wh_bboxes: [wh_bbox]
        List of width-heigh bboxes.

    Return
    ------
    retval: [(int, int)]
        List of points (4*bboxes)
    """
    return bboxes2points([
        (
            b['x'],
            b['y'],
            b['x']+b['width'],
            b['y']+b['height']
        )
        for b in wh_bboxes
    ])


def points2wh_bboxes(points, ppbbox=4):
    """Convert a list of points to wh_bboxes.

    Parameters
    ----------
    points: [(x int,y int)]
        List of (x,y) points
    ppbbox: int
        Points per bounding box (usually 4).

    Return
    ------
    retval: [wh_bbox]
        List of wh_bboxes containing the points.
    """
    return [
        {
            'x': xmin,
            'y': ymin,
            'width': xmax-xmin,
            'height': ymax-ymin
        }
        for xmin,ymin,xmax,ymax in points2bboxes(points, ppbbox)
    ]
