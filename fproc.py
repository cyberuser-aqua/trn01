#!/bin/python3
import argparse
from os import listdir, path, stat
from pathlib import PosixPath
from stat import S_IREAD, S_IWRITE
from typing import List, Generator, Literal


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'path', help='list PIDs that have opened the file at this path', type=PosixPath)
    return parser.parse_args()


def enumerate_pids() -> Generator[int, None, None]:
    return map(int, filter(lambda x: x.isdigit(), listdir('/proc')))


def enumerate_fds(pid: int) -> Generator[str, None, None]:
    return map(lambda x: f'/proc/{pid}/fd/{x}', listdir(f'/proc/{pid}/fd'))


def has_file_open(pid: int, fpath: PosixPath) -> bool:
    for fd in enumerate_fds(pid):
        if path.realpath(fd) == str(fpath.absolute()):
            return True
    return False


def get_file_attrs(pid: int, fpath: PosixPath) -> Literal['--', 'r-', '-w', 'rw']:
    read, write = False, False
    for fd in enumerate_fds(pid):
        if path.realpath(fd) == str(fpath.absolute()):
            prem = stat(fd, follow_symlinks=False).st_mode & 0o777
            read |= prem & S_IREAD == S_IREAD
            write |= prem & S_IWRITE == S_IWRITE
            if read and write:
                return 'rw'
    return (read and 'r' or '-') + (write and 'w' or '-')


def main():
    args = parse_args()
    try:
        result = {f'{pid} {get_file_attrs(pid, args.path)}'
                  for pid in enumerate_pids()
                  if has_file_open(pid, args.path)}
    except PermissionError:
        print('Run me with super-user premissions')
        exit(1)
    print(*result, sep='\n')


if __name__ == '__main__':
    main()
