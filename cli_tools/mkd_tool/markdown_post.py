import os
import re
from concurrent import futures

import markdown2

from file_operations.filename_operations import filename_ext, file_exist, filename_without_ext, path_leaf


RE = re.compile(r'---(.|\n)*?---')


def markdown_post(file_path: str):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"file {file_path} not exists in the system.")
    if not filename_ext(file_path) == '.md':
        raise Exception(f"file {file_path} is not a .md file.")
    print(f"sending {file_path}")
    file_content = ''
    with open(file_path, 'r', encoding='utf-8') as f:
        file_content = f.read()

    title = filename_without_ext(path_leaf(file_path))
    mkd = markdown2.markdown(file_content, extras=['metadata'])
    meta = mkd.metadata
    # print(RE.sub('', file_content))
    # print(file_content)
    post_data = {
        'title': meta['title'],
        'content': RE.sub('', file_content),
        'tags': meta['tags'].split(' '),
    }

    if 'date' in meta:
        post_data['created_time'] = meta['date']
    elif 'abstract' in meta:
        post_data['abstract'] = meta['abstract']
    else:
        post_data['abstract'] = ''
    return post_data


if __name__ == '__main__':
    print(markdown_post('/Users/fuasahi/Desktop/nothing/blog/source/_posts/操作系统-进程的空间虚拟化0.md'))
