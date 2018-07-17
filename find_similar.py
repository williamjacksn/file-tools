import json
import os
import pathlib
import pybktree
import typing


class Image(typing.NamedTuple):
    path: str
    dhash: int


def diff(x, y):
    return pybktree.hamming_distance(x.dhash, y.dhash)


def main():
    dhash_json = pathlib.Path(os.getcwd()).resolve() / 'dhash.json'
    dhash_tree = pybktree.BKTree(diff)
    with dhash_json.open() as f:
        data = json.load(f)
    for path, dhash in data.items():
        dhash_tree.add(Image(path, dhash))

    for image in dhash_tree:
        matches = dhash_tree.find(image, 5)
        if len(matches) > 1:
            print(image.path)
            for match in matches:
                print('{} {}'.format(match[0], match[1].path))
            input()

if __name__ == '__main__':
    main()
