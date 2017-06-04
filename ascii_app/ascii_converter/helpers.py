from .preprocess_image import PreprocessImageAPI
from .skeleton import Skeleton
from .text_search import TextSearcher
from .vectorization import Vectorization
from .ski_step import process_lines
from .utils import get_tmp_file_name, get_str_content_from_file
from .ascii_replacer import AsciiReplacer
from PIL import Image

# TODO: Call TextSearcher


##
# Pre process image by API from @PreprocessImageAPI
# @param img cv image
# @return pre processed cv image
def process_image(img):
    return PreprocessImageAPI.preprocess_image(img)


##
# Extract skeleton from image
# @param img cv image
# @return image with extracted skeleton and tuple of background indexes
def skeletonization(img):
    return Skeleton.ski_skeleton(img)


##
# Converts image to ascii
# @param img cv image
# @return ascii text and image of its
def convert_image_to_ascii(img, file_name=None, to_console=None):
    img = process_image(img)
    img, background_indexes = skeletonization(img)
    set_of_fields, img_res_approx, labeled, height, width = Vectorization.points_resort(img, background_indexes=background_indexes)
    matrix = process_lines(set_of_fields, img_res_approx, labeled, height, width)
    if file_name is None:
        file_name = get_tmp_file_name()
    if to_console:
        AsciiReplacer.write_matrix_to_console(matrix)
    AsciiReplacer.write_matrix_to_file(matrix, file_name=file_name)
    result_img = PreprocessImageAPI.text_image(file_name)
    result_text = get_str_content_from_file(file_name)
    return result_img, result_text


