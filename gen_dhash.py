import PIL.Image
import concurrent.futures
import dhash
import json
import os
import pathlib


def print_return(s):
    print(s + "\r", end="")


def get_dhash(file_path):
    try:
        image = PIL.Image.open(file_path)
    except OSError:
        return
    return dhash.dhash_int(image)


def main():
    source_dir: pathlib.Path = pathlib.Path(
        os.getenv("SOURCE_DIR", os.getcwd())
    ).resolve()

    file_list = []
    count = 0
    for root, folders, files in os.walk(str(source_dir)):
        root_path = pathlib.Path(root).resolve()
        for fn in files:
            count += 1
            file_list.append(root_path / fn)
            print_return("Collected {} files".format(count))
    print("Collected {} files".format(count))

    hashes = {}
    count = 0
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(get_dhash, file): file for file in sorted(file_list)}
        for future in concurrent.futures.as_completed(futures):
            count += 1
            file_hash = future.result()
            if file_hash is None:
                continue
            hashes[str(futures[future])] = file_hash
            print_return("Scanned {} files".format(count))
    print("Scanned {} files\n**".format(count))

    dhash_file = pathlib.Path(os.getenv("DHASH_FILE"))
    if dhash_file is None:
        dhash_file = pathlib.Path(os.getcwd()) / "dhash.json"
    dhash_file = dhash_file.resolve()
    with dhash_file.open("w") as f:
        json.dump(hashes, f, indent=2)


if __name__ == "__main__":
    main()
