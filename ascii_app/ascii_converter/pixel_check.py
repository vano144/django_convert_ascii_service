

##
# @class PixelCheck
# documentation for class @PixelCheck
# @details API to perform different checks on image according to pixels
class PixelCheck:

    ##
    # Static method, which checks current pixel of img if it belong to current field
    # @param x0 x coordinate
    # @param y0 y coordinate
    # @param labeled image after separation on bonded fields
    # @param cur_color current color of field
    # @param was_here_matrix matrix to avoid circles
    # @param current_img current cv image
    # @return 0 or 1
    @staticmethod
    def check_pixel_with_color(x0, y0, labeled, cur_color, was_here_matrix, current_img):

        try:
            # first for background
            if current_img[y0][x0][0] == 0:
                return 0
            if labeled[y0][x0] != cur_color or was_here_matrix[y0][x0] == 1:
                return 0
        except:
            return 0
        return 1

    ##
    # Static method, which checks if current pixel not equal 0
    # @param x0 x coordinate
    # @param y0 y coordinate
    # @param current_img current cv image
    # @return 0 or 1
    @staticmethod
    def check_pixel(x0, y0, current_img):

        try:
            if current_img[y0][x0][0] != 0:
                return 1
        except:
            pass
        return 0

    ##
    # Static method, which checks if current pixel not equal val
    # @param img current cv image
    # @param i y coordinate
    # @param j x coordinate
    # @param val value to compare with, default value 0
    # @return boolean
    @staticmethod
    def check_pixel_bool_result(img, i, j, val=0):
        try:
            if img[i][j] == val:
                return True
        except:
            pass
        return False

    ##
    # Static method, which clear labeled from all pixels which is not equal to value
    # @param labeled image after separation on bonded fields
    # @param val int
    # @return labeled
    @staticmethod
    def clear_except(labeled, value):
        for i in range(0, len(labeled)):
            for j in range(0, len(labeled[0])):
                if labeled[i][j] != value:
                    labeled[i][j] = 0
        return labeled
