import argparse
import pathlib
import subprocess
import datetime


class Args:
    file: pathlib.Path


def parse_args() -> Args:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=pathlib.Path)
    return parser.parse_args(namespace=Args())


def main():
    args = parse_args()
    cmd: list[str | pathlib.Path] = [
        "ffprobe",
        "-v",
        "quiet",
        "-show_entries",
        "format_tags=com.apple.quicktime.creationdate",
        args.file,
    ]
    ffprobe_result = subprocess.run(cmd, capture_output=True, text=True)
    for line in ffprobe_result.stdout.splitlines():
        if line.startswith("TAG"):
            creation_date = datetime.datetime.fromisoformat(line.split("=")[1])
            target = f"{creation_date:%Y%m%d_%H%M%S}{args.file.suffix.lower()}"
            print(f"{args.file} -> {target}")
            args.file.rename(target)


if __name__ == "__main__":
    main()
