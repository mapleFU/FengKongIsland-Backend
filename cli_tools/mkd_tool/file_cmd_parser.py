import argparse
from concurrent import futures
from pathlib import Path
import os

from dotenv import load_dotenv

from file_operations.filename_operations import filename_ext, dir_path


def load_all_env():
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)


load_all_env()


def get_base_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Process some markdown files')

    parser.add_argument('files', metavar='N', type=str, nargs='+',
                        help='input the files in the list')

    return parser


def parse_files_from_list(files, direc=''):
    f_list = []

    for file_path in files:
        file_path = direc + file_path
        if not os.path.exists(file_path):
            print(f"file {file_path} not exists in the system.")
            continue
        if os.path.isdir(file_path):
            f_list.extend(parse_files_from_list(os.listdir(file_path), direc=file_path + '/'))
            continue
        elif not filename_ext(file_path) == '.md':
            print(f"file {file_path} is not a .md file.")
            continue
        f_list.append(file_path)
    return f_list


def exec_func(cmd_parser: argparse.ArgumentParser, task_func):
    """
    执行任务，在线程池中 处理任务的执行

    :param cmd_parser: 任务的 parser 对象
    :param task_func: 需要执行的任务函数
    :param need_field: 需要的字段
    :return:
    """
    args = cmd_parser.parse_args()
    with futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Start the load operations and mark each future with its URL
        future_to_url = {executor.submit(task_func, file_name): file_name for file_name in parse_files_from_list(args.files)}
        for future in futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception:\n %s' % (url, exc))
            else:
                print(f"Down with {future}")
