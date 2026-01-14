import pathlib


def main():
    directory = pathlib.Path().resolve()
    for item in directory.iterdir():
        if item.suffix == ".HEIC":
            item.with_suffix(".MP4").unlink(missing_ok=True)


if __name__ == "__main__":
    main()
