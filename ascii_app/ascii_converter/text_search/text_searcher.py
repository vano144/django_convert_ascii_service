import cv2
from cv2 import boundingRect, countNonZero, cvtColor, drawContours, findContours, getStructuringElement
from cv2 import imread, morphologyEx, pyrDown, rectangle, threshold
import numpy as np
import tempfile
from subprocess import Popen, PIPE
from PIL import Image
import re


# TODO: FINISH this module - delete fields and delete rectangles around
# TODO: write unit test

##
# @class TextSearcher
# documentation for class @TextSearcher
# @details API to search and delete text from image
class TextSearcher:

    ##
    #
    # @param cv_image
    # @return
    def __init__(self, cv_image):
        self.img = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        self.output = pyrDown(cv_image)

    ##
    #
    # @param coefficient
    # @return
    def set_width_and_height_metric(self, coefficient=0.35):
        width, height = self.img.shape
        self.max_width = coefficient * width
        self.max_height = coefficient * height
        self.min_width = 8
        self.min_height = 8

    ##
    #
    # @param width:
    # @param height:
    # @return:
    def is_correct_shape(self, width, height):
        return width > self.min_width and height > self.min_height\
               and (width < self.max_width or height < self.max_height)

    ##
    #
    # @param img
    # @param extension
    # @return
    @staticmethod
    def extract_text(img, extension):
        f = tempfile.mkstemp()
        tmp_filename_img = f[1] + ".%s" % extension
        cv2.imwrite(tmp_filename_img, img)
        pipe = Popen(["/usr/local/bin/tesseract", tmp_filename_img, "stdout"], stdin=PIPE, stdout=PIPE)
        result = pipe.communicate()
        res_str = result[0].decode("utf-8")
        return True
        if re.search('[a-zA-Z]', res_str.replace(" ", "")):
            print(res_str)
            return True
        return False

    ##
    #
    # @return
    def extra_preprocess(self):

        assert self.img is not None
        self.img = pyrDown(self.img)
        small = self.img.copy()
        # morphological gradient
        morph_kernel = getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        grad = morphologyEx(small, cv2.MORPH_GRADIENT, morph_kernel)
        # binarize
        _, bw = threshold(src=grad, thresh=0, maxval=255, type=cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        morph_kernel = getStructuringElement(cv2.MORPH_RECT, (9, 1))
        # connect horizontally oriented regions
        connected = morphologyEx(bw, cv2.MORPH_CLOSE, morph_kernel)
        return connected

    ##
    #
    # @param rect_width
    # @param rect_height
    # @return
    @staticmethod
    def calc_ratio(rect_width, rect_height):
        if rect_width >= rect_height:
            ratio = float(rect_height)/rect_width
        else:
            ratio = float(rect_width)/rect_height
        return ratio

    ##
    #
    # @param text_regions
    # @return
    def draw_all_text_regions(self, text_regions):
        for text_region in text_regions:
            self.img = rectangle(self.img, text_region["left_bottom"], text_region["right_top"], (255, 0, 255), 3)

    ##
    #
    # @param text_regions
    # @return
    def delete_all_text_regions(self, text_regions, mean_color):
        for region in text_regions:
            cv2.rectangle(self.img, region["top_left"], region["bottom_right"], mean_color, cv2.FILLED)

    ##
    #
    # @param extra_preprocessed_img
    # @param extension
    # @return
    def find_text(self, extra_preprocessed_img, extension="png"):
        mask = np.zeros(extra_preprocessed_img.shape, np.uint8)
        # find contours
        im2, contours, hierarchy = findContours(extra_preprocessed_img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        # filter contours
        result = []
        # for idx in range(0, len(hierarchy[0])):
        #     if hierarchy[0][idx][0] < 0:
        #         continue # or continue
        #     x, y, rect_width, rect_height = boundingRect(contours[idx])
        #     # fill the contour
        #     mask = drawContours(mask, contours, idx, (255, 255, 2555), cv2.FILLED)
        #     maskROI = mask[y:y+rect_height, x:x+rect_width]
        #     # ratio of non-zero pixels in the filled region
        #     ratio = TextSearcher.calc_ratio(rect_width, rect_height)
        #     p_img = self.img[y:y+rect_height, x:x+rect_width]
        #     r = float(rect_width * rect_height - countNonZero(p_img)) / (rect_width * rect_height)
        #     # r = float(countNonZero(maskROI)) / (rect_width * rect_height)
        #
        #     if r > .10 and self.is_correct_shape(rect_width, rect_height):
        #         if TextSearcher.extract_text(p_img, extension=extension):
        #             # Image.fromarray(p_img).show()
        #             result.append({"top_left": (x, y), "bottom_right": (x + rect_width, y + rect_height)})
        #             self.img = rectangle(self.img, (x, y+rect_height), (x+rect_width, y), (0, 0, 255), 3)
        #
        # return result
        for idx in range(0, len(hierarchy[0])):
            if hierarchy[0][idx][0] < 0:
                break
            x, y, rect_width, rect_height = boundingRect(contours[idx])
            # fill the contour
            # maskROI = (0,0,0)
            mask = drawContours(mask, contours, idx, (255, 255, 2555), cv2.FILLED)
            maskROI = mask[y:y+rect_height, x:x+rect_width]
            p_img = self.img[y:y+rect_height, x:x+rect_width]
            # ratio of non-zero pixels in the filled region
            # r = float(rect_width * rect_height - countNonZero(p_img)) / (rect_width * rect_height)
            r = float(countNonZero(maskROI)) / (rect_width * rect_height)
            # if r > .45 and rect_height > 8 and rect_width > 8:
            print(r)
            if r > .35 and self.is_correct_shape(rect_width, rect_height):
            # if r > .0 and self.is_correct_shape(rect_width, rect_height):
                if TextSearcher.extract_text(p_img, extension=extension):
                    # Image.fromarray(p_img).show()
                    self.output = rectangle(self.output, (x, y+rect_height), (x+rect_width, y), (255, 0, 255), 3)
        return []

    ##
    #
    # @param extension
    # @return
    def find_and_delete_text(self, extension):
        extra_preprocessed_img = self.extra_preprocess()
        text_regions = self.find_text(extra_preprocessed_img, extension)
        # self.delete_all_text_regions(text_regions)