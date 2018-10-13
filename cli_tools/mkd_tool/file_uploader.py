#!/usr/local/bin/ python3

import os
import json

from file_cmd_parser import get_base_parser, exec_func
from file_operations.filename_operations import file_exist, filename_ext, path_leaf, filename_without_ext
from markdown_caster import process_file

import requests
import markdown2

remote_url = 'http://maplewish.cn:8000/api/v1/posts/'

# META_RE = re.compile(r'^[ ]{0,3}(?P<key>[A-Za-z0-9_-]+):\s*(?P<value>.*)')


def upload_file(file_path: str):
    print(f'filename: {file_path}')
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"file {file_path} not exists in the system.")
    if not filename_ext(file_path) == '.md':
        raise Exception(f"file {file_path} is not a .md file.")

    token = os.environ.get('token')
    print(f"sending {file_path}")
    file_content = ''
    with open(file_path, 'r', encoding='utf-8') as f:
        file_content = f.read()

    title = filename_without_ext(path_leaf(file_path))

    meta = markdown2.markdown(file_content, extras=['metadata']).metadata
    post_data = {
        'title': meta['title'],
        'content': file_content,
        'tags': meta['tags'].split(' '),
    }
    if 'date' in meta:
        post_data['created_time'] = meta['date']
    elif 'abstract' in meta:
        post_data['abstract'] = meta['abstract']
    else:
        post_data['abstract'] = ''
    result = requests.post(remote_url, data=json.dumps(post_data), headers={
        'Authorization': f'token {token}',
        'Content-Type': 'application/json'
    })
    print(f'upload {title} done: {result}')


if __name__ == '__main__':
    parser = get_base_parser()

    exec_func(parser, process_file)
    exec_func(parser, upload_file)
