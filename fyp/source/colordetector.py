from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np
import argparse
import imutils
import cv2


class ColorDetector:
    def __init__(self):
        # initialize the colors dictionary, containing the color
        # name as the key and the RGB tuple as the value
        colors = OrderedDict({
            "Indian Red": (205, 92, 92),
            "Light Coral": (240, 128, 128),
            "Salmon": (250, 128, 114),
            "Dark Salmon": (233, 150, 122),
            "Light Salmon": (255, 160, 122),
            "Crimson": (220, 20, 60),
            "Red": (255, 0, 0),
            "Firebrick ": (178, 34, 34),
            "Dark Red": (139, 0, 0),
            "Pink": (255, 192, 203),
            "Light Pink": (255, 182, 193),
            "Hot Pink": (255, 105, 180),
            "Deep Pink": (255, 20, 147),
            "Medium Violet Red": (199, 21, 133),
            "Pale Violet Red ": (219, 112, 147),
            "Coral": (255, 127, 80),
            "Tomato": (255, 99, 71),
            "Orange Red": (255, 69, 0),
            "Dark Orange": (255, 140, 0),
            "Orange": (255, 165, 0),
            "Gold": (255, 215, 0),
            "Yellow": (255, 255, 0),
            "Light Yellow": (255, 255, 224),
            "Lemon Chiffon": (255, 250, 205),
            "Light Goldenrod Yellow": (250, 250, 210),
            "Papayawhip ": (255, 239, 213),
            "Moccasin ": (255, 228, 181),
            "Peachpuff ": (255, 218, 185),
            "Pale Goldenrod": (238, 232, 170),
            "Khaki ": (240, 230, 140),
            "Dark Khaki ": (189, 183, 107),
            "Lavender": (230, 230, 250),
            "Thistle ": (216, 191, 216),
            "Plum ": (221, 160, 221),
            "Violet": (238, 130, 238),
            "Orchids": (218, 112, 214),
            "Fuchsia": (255, 0, 255),
            "Magenta": (255, 0, 255),
            "Medium Orchid": (186, 85, 211),
            "Medium Purple": (147, 112, 219),
            "Rebeccapurple": (102, 51, 153),
            "Blue Violet": (138, 43, 226),
            "Dark Violet": (148, 0, 211),
            "Dark Orchid": (153, 50, 204),
            "Dark Magenta": (139, 0, 139),
            "Purple": (128, 0, 128),
            "Indigo ": (75, 0, 130),
            "Slate Blue": (106, 90, 205),
            "Dark Slate Blue": (72, 61, 139),
            "Medium Slate Blue": (123, 104, 238),
            "Green Yellow": (173, 255, 47),
            "Chartreuse": (127, 255, 0),
            "Lawn Green": (124, 252, 0),
            "Lime": (0, 255, 0),
            "Lime Green": (50, 205, 50),
            "Pale Green": (152, 251, 152),
            "Light Green": (144, 238, 144),
            "Medium Spring Green": (0, 250, 154),
            "Spring Green": (0, 255, 127),
            "Medium Sea Green": (60, 179, 113),
            "Sea Green": (46, 139, 87),
            "Forest Green": (34, 139, 34),
            "Green": (0, 128, 0),
            "Dark Green": (0, 100, 0),
            "Yellow Green": (154, 205, 50),
            "Olive Drab": (107, 142, 35),
            "Olive": (128, 128, 0),
            "Darkolive Green": (85, 107, 47),
            "Medium Aquamarine": (102, 205, 170),
            "Dark Sea Green": (143, 188, 139),
            "Light Sea Green": (32, 178, 170),
            "Dark Cyan": (0, 139, 139),
            "Teal": (0, 128, 128),
            "Aqua": (0, 255, 255),
            "Cyan": (0, 255, 255),
            "Light Cyan": (224, 255, 255),
            "Pale Turquoise": (175, 238, 238),
            "Aquamarine": (127, 255, 212),
            "Turquoise": (64, 224, 208),
            "Medium Turquoise": (72, 209, 204),
            "Dark Turquoise": (0, 206, 209),
            "Cadet Blue": (95, 158, 160),
            "Steel Blue": (70, 130, 180),
            "Lightsteel Blue": (176, 196, 222),
            "Powder Blue": (176, 224, 230),
            "Light Blue": (173, 216, 230),
            "Sky Blue": (135, 206, 235),
            "Lightsky Blue": (135, 206, 250),
            "Deepsky Blue": (0, 191, 255),
            "Dodger Blue": (30, 144, 255),
            "Cornflower Blue": (100, 149, 237),
            "Mediumslate Blue": (123, 104, 238),
            "Royal Blue": (65, 105, 225),
            "Blue": (0, 0, 255),
            "Medium Blue": (0, 0, 205),
            "Dark Blue": (0, 0, 139),
            "Navy": (0, 0, 128),
            "Midnight Blue": (25, 25, 112),
            "Cornsilk": (255, 248, 220),
            "Blanched Almond": (255, 235, 205),
            "Bisque": (255, 228, 196),
            "Navajo White": (255, 222, 173),
            "Wheat": (245, 222, 179),
            "Burly Wood": (222, 184, 135),
            "Tan": (210, 180, 140),
            "Rosy Brown": (188, 143, 143),
            "Sandy Brown": (244, 164, 96),
            "Goldenrod": (218, 165, 32),
            "Dark Goldenrod": (184, 134, 11),
            "Peru": (205, 133, 63),
            "Chocolate": (210, 105, 30),
            "Saddle Brown": (139, 69, 19),
            "Sienna": (160, 82, 45),
            "Brown": (165, 42, 42),
            "Maroon": (128, 0, 0),
            "White": (255, 255, 255),
            "Snow": (255, 250, 250),
            "Honeydew": (240, 255, 240),
            "Mint Cream": (245, 255, 250),
            "Azure": (240, 255, 255),
            "Alice Blue": (240, 248, 255),
            "Ghost White": (248, 248, 255),
            "White Smoke": (245, 245, 245),
            "Seashell": (255, 245, 238),
            "Beige": (245, 245, 220),
            "Old Lace": (253, 245, 230),
            "Floral White": (255, 250, 240),
            "Ivory": (255, 255, 240),
            "Antique White": (250, 235, 215),
            "Linen": (250, 240, 230),
            "Lavender Blush": (255, 240, 245),
            "Misty Rose": (255, 228, 225),
            "Gainsboro": (220, 220, 220),
            "Light Gray": (211, 211, 211),
            "Silver": (192, 192, 192),
            "Dark Gray": (169, 169, 169),
            "Gray": (128, 128, 128),
            "Dim Gray": (105, 105, 105),
            "Light Slate Gray": (119, 136, 153),
            "Slate Gray": (112, 128, 144),
            "Dark Slate Gray": (47, 79, 79),
            "Black": (0, 0, 0)
        })
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

    def label(self, image, c, n=5):
        # construct a mask for the contour, then compute the
        # average L*a*b* value for the masked region
        mask = np.zeros(image.shape[:2], dtype="uint8")
        cv2.drawContours(mask, [c], -1, 255, -1)
        mask = cv2.erode(mask, None, iterations=2)
        mean = cv2.mean(image, mask=mask)[:3]

        # initialize the minimum distance found thus far
        minDistList = []
        minDist = (np.inf, None)

        # loop over the known L*a*b* color values
        for (i, row) in enumerate(self.lab):
            # compute the distance between the current L*a*b*
            # color value and the mean of the image
            d = dist.euclidean(row[0], mean)
            minDistList.append((d, i))
            # if the distance is smaller than the current distance,
            # then update the bookkeeping variable
            if d < minDist[0]:
                minDist = (d, i)

        # sort by distance in ascending order
        minDistList.sort(key=lambda x: int(x[0]))
        # return the name of the color with the smallest distance for first n elements
        return [self.colorNames[i[1]] for i in minDistList[:n]]


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
