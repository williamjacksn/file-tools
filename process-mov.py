import argparse
import datetime
import pathlib
import subprocess


class Args:
    file: list[pathlib.Path]


def parse_args() -> Args:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="+", type=pathlib.Path)
    return parser.parse_args(namespace=Args())


def main() -> None:
    args = parse_args()
    total = len(args.file)
    for i, f in enumerate(args.file, start=1):
        print(f"* {f} ({i} of {total})")
        cmd: list[str | pathlib.Path] = [
            "ffprobe",
            "-v",
            "quiet",
            "-show_entries",
            "format_tags=com.apple.quicktime.creationdate",
            f,
        ]
        ffprobe_result = subprocess.run(args=cmd, capture_output=True, text=True)
        for line in ffprobe_result.stdout.splitlines():
            if line.startswith("TAG"):
                creation_date = datetime.datetime.fromisoformat(line.split("=")[1])
                target_base = creation_date.strftime("%Y%m%d_%H%M%S")
                target = pathlib.Path(f"{target_base}{f.suffix.lower()}")
                suffix = 0
                while target.exists():
                    suffix += 1
                    target = pathlib.Path(f"{target_base}_{suffix}{f.suffix.lower()}")
                print(f"  -> {target}")
                f.rename(target)


if __name__ == "__main__":
    main()
