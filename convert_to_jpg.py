import argparse
import pathlib
import subprocess


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='+')
    return parser.parse_args()


def convert_to_jpg(source_path):
    target_path = source_path.with_suffix('.jpg')
    cmd = [
        '/usr/bin/magick',
        str(source_path),
        str(target_path)
    ]
    subprocess.call(cmd)


def main():
    args = parse_args()
    total = len(args.files)
    for i, filename in enumerate(args.files, start=1):
        source_path = pathlib.Path(filename).resolve()
        print(f'Processing {source_path} ({i} of {total})')
        convert_to_jpg(source_path)


if __name__ == '__main__':
    main()
