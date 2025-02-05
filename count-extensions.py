import collections
import pathlib


def main():
    counter = collections.Counter()
    dirs = [pathlib.Path()]
    while dirs:
        dir = dirs.pop()
        for item in dir.iterdir():
            if item.is_dir():
                dirs.append(item)
            elif item.is_file() and item.suffix:
                counter.update([item.suffix.lower()])
    for ext, count in counter.most_common():
        print(count, ext)


if __name__ == '__main__':
    main()
