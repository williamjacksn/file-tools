import argparse
import hashlib
import pathlib


def yield_files(paths):
    if not isinstance(paths, list):
        paths = [paths]
    for path in paths:
        if isinstance(path, pathlib.Path):
            p = path.resolve()
        else:
            p = pathlib.Path(path).resolve()
        if p.is_dir():
            for item in p.iterdir():
                if item.is_file():
                    yield item
        else:
            yield p


def get_hash(file_path, buffer_size=65536):
    with file_path.open(mode="rb") as f:
        hasher = hashlib.md5()
        buffer = f.read(buffer_size)
        while len(buffer) > 0:
            hasher.update(buffer)
            buffer = f.read(buffer_size)
        return hasher.hexdigest()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="+")
    return parser.parse_args()


def main():
    args = parse_args()
    for file in yield_files(args.path):
        file_hash = get_hash(file)
        file.rename(file.with_name(file_hash).with_suffix(file.suffix.lower()))


if __name__ == "__main__":
    main()
