import argparse
import json
import pathlib
import readline
import subprocess


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+")
    return parser.parse_args()


def get_date(pathname):
    cmd = [
        "exiftool",
        "-json",
        "-datetimeoriginal",
        str(pathname),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = json.loads(result.stdout)
    return output[0].get("DateTimeOriginal")


def set_date(pathname, new_date):
    cmd = [
        "exiftool",
        f'-datetimeoriginal="{new_date}"',
        str(pathname),
    ]
    print(f"running: {cmd}")
    subprocess.run(cmd)


def main():
    args = parse_args()
    for filename in args.files:
        pathname = pathlib.Path(filename).resolve()
        existing_date = get_date(pathname)
        if existing_date:
            print(f"{pathname} has date {existing_date}")
            continue
        new_date = input(f"{pathname} > ")
        set_date(pathname, new_date)


if __name__ == "__main__":
    main()
