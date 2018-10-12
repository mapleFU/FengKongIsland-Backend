import os
import ntpath


def path_leaf(path: str)->str:
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def filename_without_ext(path: str)-> str:
    return os.path.splitext(path)[0]


def filename_ext(path: str) -> str:
    return os.path.splitext(path)[1]


def file_exist(path: str) -> str:
    os.path.isfile(path)