#!/bin/python3
import argparse
from os import path, listdir, stat
from pathlib import PosixPath
from stat import S_IREAD, S_IWRITE

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='list PIDs that have opened the file at this path', type=PosixPath)
    return parser.parse_args()

def enumerate_pids() -> int:
    return map(int, filter(lambda x: x.isdigit(), listdir('/proc')))

def enumerate_files(pid):
    return map(lambda x: f'/proc/{pid}/fd/{x}', listdir(f'/proc/{pid}/fd'))

def has_file_open(pid, fpath: PosixPath): 
    for f in listdir(f'/proc/{pid}/fd'):
        if path.realpath(f'/proc/{pid}/fd/{f}') == str(fpath.absolute()):
            return True
    return False
        

def get_file_attrs(pid, fpath: PosixPath): 
    read, write = False, False
    for f_path in enumerate_files(pid):
        if path.realpath(f_path) == str(fpath.absolute()):
            prem = stat(f_path, follow_symlinks=False).st_mode & 0o777
            read |= prem & S_IREAD == S_IREAD
            write |= prem & S_IWRITE == S_IWRITE
        if read and write:
            return 'rw'
    return (read and 'r' or '-') + (write and 'w' or '-')

def main():
    args = parse_args()
    result = {f'{pid} {get_file_attrs(pid, args.path)}' 
              for pid in enumerate_pids() 
              if has_file_open(pid, args.path)}
    print(*result)



if __name__ == '__main__':
    main()