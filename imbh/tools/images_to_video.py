#!/usr/bin/env python3
import os

import cv2
from hurry.filesize import size
from tools.file_utils import get_filepaths


def rescaled_dim(img, scale_percent=30):
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    return dim


def make_vid(images_path, video_name):
    image_filepaths = get_filepaths(images_path, file_ending=".png")
    print("Number of images: " + str(len(image_filepaths)))
    if image_filepaths:
        img = cv2.imread(image_filepaths[0], 0)
        new_dim = rescaled_dim(img, scale_percent=10)
        print("Orig size: (" + str(img.shape[1]) + ", " + str(img.shape[0]) + ")")
        print("New size: (" + str(new_dim[1]) + ", " + str(new_dim[0]) + ")")

        video = cv2.VideoWriter(filename=video_name, fourcc=0, fps=1, frameSize=new_dim)

        for image_filepath in image_filepaths:
            image = cv2.imread(image_filepath, 0)
            rescaled_image = cv2.resize(image, new_dim, interpolation=cv2.INTER_AREA)
            video.write(rescaled_image)

        mem_size = size(os.path.getsize(video_name))
        print("Video filesize: " + mem_size)
        video.release()
