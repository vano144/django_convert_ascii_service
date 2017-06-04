import os
import numpy as np
from ascii_app.ascii_converter import config
from .vectorization import Vectorization
from .ascii_replacer import AsciiReplacer


##
# Main function to process lines from image in which set of fields, it extracts array of lines, which than transfer
#  to @Vectorization module to define if it line or not and replace it by ascii symbol
# @param set_of_fields dict of sets of fields
# @param img_res_approx copy of input image after skeletonization and @convert_image_to_1
# @param labeled labeled image after separation on bonded fields
# @param height input image height
# @param width input image width
# @return path to file with replaced lines by ascii symbols
def process_lines(set_of_fields, img_res_approx, labeled, height, width):
    new_height, want_width = AsciiReplacer.count_new_height_and_width(height, width)
    matrix = Vectorization.get_matrix(int(new_height/config.AMOUNT_SKIP_PIXEL), int(want_width/config.AMOUNT_SKIP_PIXEL))
    img_res = np.zeros((int(new_height/config.AMOUNT_SKIP_PIXEL), int(want_width/config.AMOUNT_SKIP_PIXEL), 3), np.uint8)

    for i in range(min(set_of_fields.keys()), max(set_of_fields.keys())+1):
        print(i)
        input_array = np.array(set_of_fields[i])
        pre_new_input_array = Vectorization.split_fields(input_array, labeled, img_res_approx)
        Vectorization.find_and_replace_line_by_ascii(pre_new_input_array, img_res, matrix, height, width)
    return matrix


