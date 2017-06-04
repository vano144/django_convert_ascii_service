from .helpers import process_image, skeletonization, convert_image_to_ascii
from .metric import Metric
from PIL import Image
import cv2
import os


# TODO: write unit test


def process_image_test(path):
    if os.path.exists(path):
        img = cv2.imread(path, 0)
        img = process_image(img)
        Image.fromarray(img).show()


def skeletonization_test(path):
    if os.path.exists(path):
        img = cv2.imread(path, 0)
        img = process_image(img)
        img, _ = skeletonization(img)
        Image.fromarray(img).show()


def main_test(path):
    if os.path.exists(path):
        img = cv2.imread(path, 0)
        convert_image_to_ascii(img)

ex_path = '/Users/v144/Documents/workspace/docker_mount/project/data/testData/1.png'

# main_test(ex_path)
