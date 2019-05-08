#!/usr/local/bin/ python3

import os
import json

from file_cmd_parser import get_base_parser, exec_func
from markdown_caster import process_file
from markdown_post import markdown_post

import requests


remote_url = 'http://maplewish.cn:8100/api/v1/posts/'

# META_RE = re.compile(r'^[ ]{0,3}(?P<key>[A-Za-z0-9_-]+):\s*(?P<value>.*)')


def upload_file(file_path: str):
    print(f'filename: {file_path}')
    token = os.environ.get('token')
    post_data = markdown_post(file_path)
    print(post_data['created_time'])
    result = requests.post(remote_url, data=json.dumps(post_data), headers={
        'Authorization': f'token {token}',
        'Content-Type': 'application/json'
    })
    print(f'upload done: {result}')
    print(result.content)


if __name__ == '__main__':
    parser = get_base_parser()

    exec_func(parser, process_file)
    exec_func(parser, upload_file)
