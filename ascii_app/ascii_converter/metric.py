from .helpers import process_image, skeletonization, convert_image_to_ascii
from .preprocess_image import PreprocessImageAPI
from ascii_app.ascii_converter import config
from .log_system import Log
from PIL import Image
import cv2
import uuid
import os
import numpy as np


##
# @class Metric
# documentation for class @Metric
# @details API to check different stage of algorithm
class Metric:
    path_to_save_result = ""

    ##
    # Static method to calc MSE between two images
    # @param image_a first image
    # @param image_b second image
    # @return the MSE, the lower the error, the more "similar" the two images are
    @staticmethod
    def mse(image_a, image_b):
        err = np.sum((image_a.astype("float") - image_b.astype("float")) ** 2)
        err /= float(image_a.shape[0] * image_b.shape[1])
        return err

    ##
    # Static method, which finds distance to nearest filled pixel
    # @param cur_pixel current pixel
    # @param region distance - 0, 1, 2 and etc.
    # @param original_image original image
    # @param dominant_color background color
    # @return 0, -1 or region
    @staticmethod
    def check_nearest_neighbour(cur_pixel, region, original_image, dominant_color):
        h, w = PreprocessImageAPI.get_height_and_width(original_image)
        left_width = cur_pixel[0] - region
        right_width = cur_pixel[0] + region
        top_height = cur_pixel[1] - region
        bottom_height = cur_pixel[1] + region
        if left_width < 0 or top_height < 0 or right_width >= w or bottom_height >= h:
            return 0

        for i in range(left_width, right_width + 1):
            if original_image[i][cur_pixel[1] + region] != dominant_color:
                return region
            if original_image[i][cur_pixel[1] - region] != dominant_color:
                return region

        for j in range(top_height, bottom_height + 1):
            if original_image[cur_pixel[0] + region - 1][j] != dominant_color:
                return region
            if original_image[cur_pixel[0] - region + 1][j] != dominant_color:
                return region
        return -1

    ##
    # Static method, which calculates distance to near filled pixel on ideal image
    # @param i y
    # @param j x
    # @param original_image original image
    # @param dominant_color background color
    # @return value for current pixel
    @staticmethod
    def find_nearest_neighbour(i, j, original_image, dominant_color):
        if original_image[i][j] != dominant_color:
            return 0
        cur_pixel = (i, j)
        region = 1
        while True:
            result = Metric.check_nearest_neighbour(cur_pixel, region, original_image, dominant_color)
            if result == -1:
                region += 1
                continue
            else:
                return result

    # TODO: SCHEME 4.1
    ##
    # Static methods, which calculates metrics for image according to SCHEME
    # @param original_img original image
    # @param ideal_img ideal image
    # @param dominant_color background color
    # @param stage_name stage's name
    # @return float value of metrics
    @staticmethod
    def calc_metrics(original_img, ideal_img, dominant_color, stage_name):
        w, h = ideal_img.shape
        distance = 0
        amount = 0
        amount_bad_cell = 0
        for i in range(w-1):
            for j in range(h-1):
                if ideal_img[i][j] != dominant_color:
                    amount += 1
                    distance_res = Metric.find_nearest_neighbour(i, j, original_img, dominant_color)
                    if distance_res != 0:
                        amount_bad_cell += 1
                    distance += distance_res
        print("Stage %s: Amount - %d, Distance - %d, Cell amount - %d, Criteria %s " % (stage_name,
                                                                                        amount, distance,
                                                                                        amount_bad_cell,
                                                                                        str(distance/amount)))
        return distance/amount

    ##
    # Static methods, which saves img according to DEBUG_PATH
    # @param name image's name
    # @param img cv img
    @staticmethod
    def save_img(name, img):
        if config.DEBUG_PATH and Metric.path_to_save_result:
            cv2.imwrite(os.path.join(Metric.path_to_save_result, name), img)

    ##
    # Static method, which calculates metric for stage - PreProcessing
    # @param original_img_path path to original image
    # @param ideal_img_path path to ideal image
    # @return float value of metrics
    # @error AssertionError
    @staticmethod
    def compare_img(original_img_path, ideal_img_path):
        assert os.path.exists(original_img_path)
        assert os.path.exists(ideal_img_path)
        stage_name = "PreProcessing"
        original_img = cv2.imread(original_img_path)
        original_img = process_image(original_img)
        ideal_img = cv2.imread(ideal_img_path, 0)
        # pil_image1 = Image.fromarray(original_img)
        # pil_image2 = Image.fromarray(ideal_img)
        return Metric.calc_metrics(original_img, ideal_img, 255, stage_name=stage_name)

    ##
    # Static method, which calculates metric for stage - Skeletonization
    # @param original_img_path path to original image
    # @param ideal_img_path path to ideal image
    # @return float value of metrics
    # @error AssertionError
    @staticmethod
    def compare_skeletonization(original_img_path, ideal_img_path):
        assert os.path.exists(original_img_path)
        assert os.path.exists(ideal_img_path)
        stage_name = "Skeletonization"
        original_img = cv2.imread(original_img_path)
        original_img = process_image(original_img)
        original_img_skeleton, _ = skeletonization(original_img)
        ideal_img = cv2.imread(ideal_img_path, 0)
        return Metric.calc_metrics(original_img_skeleton, ideal_img, 0, stage_name=stage_name)

    ##
    # Static method, which calculates metric for stage - Ascii
    # @param original_img_path path to original image
    # @param ideal_img_path path to ideal image
    # @return float value of metrics
    # @error AssertionError
    @staticmethod
    def compare_ascii(original_img_path, ideal_img_path):
        assert os.path.exists(original_img_path)
        assert os.path.exists(ideal_img_path)
        stage_name = "Ascii"
        original_img = cv2.imread(original_img_path)
        ideal_img = cv2.imread(ideal_img_path, 0)
        ascii_img, path_to_ascii, _ = convert_image_to_ascii(original_img)
        open_cv_image = np.array(ascii_img)
        return Metric.calc_metrics(open_cv_image, ideal_img, 0, stage_name=stage_name)

    ##
    # Static method which counts metric for all major stages of algorithm
    # @param original_img_path path to original image
    # @param ideal_pre_processing_path path to ideal pre processed image
    # @param ideal_skeletonization_path path to ideal skeleton image
    # @param ideal_ascii_path path to ideal ascii image
    # @param path_to_save_result path to save result
    # @return tuple of pre_processed_metric, skeleton_metric, ascii_metric
    @staticmethod
    def run_comparing(original_img_path, ideal_pre_processing_path, ideal_skeletonization_path, ideal_ascii_path,
                      path_to_save_result=""):
        if path_to_save_result and not os.path.exists(path_to_save_result):
            os.mkdir(path_to_save_result)
        Metric.path_to_save_result = path_to_save_result
        pre_processed_metric = Metric.compare_img(original_img_path, ideal_pre_processing_path)
        skeleton_metric = Metric.compare_skeletonization(original_img_path, ideal_skeletonization_path)
        ascii_metric = Metric.compare_ascii(original_img_path, ideal_ascii_path)
        return pre_processed_metric, skeleton_metric, ascii_metric
