#! /usr/bin/python3
from PIL import Image, ImageFilter
import math, subprocess, cv2, numpy as np

# Black and White function
def black_and_white(image, uid):
    img = Image.open(image).convert('LA')
    img.save('{}_effect.png'.format(uid))

def gaussian_blur(image, uid):
    img = Image.open(image)
    img = img.filter(ImageFilter.GaussianBlur(radius=3))
    img.save('{}_effect.png'.format(uid))

def sobel_filter(image, uid):
    img = Image.open(image)
    width, height = img.size
    newimg = Image.new("RGB", (width, height), "white")
    for x in range(1, width-1):  # ignore the edge pixels for simplicity (1 to width-1)
        for y in range(1, height-1): # ignore edge pixels for simplicity (1 to height-1)

            # initialise Gx to 0 and Gy to 0 for every pixel
            Gx = 0
            Gy = 0

            # top left pixel
            p = img.getpixel((x-1, y-1))
            r = p[0]
            g = p[1]
            b = p[2]

            # intensity ranges from 0 to 765 (255 * 3)
            intensity = r + g + b

            # accumulate the value into Gx, and Gy
            Gx += -intensity
            Gy += -intensity

            # remaining left column
            p = img.getpixel((x-1, y))
            r = p[0]
            g = p[1]
            b = p[2]

            Gx += -2 * (r + g + b)

            p = img.getpixel((x-1, y+1))
            r = p[0]
            g = p[1]
            b = p[2]

            Gx += -(r + g + b)
            Gy += (r + g + b)

            # middle pixels
            p = img.getpixel((x, y-1))
            r = p[0]
            g = p[1]
            b = p[2]

            Gy += -2 * (r + g + b)

            p = img.getpixel((x, y+1))
            r = p[0]
            g = p[1]
            b = p[2]

            Gy += 2 * (r + g + b)

            # right column
            p = img.getpixel((x+1, y-1))
            r = p[0]
            g = p[1]
            b = p[2]

            Gx += (r + g + b)
            Gy += -(r + g + b)

            p = img.getpixel((x+1, y))
            r = p[0]
            g = p[1]
            b = p[2]

            Gx += 2 * (r + g + b)

            p = img.getpixel((x+1, y+1))
            r = p[0]
            g = p[1]
            b = p[2]

            Gx += (r + g + b)
            Gy += (r + g + b)

            # calculate the length of the gradient (Pythagorean theorem)
            length = math.sqrt((Gx * Gx) + (Gy * Gy))

            # normalise the length of gradient to the range 0 to 255
            length = length / 4328 * 255

            length = int(length)

            # draw the length in the edge image
            #newpixel = img.putpixel((length,length,length))
            newimg.putpixel((x,y),(length,length,length))
    newimg.save('{}_effect.png'.format(uid))

def cartoon_effect(image, uid):
    img = cv2.imread('{}'.format(image))

    # 1) Edges
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

    # 2) Color
    color = cv2.bilateralFilter(img, 9, 300, 300)

    # 3) Cartoon
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    cv2.imwrite('{}_effect.png'.format(uid), cartoon)

def edges_effect(image, uid):
    img = cv2.imread('{}'.format(image))

    # 1) Edges
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

    # 2) Color
    color = cv2.bilateralFilter(img, 9, 300, 300)

    # 3) Cartoon
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    cv2.imwrite('{}_effect.png'.format(uid), edges)
