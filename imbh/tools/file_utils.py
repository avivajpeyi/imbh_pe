#!/usr/bin/env python3
import logging
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
        logging.warning(
            "0 files with regex {} found in '{}' ".format(file_regex, root_path)
        )
    else:
        logging.info(f"{len(files_paths)} files with regex {file_regex} found")

    return files_paths


def filter_list(lst, filter_regex: str):
    selected_files = list(filter(re.compile(filter_regex).search, lst))
    if not selected_files:
        logging.warning(
            "0 files with regex {} found in '{}' ".format(filter_regex, lst)
        )
    else:
        logging.info(
            f"{len(selected_files)}/{len(lst)} files selected "
            f"using regex {filter_regex}"
        )
    return selected_files


class IncorrectFileType(Exception):
    pass
