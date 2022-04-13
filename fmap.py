#!/bin/python3
import argparse
from os import path
from typing import List


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'pid', help='(PID) Process ID to print maps for', type=int)
    return parser.parse_args()


def get_proc_maps(pid: int) -> List[List[str]]:
    with open(f'/proc/{pid}/maps') as f:
        return [l.split() for l in f.readlines()]


def filter_out_not_files(map_line) -> bool:
    return len(map_line) > 5 and path.isfile(map_line[5])


def main():
    args = parse_args()
    try:
        maps = get_proc_maps(args.pid)
        file_maps = filter(filter_out_not_files, maps)
    except PermissionError:
        print('Run me with super-user premissions')
        exit(1)
    for fm in file_maps:
        print(*fm)


if __name__ == '__main__':
    main()
