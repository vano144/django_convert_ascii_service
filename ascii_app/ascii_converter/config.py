import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "resources", "test_data")
OUTPUT_DIR = os.path.join(BASE_DIR, "resources", "output")
FOLDER_RESULT = "/tmp"
ASCII_FILE_NAME_OTHER = "result_ascii_other.txt"
ASCII_FILE_NAME = "result_ascii.txt"
ASCII_IMAGE_NAME = "result_ascii_img.png"
ASCII_IMAGE_NAME_OTHER = "result_ascii_img_other.png"
FONT_PATH = os.path.join(BASE_DIR, "resources", "fonts", "Menlo.ttc")
MIN_LENGTH_POINT = 2
EPSILON_ANGLE = 30.0
AMOUNT_SKIP_PIXEL = 1
ASPECT_RATIO = 1
PIXEL_ON = 0
PIXEL_OFF = 255
SEARCH_FIRST_POINT = True

SORT_POINTS_AS = 8
COUNT_NEIGHBOURS_AS = 8
SPLIT_FIELDS_AS = 8
LIMIT_WIDTH = 100
LIMIT_HEIGHT = 100

DEBUG_PATH = "/tmp"
