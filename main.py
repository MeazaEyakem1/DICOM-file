# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import argparse

import matplotlib.pyplot as plt
from pydicom import dcmread
import pylibjpeg
import getopt
import sys
import matplotlib.pyplot as plt
from pydicom import dcmread
from pydicom.data import get_testdata_file
import os
import glob
import numpy as np


def dcmviewer():

    argv = sys.argv[1:]

    if len(argv) == 0:
        print("Error: there are no arguments specified")
        return

    try:
        opts, args = getopt.getopt(argv, "i:d:l:h:o:b:c:")
    except:
        print("Error")

    for opt, arg in opts:
        if opt in ['-i']:
            file = arg
        elif opt in ['-d']:
            d = arg
        elif opt in ["-l"]:
            l = arg
        elif opt in ['-h']:
            h = arg
        elif opt in ['-o']:
            o = arg
        elif opt in ['-b']:
            b = arg
        elif opt in ['-c']:
            c = arg

    try:
        f = dcmread(file)
        height = f.Rows
        width = f.Columns
        bits_stored = f.BitsStored
        #samples_per_pixel = f.SamplesperPixel
    except FileNotFoundError as fnf:
        print("the path you specified were not found")
        print("\n{}",fnf)
        exit()
    except ModuleNotFoundError as mnf:
        print("module name {} is not found".format(ModuleNotFoundError.name))
        exit()

    arr = f.pixel_array
    if argv.count("-l") > 0:
        low_thresh = int(l)
        arr[arr < low_thresh] = low_thresh

    if argv.count("-h") > 0:
        high_thresh = int(h)
        arr[arr > high_thresh] = high_thresh
    if argv.count("-d") > 0:

        #print the extracted information when argument d is given
        print(f"window height ...:{height}")
        print(f"window width..:{width}")
        print(f"Bits stored: {bits_stored}")
       # print(f"Samples per pixel: {samples_per_pixel}")
    if argv.count("-o") == 0:

        # plot the image using matplotlib
        plt.imshow(arr, cmap=plt.cm.gray)

        #save the image
        plt.savefig('image.png')
        plt.show()

        if argv.count("d") > 0:
            print(f"the minimam and maximam values of the window:{arr.min()}")
            print(f"the minimam and maximam values of the window:{arr.max()}")

    image = arr
    image = image / (image.max() / 255)

    mean_value = np.mean(image)
    centered_value = image - mean_value
    print(type(centered_value))
    print(type(c))
    new_centered_value = centered_value * int(c)
    new_value = new_centered_value + mean_value
    new_value = np.clip(new_value, 0, 255)
    plt.imshow(new_value, cmap=plt.cm.gray)
    plt.title("contrasted image")
    plt.savefig('contrasted_image.png')
    plt.show()

    brightened_image = image + int(b)
    brightened_image = np.clip(brightened_image, 0, 255)

    plt.imshow(brightened_image, cmap=plt.cm.gray)
    plt.title("brightened image image")
    plt.savefig('b_image.png')
    plt.show()

dcmviewer()



