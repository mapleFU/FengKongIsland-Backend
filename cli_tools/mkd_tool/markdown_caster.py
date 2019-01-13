#!/usr/local/bin/python3

import argparse
import re
from concurrent import futures


from file_operations.filename_operations import filename_ext, file_exist, filename_without_ext, path_leaf
from qiniu_tools.QiniuUploader import upload
from file_cmd_parser import get_base_parser, exec_func


LINE_RE = "(?:!\[(.*?)\]\((.*?)\))"
line_regex = re.compile(LINE_RE)


def process_file(file_name: str) -> bool:
    """
    :param file_name: markdown file name
    :return:
    """
    print(f'filename: {file_name}')
    if not file_exist(file_name):
        raise FileNotFoundError(f"file {file_name} not exists in the system.")
    if not filename_ext(file_name) == '.md':
        raise Exception(f"file {file_name} is not a .md file.")
    # get path leaf
    file_name_without_path = filename_without_ext(path_leaf(file_name))
    new_text = ''
    cnt_line, image_cnt = 0, 0
    with open(file_name, encoding='utf-8', mode='r') as f:
        for line in f.readlines():
            cnt_line += 1
            match_result = line_regex.search(line)
            if match_result is not None:
                image_cnt += 1
                print(f"result: {match_result}, group: {match_result.group(2)}")

                image_link = match_result.group(2)
                print(f'image_link: {image_link}')
                if 'nmsl.maplewish.cn' not in image_link and 'http' not in image_link:
                    # new_file_name = f'blog:{file_name_without_path}:{path_leaf(image_link)}'
                    f_name = file_name.replace(' ', '-')
                    f_leaf = path_leaf(image_link).replace(' ', '-')
                    new_file_name = f'blog:{file_name}:{path_leaf(image_link)}'
                    upload(new_file_name, image_link)

                    line = line.replace(image_link, "https://nmsl.maplewish.cn/" + new_file_name)
            new_text = new_text + line
    print(f'the file has {cnt_line} lines, and {image_cnt} has image')
    with open(file_name, encoding='utf-8', mode='w') as fw:
        fw.write(new_text)
    print(f' {file_name} markdown 成功转化为 七牛链接')


if __name__ == '__main__':
    parser = get_base_parser()

    exec_func(parser, process_file)
