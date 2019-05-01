import argparse
import os

import cv2
from hurry.filesize import size


def main():
    parser = argparse.ArgumentParser(description="test")
    parser.add_argument("--path", "-p", type=str, help="path to dir with .png")
    parser.add_argument("--video", "-v", type=str, help="path to video (.avi)")
    args = parser.parse_args()
    make_vid(images_path=args.path, video_name=args.video)


def rescaled_dim(img, scale_percent=30):
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    return dim


def get_image_filepaths(images_path):
    files = []
    print("Looking through " + images_path + " for '.png'")
    for root, directories, files in os.walk(images_path):
        for file in files:
            print(file)
            if ".png" in file:
                image_path = os.path.join(root, file)
                files.append(image_path)
    return files


def make_vid(images_path, video_name):
    image_filepaths = get_image_filepaths(images_path)
    print("Number of images: " + str(len(image_filepaths)))
    if image_filepaths:
        img = cv2.imread(image_filepaths[0], 0)
        new_dim = rescaled_dim(img, scale_percent=30)
        print("Orig size: (" + img.shape[1] + ", " + img.shape[0] + ")")
        print("New size: (" + img.shape[1] + ", " + img.shape[0] + ")")

        video = cv2.VideoWriter(
            filename=video_name, fourcc=0, fps=10, frameSize=new_dim
        )

        for image_filepath in image_filepaths:
            image = cv2.imread(image_filepath, 0)
            rescaled_image = cv2.resize(image, new_dim, interpolation=cv2.INTER_AREA)
            video.write(rescaled_image)

        mem_size = size(os.path.getsize(video_name))
        print("Video filesize: " + mem_size)
        video.release()


if __name__ == "__main__":
    main()
