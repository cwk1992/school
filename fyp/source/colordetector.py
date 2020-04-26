from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np
import cv2

import argparse
import imutils


class ColorDetector:
    def __init__(self):
        # initialize the colors dictionary, containing the color
        # name as the key and the RGB tuple as the value
        colors = OrderedDict({
            "INDIANRED": (205, 92, 92),
            "LIGHTCORAL": (240, 128, 128),
            "SALMON": (250, 128, 114),
            "DARKSALMON": (233, 150, 122),
            "LIGHTSALMON": (255, 160, 122),
            "CRIMSON": (220, 20, 60),
            "RED": (255, 0, 0),
            "FIREBRICK": (178, 34, 34),
            "DARKRED": (139, 0, 0),
            "PINK": (255, 192, 203),
            "LIGHTPINK": (255, 182, 193),
            "HOTPINK": (255, 105, 180),
            "DEEPPINK": (255, 20, 147),
            "MEDIUMVIOLETRED": (199, 21, 133),
            "PALEVIOLETRED": (219, 112, 147),
            "LIGHTSALMON": (255, 160, 122),
            "CORAL": (255, 127, 80),
            "TOMATO": (255, 99, 71),
            "ORANGERED": (255, 69, 0),
            "DARKORANGE": (255, 140, 0),
            "ORANGE": (255, 165, 0),
            "GOLD": (255, 215, 0),
            "YELLOW": (255, 255, 0),
            "LIGHTYELLOW": (255, 255, 224),
            "LEMONCHIFFON": (255, 250, 205),
            "LIGHTGOLDENRODYELLOW": (250, 250, 210),
            "PAPAYAWHIP": (255, 239, 213),
            "MOCCASIN": (255, 228, 181),
            "PEACHPUFF": (255, 218, 185),
            "PALEGOLDENROD": (238, 232, 170),
            "KHAKI": (240, 230, 140),
            "DARKKHAKI": (189, 183, 107),
            "LAVENDER": (230, 230, 250),
            "THISTLE": (216, 191, 216),
            "PLUM": (221, 160, 221),
            "VIOLET": (238, 130, 238),
            "ORCHID": (218, 112, 214),
            "FUCHSIA": (255, 0, 255),
            "MAGENTA": (255, 0, 255),
            "MEDIUMORCHID": (186, 85, 211),
            "MEDIUMPURPLE": (147, 112, 219),
            "REBECCAPURPLE": (102, 51, 153),
            "BLUEVIOLET": (138, 43, 226),
            "DARKVIOLET": (148, 0, 211),
            "DARKORCHID": (153, 50, 204),
            "DARKMAGENTA": (139, 0, 139),
            "PURPLE": (128, 0, 128),
            "INDIGO": (75, 0, 130),
            "SLATEBLUE": (106, 90, 205),
            "DARKSLATEBLUE": (72, 61, 139),
            "MEDIUMSLATEBLUE": (123, 104, 238),
            "GREENYELLOW": (173, 255, 47),
            "CHARTREUSE": (127, 255, 0),
            "LAWNGREEN": (124, 252, 0),
            "LIME": (0, 255, 0),
            "LIMEGREEN": (50, 205, 50),
            "PALEGREEN": (152, 251, 152),
            "LIGHTGREEN": (144, 238, 144),
            "MEDIUMSPRINGGREEN": (0, 250, 154),
            "SPRINGGREEN": (0, 255, 127),
            "MEDIUMSEAGREEN": (60, 179, 113),
            "SEAGREEN": (46, 139, 87),
            "FORESTGREEN": (34, 139, 34),
            "GREEN": (0, 128, 0),
            "DARKGREEN": (0, 100, 0),
            "YELLOWGREEN": (154, 205, 50),
            "OLIVEDRAB": (107, 142, 35),
            "OLIVE": (128, 128, 0),
            "DARKOLIVEGREEN": (85, 107, 47),
            "MEDIUMAQUAMARINE": (102, 205, 170),
            "DARKSEAGREEN": (143, 188, 139),
            "LIGHTSEAGREEN": (32, 178, 170),
            "DARKCYAN": (0, 139, 139),
            "TEAL": (0, 128, 128),
            "AQUA": (0, 255, 255),
            "CYAN": (0, 255, 255),
            "LIGHTCYAN": (224, 255, 255),
            "PALETURQUOISE": (175, 238, 238),
            "AQUAMARINE": (127, 255, 212),
            "TURQUOISE": (64, 224, 208),
            "MEDIUMTURQUOISE": (72, 209, 204),
            "DARKTURQUOISE": (0, 206, 209),
            "CADETBLUE": (95, 158, 160),
            "STEELBLUE": (70, 130, 180),
            "LIGHTSTEELBLUE": (176, 196, 222),
            "POWDERBLUE": (176, 224, 230),
            "LIGHTBLUE": (173, 216, 230),
            "SKYBLUE": (135, 206, 235),
            "LIGHTSKYBLUE": (135, 206, 250),
            "DEEPSKYBLUE": (0, 191, 255),
            "DODGERBLUE": (30, 144, 255),
            "CORNFLOWERBLUE": (100, 149, 237),
            "MEDIUMSLATEBLUE": (123, 104, 238),
            "ROYALBLUE": (65, 105, 225),
            "BLUE": (0, 0, 255),
            "MEDIUMBLUE": (0, 0, 205),
            "DARKBLUE": (0, 0, 139),
            "NAVY": (0, 0, 128),
            "MIDNIGHTBLUE": (25, 25, 112),
            "CORNSILK": (255, 248, 220),
            "BLANCHEDALMOND": (255, 235, 205),
            "BISQUE": (255, 228, 196),
            "NAVAJOWHITE": (255, 222, 173),
            "WHEAT": (245, 222, 179),
            "BURLYWOOD": (222, 184, 135),
            "TAN": (210, 180, 140),
            "ROSYBROWN": (188, 143, 143),
            "SANDYBROWN": (244, 164, 96),
            "GOLDENROD": (218, 165, 32),
            "DARKGOLDENROD": (184, 134, 11),
            "PERU": (205, 133, 63),
            "CHOCOLATE": (210, 105, 30),
            "SADDLEBROWN": (139, 69, 19),
            "SIENNA": (160, 82, 45),
            "BROWN": (165, 42, 42),
            "MAROON": (128, 0, 0),
            "WHITE": (255, 255, 255),
            "SNOW": (255, 250, 250),
            "HONEYDEW": (240, 255, 240),
            "MINTCREAM": (245, 255, 250),
            "AZURE": (240, 255, 255),
            "ALICEBLUE": (240, 248, 255),
            "GHOSTWHITE": (248, 248, 255),
            "WHITESMOKE": (245, 245, 245),
            "SEASHELL": (255, 245, 238),
            "BEIGE": (245, 245, 220),
            "OLDLACE": (253, 245, 230),
            "FLORALWHITE": (255, 250, 240),
            "IVORY": (255, 255, 240),
            "ANTIQUEWHITE": (250, 235, 215),
            "LINEN": (250, 240, 230),
            "LAVENDERBLUSH": (255, 240, 245),
            "MISTYROSE": (255, 228, 225),
            "GAINSBORO": (220, 220, 220),
            "LIGHTGRAY": (211, 211, 211),
            "SILVER": (192, 192, 192),
            "DARKGRAY": (169, 169, 169),
            "GRAY": (128, 128, 128),
            "DIMGRAY": (105, 105, 105),
            "LIGHTSLATEGRAY": (119, 136, 153),
            "SLATEGRAY": (112, 128, 144),
            "DARKSLATEGRAY": (47, 79, 79),
            "BLACK": (0, 0, 0)})
        # allocate memory for the L*a*b* image, then initialize
        # the color names list
        self.lab = np.zeros((len(colors), 1, 3), dtype="uint8")
        self.colorNames = []
        # loop over the colors dictionary
        for (i, (name, rgb)) in enumerate(colors.items()):
            # update the L*a*b* array and the color names list
            self.lab[i] = rgb
            self.colorNames.append(name)
        # convert the L*a*b* array from the RGB color space
        # to L*a*b*
        self.lab = cv2.cvtColor(self.lab, cv2.COLOR_RGB2LAB)

    def label(self, image, c):
        # construct a mask for the contour, then compute the
        # average L*a*b* value for the masked region
        mask = np.zeros(image.shape[:2], dtype="uint8")
        cv2.drawContours(mask, [c], -1, 255, -1)
        mask = cv2.erode(mask, None, iterations=2)
        mean = cv2.mean(image, mask=mask)[:3]
        # initialize the minimum distance found thus far
        minDist = (np.inf, None)
        # loop over the known L*a*b* color values
        for (i, row) in enumerate(self.lab):
            # compute the distance between the current L*a*b*
            # color value and the mean of the image
            d = dist.euclidean(row[0], mean)
            # if the distance is smaller than the current distance,
            # then update the bookkeeping variable
            if d < minDist[0]:
                minDist = (d, i)
        # return the name of the color with the smallest distance
        return self.colorNames[minDist[1]]


def colorDetect(image_path):

    # load the image and resize it to a smaller factor so that
    # the shapes can be approximated better
    image = cv2.imread(image_path)
    resized = imutils.resize(image, width=300)
    # blur the resized image slightly, then convert it to both
    # grayscale and the L*a*b* color spaces
    blurred = cv2.GaussianBlur(resized, (5, 5), 0)
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
    thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]
    # find contours in the thresholded image
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # initialize the shape detector and color labeler
    cl = ColorDetector()

    # loop over the contours
    for c in cnts:
        # detect the shape of the contour and label the color
        color = cl.label(lab, c)
        print(color)


colorDetect('test.jpeg')
