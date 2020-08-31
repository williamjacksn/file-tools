import pathlib


def main():
    directory = pathlib.Path().resolve()
    for item in directory.iterdir():
        if item.suffix == '.jpg':
            item.with_suffix('.mov').unlink(missing_ok=True)


if __name__ == '__main__':
    main()
