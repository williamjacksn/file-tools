#!/usr/bin/env python3

import argparse
import pathlib
import readline
import subprocess

GET_DATES_CMD = ['exiftool', '-AllDates', '-FileModifyDate', '-FileAccessDate', '-FileInodeChangeDate']


def print_dates(file):
    print(subprocess.check_output(GET_DATES_CMD + [str(file)], universal_newlines=True))


def set_dates(file, date):
    print(subprocess.check_output(['exiftool', '-overwrite_original', '-AllDates=' + date, str(file)],
                                  universal_newlines=True))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', nargs='?', default='.')
    args = parser.parse_args()
    d = pathlib.Path(args.dir).resolve()

    files = []
    for item in d.iterdir():
        if item.is_file() and item.suffix.lower() in ['.jpg']:
            files.append(item)

    files.sort()

    for file in files:
        print('***')
        print('*', file)
        print_dates(file)
        new_date = input('New date? ')
        if new_date:
            set_dates(file, new_date)


if __name__ == '__main__':
    main()
