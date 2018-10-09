#!/usr/local/bin/python3

import argparse
import os
import re
import ntpath
from concurrent import futures

from QiniuUploader import upload

parser = argparse.ArgumentParser(description='Process some markdown files')

parser.add_argument('files', metavar='N', type=str, nargs='+',
                    help='input the ')

LINE_RE = "(?:!\[(.*?)\]\((.*?)\))"
line_regex = re.compile(LINE_RE)


def path_leaf(path: str)->str:
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def filename_without_ext(path: str)-> str:
    return os.path.splitext(path)[0]


def filename_ext(path: str) -> str:
    return os.path.splitext(path)[1]


def process_file(file_name: str) -> bool:
    """
    :param file_name: markdown file name
    :return:
    """
    print(f'filename: {file_name}')
    if not os.path.isfile(file_name):
        raise FileNotFoundError(f"file {file_name} not exists in the system.")
    if not filename_ext(file_name) == 'md':
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
                    new_file_name = f'blog:{file_name}:{path_leaf(image_link)}'
                    upload(new_file_name, image_link)

                    line = line.replace(image_link, "https://nmsl.maplewish.cn/" + new_file_name)
            new_text = new_text + line
    print(f'the file has {cnt_line} lines, and {image_cnt} has image')
    with open(file_name, encoding='utf-8', mode='w') as fw:
        fw.write(new_text)


if __name__ == '__main__':
    args = parser.parse_args()

    with futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Start the load operations and mark each future with its URL
        future_to_url = {executor.submit(process_file, file_name): file_name for file_name in args.files}
        for future in futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))
            else:
                print('%r page is %d bytes' % (url, len(data)))
