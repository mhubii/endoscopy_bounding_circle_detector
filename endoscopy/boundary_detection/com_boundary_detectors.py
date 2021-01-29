import cv2
import numpy as np
from typing import Tuple


def boundaryRectangle(img: np.array, th: int=10) -> Tuple[np.array, tuple]:
    """Finds the rectangle that circumferences an endoscopic image.

    Args:
        img (np.array): Grayscale image of shape HxW
        th (int): Whiten threshold, each pixel where value > th is whitened

    Return:
        rectangle (Tuple[np.array, tuple]): Top left corner and shape of found rectangle
    """
    img = np.where(img < th, 0, 255).astype(np.uint8)
    
    col_mean = img.mean(axis=0)
    row_mean = img.mean(axis=1)

    top    = np.min(np.nonzero(row_mean))
    bottom = np.max(np.nonzero(row_mean))
    left   = np.min(np.nonzero(col_mean))
    right  = np.max(np.nonzero(col_mean))

    top_left = np.array([top, left])
    shape = (bottom - top + 1, right - left + 1)

    return top_left, shape


def boundaryCircle(img: np.array, th: int=10) -> Tuple[np.array, float]:
    """Find the circle that circumferences an endoscopic image. Works only with full view of the endoscopic image.

    Args:
        img (np.array): Grayscale image of shape HxW
        th (int): Whiten threshold, each pixel where value > th is whitened

    Return:
        circle (Tuple[np.array, float]): Center and radius of found circle
    """
    img = np.where(img < th, 0, 255).astype(np.uint8)

    col_mean = img.mean(axis=0)
    row_mean = img.mean(axis=1)

    col_com = np.sum(np.multiply(np.arange(col_mean.shape[0]), col_mean), axis=0)/col_mean.sum()
    row_com = np.sum(np.multiply(np.arange(row_mean.shape[0]), row_mean), axis=0)/row_mean.sum()

    col_radius = (np.max(np.nonzero(col_mean)) - np.min(np.nonzero(col_mean)))/2.
    row_radius = (np.max(np.nonzero(col_mean)) - np.min(np.nonzero(col_mean)))/2.

    radius = max(col_radius, row_radius)

    return np.array([row_com, col_com]), radius


if __name__ == '__main__':
    import os

    prefix = os.getcwd()
    in_file = 'data/eye.tif'

    img = cv2.imread(os.path.join(prefix, in_file))
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    top_left, shape = boundaryRectangle(img_gray, th=30)   
    center, radius = boundaryCircle(img_gray, th=30)

    top_left, shape, center, radius = top_left.astype(np.int), tuple(map(int, shape)), center.astype(np.int), int(radius)

    cv2.rectangle(img, (top_left[1], top_left[0]), (top_left[1] + shape[1], top_left[0] + shape[0]), (255, 255, 0), 1)
    cv2.circle(img, (center[1], center[0]), radius, (0,255,255), 1)
    cv2.circle(img, (center[1], center[0]), 2, (255,0,255), 4)

    cv2.imshow('img', img)
    cv2.waitKey()
