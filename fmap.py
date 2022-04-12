#!/bin/python3
import argparse
from os import path

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('pid', help='(PID) Process ID to print maps for', type=int)
    return parser.parse_args()

def get_proc_maps(pid: int): 
    with open(f'/proc/{pid}/maps') as f:
        return [l.split() for l in f.readlines()]

def filter_out_not_files(map_line):
    return len(map_line) > 5 and path.isfile(map_line[5])

def main():
    args = parse_args()
    maps = get_proc_maps(args.pid)
    file_maps = filter(filter_out_not_files, maps)
    for fm in file_maps:
        print(*fm)

if __name__ == '__main__':
    main()
