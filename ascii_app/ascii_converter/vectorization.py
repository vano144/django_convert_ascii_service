
from .preprocess_image import PreprocessImageAPI
from .skeleton import Skeleton
import cv2
import os
import ascii_app.ascii_converter.config as config
import numpy as np
from skimage.morphology import label
from .log_system import Log
from .pixel_check import PixelCheck
from .ascii_replacer import AsciiReplacer
import math
import sys
sys.setrecursionlimit(10000)


##
# @class Vectorization
# documentation for class @Vectorization
# @details API to vectorize image
class Vectorization:

    ##
    # Static methods, which find line and try to replace it by ascii symbols
    # @param array_of_possible_lines array of possible lines
    # @param restored_img_by_lines img, whre you can find all vectorized lines
    # @param matr matrix with replaces lines on ascii
    # @param h height of input image
    # @param w width of input image
    @staticmethod
    def find_and_replace_line_by_ascii(array_of_possible_lines, restored_img_by_lines, matr, h, w):

        scale_y = len(matr)/h
        scale_x = len(matr[0])/w
        # scale_y = 1
        # scale_x = 1
        for line in array_of_possible_lines:
            if len(line) <= config.MIN_LENGTH_POINT:
                continue
            epsilon = 0.01 * cv2.arcLength(line, True)  # curve length * 0.1
            approx = cv2.approxPolyDP(line, epsilon, False)
            st_pixel = approx[0][0]
            st_pixel[0] = int(st_pixel[0]*scale_y)
            st_pixel[1] = int(st_pixel[1]*scale_x)
            if len(approx) > 1:
                for i in range(1, len(approx)):
                    pixel = approx[i][0]

                    pixel[0] = int(pixel[0]*scale_y)
                    pixel[1] = int(pixel[1]*scale_x)
                    if config.DEBUG_PATH:
                        cv2.line(restored_img_by_lines, (st_pixel[1], st_pixel[0]),
                                 (pixel[1], pixel[0]), (255, 0, 255), 1)
                    AsciiReplacer.add_line(matr, st_pixel, pixel)
                    # add_line(matr, st_pixel, pixel)
                    st_pixel = pixel

    # TODO: SCHEMA 2.4 section
    ##
    # Static method, which perform extra split in bounded field
    # @param field part of labeled - image after separation on bonded fields
    # @param labeled image after separation on bonded fields
    # @param current_img current image
    # @return array of new fields
    @staticmethod
    def split_fields(field, labeled, current_img):

        # * * *
        # * x *
        # * * *

        new_result = []
        pre_result = []
        counter = 0
        for point in field:
            x = point[1]
            y = point[0]

            pre_result.append([y, x])
            criterion = 0

            if config.SPLIT_FIELDS_AS == 8:

                # x - 1 y -1
                criterion += PixelCheck.check_pixel(x - 1, y - 1, current_img)

                # x + 1 y - 1
                criterion += PixelCheck.check_pixel(x + 1, y - 1, current_img)

                # x - 1 y + 1
                criterion += PixelCheck.check_pixel(x - 1, y + 1, current_img)

                # x + 1 y + 1
                criterion += PixelCheck.check_pixel(x + 1, y + 1, current_img)

            # x  y - 1
            criterion += PixelCheck.check_pixel(x, y - 1, current_img)

            # x - 1 y
            criterion += PixelCheck.check_pixel(x - 1, y, current_img)
            # nothing
            # x + 1 y
            criterion += PixelCheck.check_pixel(x + 1, y, current_img)

            # x y + 1
            criterion += PixelCheck.check_pixel(x, y + 1, current_img)

            distance_criterion = counter+1 < len(field) and\
                math.sqrt((field[counter+1][1]-x)*(field[counter+1][1]-x) +
                          (field[counter+1][0]-y)*(field[counter+1][0]-y)) >= 2

            # if distance_criterion:
            if criterion > 2 or distance_criterion:
                new_result.append(np.array(pre_result))
                pre_result = []
            counter += 1

        if len(pre_result) != 0:
            new_result.append(np.array(pre_result))

        return new_result

    # TODO: SCHEMA 2.2 section
    ##
    # Static methods, which perform special sort of field from image after separation on bonded fields
    # @param labeled image after separation on bonded fields
    # @param i y coordinate
    # @param j x coordinate
    # @param result array of sorted fields
    # @param was_here_matrix matrix to avoid circles
    # @param current_img current cv img
    @staticmethod
    def sort_points_in_area(labeled, i, j, result, was_here_matrix, current_img):
        current_color = labeled[i][j]
        y = i
        x = j
        was_here_matrix[y][x] = 1
        result[current_color].append([y, x])

        # x  y - 1
        if PixelCheck.check_pixel_with_color(x, y - 1, labeled, current_color, was_here_matrix, current_img) == 1:
            Vectorization.sort_points_in_area(labeled, y - 1, x, result, was_here_matrix, current_img)

        # x - 1 y
        if PixelCheck.check_pixel_with_color(x - 1, y, labeled, current_color, was_here_matrix, current_img) == 1:
            Vectorization.sort_points_in_area(labeled, y, x - 1, result, was_here_matrix, current_img)
        # nothing
        # x + 1 y
        if PixelCheck.check_pixel_with_color(x + 1, y, labeled, current_color, was_here_matrix, current_img) == 1:
            Vectorization.sort_points_in_area(labeled, y, x + 1, result, was_here_matrix, current_img)

        # x y + 1
        if PixelCheck.check_pixel_with_color(x, y + 1, labeled, current_color, was_here_matrix, current_img) == 1:
            Vectorization.sort_points_in_area(labeled, y + 1, x, result, was_here_matrix, current_img)

        if config.SORT_POINTS_AS == 8:
            # x - 1 y -1
            if PixelCheck.check_pixel_with_color(x - 1, y - 1, labeled, current_color, was_here_matrix, current_img) == 1:
                Vectorization.sort_points_in_area(labeled, y - 1, x - 1, result, was_here_matrix, current_img)

            # x + 1 y - 1
            if PixelCheck.check_pixel_with_color(x + 1, y - 1, labeled, current_color, was_here_matrix, current_img) == 1:
                Vectorization.sort_points_in_area(labeled, y - 1, x + 1, result, was_here_matrix, current_img)

            # x - 1 y + 1
            if PixelCheck.check_pixel_with_color(x - 1, y + 1, labeled, current_color, was_here_matrix, current_img) == 1:
                Vectorization.sort_points_in_area(labeled, y + 1, x - 1, result, was_here_matrix, current_img)

            # x + 1 y + 1
            if PixelCheck.check_pixel_with_color(x + 1, y + 1, labeled, current_color, was_here_matrix, current_img) == 1:
                Vectorization.sort_points_in_area(labeled, y + 1, x + 1, result, was_here_matrix, current_img)

    ##
    # Static method, which counts neighbour for current pixel
    # @param img cv img
    # @param x x coordinate
    # @param y y coordinate
    # @param val  value to compare with, default value is 0
    # @return amount of neighbours for current pixel
    @staticmethod
    def count_neighbours(img, x, y, val=0):
        res = 0
        if 8 == config.COUNT_NEIGHBOURS_AS:
            # x - 1 y -1
            if PixelCheck.check_pixel_bool_result(img, x - 1, y - 1, val):
                res += 1

            # x + 1 y - 1
            if PixelCheck.check_pixel_bool_result(img, x + 1, y - 1, val):
                res += 1

            # x - 1 y + 1
            if PixelCheck.check_pixel_bool_result(img, x - 1, y + 1, val):
                res += 1

            # x + 1 y + 1
            if PixelCheck.check_pixel_bool_result(img, x + 1, y + 1, val):
                res += 1

        # x  y - 1
        if PixelCheck.check_pixel_bool_result(img, x, y - 1, val):
            res += 1

        # x - 1 y
        if PixelCheck.check_pixel_bool_result(img, x - 1, y, val):
            res += 1
        # nothing
        # x + 1 y
        if PixelCheck.check_pixel_bool_result(img, x + 1, y, val):
            res += 1

        # x y + 1
        if PixelCheck.check_pixel_bool_result(img, x, y + 1, val):
            res += 1
        return res

    # TODO: SCHEMA 2.3 section
    ##
    # Static method, which sorts field on labeled region
    # @param labeled image after separation on bonded fields
    # @param i
    # @param j
    # @return sorted pixel in special order
    @staticmethod
    def find_first_element_by_labeled(labeled, i, j):
        labeled_copy = np.copy(labeled)
        labeled_copy = PixelCheck.clear_except(labeled_copy, labeled[i][j])
        amount_of_neighbours = {}
        # to do
        x, y = np.where(labeled_copy != 0)
        elements = zip(y, x)
        for point in elements:
            amount_of_neighbours[(point[0], point[1])] = Vectorization.count_neighbours(labeled_copy, point[1],
                                                                                        point[0], val=labeled[i][j])
        return sorted(amount_of_neighbours.items(), key=lambda x: x[1])[0][0], labeled_copy

    ##
    # Static method, which converts image to IMREAD_COLOR
    # @param img img
    # @return colored img
    @staticmethod
    def convert_image_to_1(img):
        # TODO: convert to 1
        Log.log.warning('This is a warning message.')
        PreprocessImageAPI.save_image('SKISKELET', img)
        img_res = cv2.imread(os.path.join(config.FOLDER_RESULT, 'SKISKELET.png'), 1)
        return img_res

    ##
    # Static methods to convert labeled fields into array
    # @param labeled image after separation on bonded fields
    # @param height height of img
    # @param width width of img
    # @return array of points of regions
    @staticmethod
    def get_amount_of_regions(labeled, height, width):
        result = []
        for i in range(0, height):
            for j in range(0, width):
                if labeled[i][j] not in result:
                    result.append(labeled[i][j])
        result.sort()
        return result

    ##
    # Static method, to draw all bounded fields in color
    # @param img cv img
    # @param array_of_variants_of_regions array of regions of equal field
    # @param labeled image after separation on bonded fields
    # @param height height of img
    # @param width width of img
    # @return colored img
    @staticmethod
    def colored_fields_on_image(img, array_of_variants_of_regions, labeled, height, width):
        # TODO: systaksis sugar
        colored = []
        colored.append([0, 0, 0])
        for i in range(1, len(array_of_variants_of_regions)):
            r = np.random.randint(0, 255, 1)[0]
            g = np.random.randint(0, 255, 1)[0]
            b = np.random.randint(0, 255, 1)[0]
            colored.append([r, g, b])

        for i in range(0, height):
            for j in range(0, width):
                r = colored[labeled[i][j]][0]
                g = colored[labeled[i][j]][1]
                b = colored[labeled[i][j]][2]
                img[i][j][0] = r
                img[i][j][1] = g
                img[i][j][2] = b
        return img

    ##
    # Static method, which return matrix, which is initialized by init value
    # @param h height of img
    # @param w width of img
    # @param init_value value to initialize matrix
    # @return matrix
    @staticmethod
    def get_matrix(h, w, init_value=0):
        matrix = [[init_value for y in range(w)] for x in range(h)]
        return matrix

    ##
    # Static method which sort points in bounded fields using schema from 2.3 and 2.2 algorithms
    # @param labeled image after separation on bonded fields
    # @param height height of img
    # @param width width of img
    # @param img cv img
    # @return tuple of set of new sorted fields and cv img
    @staticmethod
    def sort_points(labeled, height, width, img):
        set_of_fields = {}
        was_here_matrix = Vectorization.get_matrix(height, width, -1)
        for i in range(0, height):
            for j in range(0, width):
                if labeled[i][j] == 0:
                    set_of_fields[labeled[i][j]] = []
                    continue
                if labeled[i][j] in set_of_fields:
                    continue
                else:
                    set_of_fields[labeled[i][j]] = []
                    if config.SEARCH_FIRST_POINT:
                        [init_i, init_j], labeled_copy = Vectorization.find_first_element_by_labeled(labeled, i, j)
                        Vectorization.sort_points_in_area(labeled_copy, init_j, init_i,
                                                          set_of_fields, was_here_matrix, img)
                    else:
                        Vectorization.sort_points_in_area(labeled, i, j, set_of_fields, was_here_matrix, img)
        return set_of_fields, img

    # obsolete
    @staticmethod
    def get_new_labeled_image(array_of_possible_lines):
        new_labeled = []
        for line in array_of_possible_lines:
            # if len(line) > config.MIN_LENGTH_POINT:
            new_labeled.append(line)
        return new_labeled

    ##
    # Static method to show new sorted fields
    # @param new_labeled array of lines
    # @param w image's width
    # @param h image's height
    # @return colored image
    @staticmethod
    def get_img_with_draw_lines(new_labeled, w, h):

        img_res_m = np.zeros((h, w, 3), np.uint8)
        for line in new_labeled:
            r = np.random.randint(0, 255, 1)[0]
            g = np.random.randint(0, 255, 1)[0]
            b = np.random.randint(0, 255, 1)[0]
            for pixel in line:
                img_res_m[pixel[0]][pixel[1]][0] = r
                img_res_m[pixel[0]][pixel[1]][1] = g
                img_res_m[pixel[0]][pixel[1]][2] = b
        return img_res_m

    ##
    # Static method, which find possible lines by sortimg points in fields
    # @param img image after skeletonization @Skeleton
    # @param background_indexes indexes of background color
    # @return set of new sorted fields, copy of input image after skeletonization and @convert_image_to_1,
    #  labeled, height and width of input image
    @staticmethod
    def points_resort(img, background_indexes):
        # inv_img = PreprocessImageAPI.invert_image(img)
        img_res = Vectorization.convert_image_to_1(img)
        img_res_approx = np.copy(img_res)

        skel = Skeleton.from_255_To_1_special(img)
        # labeled part
        labeled = label(skel, 8, background=img[background_indexes[0]][background_indexes[1]])
        height, width = PreprocessImageAPI.get_height_and_width(labeled)
        array_of_variants_of_regions = Vectorization.get_amount_of_regions(labeled, height, width)
        Log.log.warning("MAX %d" % max(array_of_variants_of_regions))
        Log.log.warning("MIN %d" % min(array_of_variants_of_regions))

        # TODO: ONLY IN Debug mode
        if config.DEBUG_PATH:
            colored_img = Vectorization.colored_fields_on_image(img_res, array_of_variants_of_regions, labeled, height, width)
            PreprocessImageAPI.save_image('SKISKELET.png', colored_img)
        Log.log.warning('sort points start')
        set_of_fields, img_res_approx = Vectorization.sort_points(labeled, height, width, img_res_approx)
        Log.log.warning('sort points end')
        return set_of_fields, img_res_approx, labeled, height, width


