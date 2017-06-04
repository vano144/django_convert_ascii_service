import ascii_app.ascii_converter.config as config
import math
from .log_system import Log
# coding: utf8


##
# @class AsciiReplacer
# documentation for class @AsciiReplacer
# @details API to replace lines by ascii symbols
class AsciiReplacer:
    tg_15 = math.tan(math.radians(15))
    tg_m_15 = math.tan(math.radians(-15))

    tg_75 = math.tan(math.radians(75))

    tg_30 = math.tan(math.radians(35))
    tg_60 = math.tan(math.radians(55))

    tg_m_30 = math.tan(math.radians(-35))
    tg_m_60 = math.tan(math.radians(-55))

    ##
    # Static method, which calculates new width and height according to LIMIT_WIDTH
    #  from config and aspect ration from input parameters
    # @param original_height original height in int
    # @param original_width original width in int
    # @return tuple of new_height, new_width in int
    @staticmethod
    def count_new_height_and_width(original_height, original_width):
        config.ASPECT_RATIO = original_height/float(original_width)
        new_width = original_width
        new_height = original_height
        if new_width > config.LIMIT_WIDTH:
            new_width = config.LIMIT_WIDTH
            new_height = int(config.ASPECT_RATIO * new_width)
        if new_height > config.LIMIT_HEIGHT:
            new_height = config.LIMIT_HEIGHT
            new_width = int((1.0/config.ASPECT_RATIO) * new_height)
        print("H: %d, W: %d" % (new_height, new_width))
        return new_height, new_width

    # TODO: SCHEMA 2.5 section
    ##
    # Static method, which fills matrix by ascii symbols on positions: line(st_pixel, pixel)
    # @param res_matr matrix in which the addition is happening
    # @param st_pixel start pixel of line
    # @param pixel end pixel of line
    @staticmethod
    def add_line(res_matr, st_pixel, pixel):

        y1 = pixel[0]
        x1 = pixel[1]

        y0 = st_pixel[0]
        x0 = st_pixel[1]

        dx = (x1 - x0) if x1 > x0 else (x0 - x1)
        dy = (y1 - y0) if (y1 > y0) else (y0 - y1)
        sx = 1 if (x1 >= x0) else (-1)
        sy = 1 if (y1 >= y0) else (-1)
        step = config.AMOUNT_SKIP_PIXEL
        dy_tg = y1 - y0
        dx_tg = x1 - x0
        if dx_tg == 0:
            cur_symbol = "⎪"
        else:
            tg = dy_tg / dx_tg

            if abs(tg) > AsciiReplacer.tg_75:
                cur_symbol = "⎪"
            else:
                if AsciiReplacer.tg_m_15 < tg < AsciiReplacer.tg_15:
                    cur_symbol = "–"
                else:
                    if AsciiReplacer.tg_60 > tg > AsciiReplacer.tg_30:
                        cur_symbol = "/"
                    else:
                        if AsciiReplacer.tg_m_60 < tg < AsciiReplacer.tg_m_30:
                            cur_symbol = "\\"
                        else:
                            cur_symbol = "*"

        if dy < dx:

            d = (dy << 1) - dx
            d1 = dy << 1
            d2 = (dy - dx) << 1
            try:
                res_matr[int(y0/step)][int(x0/step)] = cur_symbol
            except:
                print(y0, x0)

            x = x0 + sx
            y = y0
            tmp = cur_symbol
            for i in range(0, dx+1, step):
                if d > 0:
                    if sx*sy > 0:
                        cur_symbol = "\\"
                    else:
                        if sx*sy < 0:
                            cur_symbol = "/"
                        else:
                            cur_symbol = "*"
                    d += d2
                    y += sy
                else:
                    cur_symbol = tmp
                    d += d1
                try:
                    # write_symbol_to_matrix(res_matr, sx, sy, x, y, cur_symbol)
                    res_matr[int(y/step)][int(x/step)] = cur_symbol
                except:
                    return
                x += sx
        else:
            d = (dx << 1) - dy
            d1 = dx << 1
            d2 = (dx - dy) << 1
            try:
                res_matr[int(y0/step)][int(x0/step)] = cur_symbol
            except:
                Log.log.critical("step problem")
            x = x0
            y = y0 + sy
            tmp = cur_symbol
            for i in range(1, dy+1, step):
                if d > 0:
                    if sx*sy > 0:
                        cur_symbol = "\\"
                    else:
                        if sx*sy < 0:
                            cur_symbol = "/"
                        else:
                            cur_symbol = "*"
                    d += d2
                    x += sx

                else:
                    cur_symbol = tmp
                    d += d1
                try:
                    # write_symbol_to_matrix(res_matr, sx, sy, x, y, cur_symbol)
                    res_matr[int(y/step)][int(x/step)] = cur_symbol
                except:
                    return
                y += sy

    ##
    # Static method, which outputs matrix in console
    # @param matrix matrix with ascii symbols
    @staticmethod
    def write_matrix_to_console(matrix):
        for i in range(0, len(matrix)):
            for j in range(0, len(matrix[i])):
                try:
                    cur_symbol = matrix[i][j]
                except KeyError:
                    Log.log.critical("j %d len %d, i %d len %d" % (j, len(matrix[i]), i, len(matrix)))
                    return None
                if cur_symbol == 0:
                    print(" ", end="")
                else:
                    print(cur_symbol, end="")
            print("")
        return

    ##
    # Static method, which writes matrix in file according to filename
    # @param matrix matrix with ascii symbols
    # @param file_name
    @staticmethod
    def write_matrix_to_file(matrix, file_name):
        file_out = open(file_name, 'w', encoding="utf-8")
        for i in range(0, len(matrix)):
            for j in range(0, len(matrix[i])):
                try:
                    cur_symbol = matrix[i][j]
                except KeyError:
                    Log.log.critical("j %d len %d, i %d len %d" % (j, len(matrix[i]), i, len(matrix)))
                    return None
                if cur_symbol == 0:
                    file_out.write(" ")
                else:
                    file_out.write(cur_symbol)
            file_out.write("\n")
        file_out.close()
        return
