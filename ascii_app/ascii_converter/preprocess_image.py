import cv2
import os
import numpy as np
from ascii_app.ascii_converter import config
from PIL import Image, ImageFont, ImageOps, ImageDraw


##
# @class PreprocessImageAPI
# documentation for class @PreprocessImageAPI
# @details API to pre process image nad provide other image process operation
class PreprocessImageAPI:

    ##
    # Static method, which returns width and height from image
    # @param img cv img
    # @return height and width in int
    @staticmethod
    def get_height_and_width(img):

        try:
            height, width = img.shape
        except:
            height, width, _ = img.shape
        return height, width

    ##
    # Static method, which is wrapper around adaptiveThreshold
    # @param img cv img
    # @return cv image
    @staticmethod
    def binarization(img):
        return cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    ##
    # Static method, which is save image according to DEBUG_PATH from config
    # @param name name of image without extension
    # @param img cv img
    @staticmethod
    def save_image(name, img, extension="png"):
        if config.DEBUG_PATH:
            cv2.imwrite(os.path.join(config.DEBUG_PATH, "%s.%s" % (name, extension)), img)

    ##
    # Static method, which is apply DoG to image
    # @param img cv img
    # @param size_first size of kernel convolution for first image
    # @param size_second size of kernel convolution for second image
    # @param eps
    # @return cv image
    @staticmethod
    def DoG(img, size_first=(3, 3), size_second=(5, 5), eps=2):
        g1 = cv2.GaussianBlur(img, size_first, eps)
        g2 = cv2.GaussianBlur(img, size_second, eps*1.6)
        return g1 - g2

    ##
    # Static method, which is wrapper around medianBlur
    # @param img cv img
    # @param def_size size of kernel convolution for image, as a default it is 3
    # @return cv image
    @staticmethod
    def median_filter(img, def_size=3):
        return cv2.medianBlur(img, 3)

    ##
    # Static method, which is wrapper around cv2.resize
    # @param img cv img
    # @return cv image
    # @error AssertionError
    @staticmethod
    def resize_image(img, fx=2, fy=1):
        assert img is not None
        return cv2.resize(img, (0, 0), fx=fx, fy=fy)

    ##
    # Static method, which is perform main pre processing
    # 1. DoG
    # 2. Median
    # 3. Threshold with mean color of image
    # 4. Median
    # 5. Resize
    # 6. Erode
    # 7. Median
    # @param img cv img
    # @return cv image
    @staticmethod
    def preprocess_image(img):
        # img = PreprocessImageAPI.binarization(img)
        img = PreprocessImageAPI.DoG(img)
        img = PreprocessImageAPI.median_filter(img)
        background_color = np.average(img)
        _, img = cv2.threshold(img, round(background_color), 255, 1)
        # img = PreprocessImageAPI.resize_image(img)
        img = PreprocessImageAPI.median_filter(img)
        kernel = np.ones((3, 3), np.uint8)
        img = cv2.erode(img, kernel, iterations=1)
        img = PreprocessImageAPI.median_filter(img)
        return img

    ##
    # Static method, which crops pil img
    # @param img pil img
    # @param rectangle dict with fields: x, y, width, height
    # @return cropped img
    @staticmethod
    def crop_pil_image(img, rectangle):
        PreprocessImageAPI.check_rectangle(rectangle)
        img = img.crop((rectangle["x"], rectangle["y"],
                        rectangle["x"] + rectangle["width"], rectangle["y"] + rectangle["height"]))
        return np.array(img)
        # # Convert RGB to BGR
        # open_cv_image = open_cv_image[:, :, ::-1].copy()

    ##
    # Static method, which crops cv img
    # @param img cv img
    # @param rectangle dict with fields: x, y, width, height
    # @return cropped img
    @staticmethod
    def crop_cv_image(img, rectangle):
        PreprocessImageAPI.check_rectangle(rectangle)
        return img[rectangle["y"]:rectangle["y"] + rectangle["height"],
                   rectangle["x"]:rectangle["x"] + rectangle["width"]]

    ##
    # Static method, which checks if dict contains with fields: x, y, width, height
    # @param rectangle rectangle dict with fields: x, y, width, height
    # @error AssertionError
    @staticmethod
    def check_rectangle(rectangle):
        assert "x" in rectangle
        assert "y" in rectangle
        assert "width" in rectangle
        assert "height" in rectangle
        for key, value in rectangle.items():
            rectangle[key] = int(value)

    ##
    # Invert cv image, using threshold is equal to 127
    # @param img cv img
    # @return cv img
    @staticmethod
    def invert_image(img):
        height, width = PreprocessImageAPI.get_height_and_width(img)
        copy_img = np.copy(img)
        for i in range(0, height):
            for j in range(0, width):
                if img[i][j] > 127:
                    copy_img[i][j] = 0
                else:
                    copy_img[i][j] = 255
        return copy_img

    ##
    # Static method, which gets image from text file
    # @link https://stackoverflow.com/questions/29760402/converting-a-txt-file-to-an-image-in-python
    # @param text_path path to text file
    # @param font_path path to font
    # @param large_font size of font, as a default it is 12
    # @return pil image
    @staticmethod
    def text_image(text_path, font_path=config.FONT_PATH, large_font=12):

        gray_scale = 'L'
        # parse the file into lines
        with open(text_path, encoding='utf-8') as text_file:
            lines = tuple(l.rstrip() for l in text_file.readlines())
            font = ImageFont.load_default()
            if font_path is not None:
                try:
                    font = ImageFont.truetype(font_path, size=large_font)
                except IOError:
                    font = ImageFont.load_default()

        # points to pixels
        pt2px = lambda pt: int(round(pt * 96.0 / 72))  # convert points to pixels
        max_width_line = max(lines, key=lambda s: font.getsize(s)[0])
        # max height is adjusted down because it's too large visually for spacing
        test_string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        max_height = pt2px(font.getsize(test_string)[1])
        max_width = pt2px(font.getsize(max_width_line)[0])
        height = max_height * len(lines)  # perfect or a little oversized
        width = int(round(max_width + 40))  # a little oversized
        image = Image.new(gray_scale, (width, height), color=config.PIXEL_OFF)
        draw = ImageDraw.Draw(image)

        # draw each line of text
        vertical_position = 5
        horizontal_position = 5
        line_spacing = int(round(max_height * 0.8))  # reduced spacing seems better
        for line in lines:
            draw.text((horizontal_position, vertical_position),
                      line, fill=config.PIXEL_ON, font=font)
            vertical_position += line_spacing
        # crop the text
        c_box = ImageOps.invert(image).getbbox()
        image = image.crop(c_box)
        return image
