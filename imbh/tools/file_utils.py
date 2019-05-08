#!/usr/bin/env python3
import os
import re


def get_filepaths(root_path: str, file_regex: str):
    files_paths = []
    pattern = re.compile(file_regex)
    for root, directories, files in os.walk(root_path):
        for file in files:
            if pattern.match(file):
                files_paths.append(os.path.join(root, file))
    if len(files_paths) == 0:
        print("WARNING: 0 files with regex {} found".format(file_regex))
    return files_paths


class IncorrectFileType(Exception):
    pass
