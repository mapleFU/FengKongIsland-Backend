#!/usr/local/bin/python3

import argparse
from concurrent import futures


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some markdown files')

    parser.add_argument('files', metavar='N', type=str, nargs='+',
                        help='input the ')

    args = parser.parse_args()

    with futures.ThreadPoolExecutor(max_workers=5) as executor:
        pass

