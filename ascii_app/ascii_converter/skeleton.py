from skimage import morphology, img_as_ubyte
from PIL import Image
import scipy
import scipy.cluster
import scipy.misc
import cv2
import os
from .preprocess_image import PreprocessImageAPI


##
# @class Skeleton
# documentation for class @Skeleton
# @details API to extract skeleton from image
class Skeleton:

    ##
    # Static method, which return background color according to kmeans
    # @param img cv_img
    # @param num_clusters amount of clusters
    # @return dominated color
    @staticmethod
    def background_color(img, num_clusters=3):
        print('reading image')
        im = Image.fromarray(img).convert('LA')
        # im = Image.open(path).convert('LA')
        im = im.resize((150, 150))      # optional, to reduce time
        ar = scipy.misc.fromimage(im)
        shape = ar.shape
        ar = ar.reshape(scipy.product(shape[:2]), shape[2])

        print('finding clusters')
        codes, dist = scipy.cluster.vq.kmeans(ar.astype('double'), num_clusters)
        print('cluster centres:\n', codes)

        vecs, dist = scipy.cluster.vq.vq(ar, codes)         # assign codes
        counts, bins = scipy.histogram(vecs, len(codes))    # count occurrences

        result = []
        index_max = scipy.argmax(counts)                    # find most frequent
        peak = codes[index_max]
        result.append(peak[0])
        return result

    ##
    # Static method, which change 0 value to 1 and for others change to 0
    # @param img cv img
    # @return cv img with pixel only 0 and 1
    @staticmethod
    def from_255_To_1_special(img):
        height, width = PreprocessImageAPI.get_height_and_width(img)
        for i in range(0, height):
            for j in range(0, width):
                if img[i][j] == 0:
                    img[i][j] = 1
                else:
                    img[i][j] = 0

        return img

    ##
    # Static method, which change all value not equaled to 0 on 255
    # @param img cv img
    # @return cv img
    @staticmethod
    def from_1_To_255(img):
        height, width = PreprocessImageAPI.get_height_and_width(img)
        for i in range(0, height):
            for j in range(0, width):
                if img[i][j] != 0:
                    img[i][j] = 255
        return img

    ##
    # Static methods calculates background color of image
    # @param img cv img
    # @return int value of color in range [0, 255]
    @staticmethod
    def calc_background_color(img):
        peak = Skeleton.background_color(img)
        b_c = int(peak[0])
        return b_c

    ##
    # Static methods which perform binarization according to value, apart from it returns indexes of background color
    # @param img cv img
    # @param b_c background color
    # @return tuple of cv img and background indexes
    @staticmethod
    def binarize_by_threshold(img, b_c):
        height, width = PreprocessImageAPI.get_height_and_width(img)
        background_indexes = None
        for i in range(0, height):
            for j in range(0, width):
                if img[i][j] > b_c:
                    img[i][j] = 255
                else:
                    img[i][j] = 0
                    if background_indexes is None:
                        background_indexes = [i, j]
        return img, background_indexes

    ##
    # Static methods which extract skeleton, using morphology.skeletonize from ski package
    # @param img cv img
    # @return tuple of cv img and background indexes
    @staticmethod
    def ski_skeleton(img):
        try:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        except cv2.error:
            pass
        img = Skeleton.from_255_To_1_special(img)
        skeleton = morphology.skeletonize(img)
        img = img_as_ubyte(skeleton)
        img = Skeleton.from_1_To_255(img)
        b_c = Skeleton.calc_background_color(img)
        return Skeleton.binarize_by_threshold(img, b_c=b_c)
