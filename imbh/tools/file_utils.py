#!/usr/bin/env python3
import os


def get_filepaths(images_path, file_ending="_result.json"):
    files_paths = []
    for root, directories, files in os.walk(images_path):
        for file in files:
            if file.endswith(file_ending):
                files_paths.append(os.path.join(root, file))
    if len(files_paths) == 0:
        print("WARNING: 0 files with ending {} found".format(file_ending))
    return files_paths


class IncorrectFileType(Exception):
    pass
