import argparse
import pathlib
from collections.abc import Iterator


class Args:
    ext: str


def parse_args() -> Args:
    parser = argparse.ArgumentParser()
    parser.add_argument("ext")
    return parser.parse_args(namespace=Args())


def yield_items(p: pathlib.Path) -> Iterator[pathlib.Path]:
    for item in p.iterdir():
        if item.is_dir():
            yield from yield_items(item)
        else:
            yield item


args = parse_args()
pwd = pathlib.Path()

for item in yield_items(pwd):
    if item.suffix.lower() == args.ext.lower():
        print(item)
        break
