import pathlib


def main() -> None:
    directory = pathlib.Path()
    for item in directory.iterdir():
        if item.suffix == ".HEIC":
            live_photo = item.with_suffix(".MP4")
            if live_photo.exists():
                print(f"Removing {live_photo}")
                live_photo.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
