import argparse
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
            "exiftool",
            "-datetimeoriginal",
            "-csv",
            "-d",
            "%Y%m%d_%H%M%S",
            f,
        ]
        exiftool_result = subprocess.run(args=cmd, capture_output=True, text=True)
        for line in exiftool_result.stdout.splitlines():
            if line.startswith(f.name):
                dto = line.split(",")[1]
                target = pathlib.Path(f"{dto}.jpg")
                suffix = 0
                while target.exists():
                    suffix += 1
                    target = pathlib.Path(f"{dto}_{suffix}.jpg")
                else:
                    cmd = ["gm", "convert", f, target]
                    print(f"  -> {target}")
                    subprocess.call(args=cmd)
                    f.unlink()


if __name__ == "__main__":
    main()
