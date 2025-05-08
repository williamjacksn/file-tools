import collections
import concurrent.futures
import dhash
import hashlib
import os
import pathlib
import PIL.Image


def print_return(s):
    print(s + "\r", end="")


def get_dhash(file_path):
    try:
        image = PIL.Image.open(file_path)
    except OSError:
        return
    row, col = dhash.dhash_row_col(image)
    return dhash.format_hex(row, col)


def get_hash(file_path, buffer_size=65536):
    with file_path.open(mode="rb") as f:
        hasher = hashlib.sha256()
        buffer = f.read(buffer_size)
        while len(buffer) > 0:
            hasher.update(buffer)
            buffer = f.read(buffer_size)
        return hasher.hexdigest()


def main():
    file_list = []
    hashes = {}
    dupes = collections.defaultdict(list)

    count = 0
    for root, folders, files in os.walk(os.getcwd()):
        root_path = pathlib.Path(root).resolve()
        for fn in files:
            count += 1
            file_list.append(root_path / fn)
            print_return("Collected {} files".format(count))
    print("Collected {} files".format(count))

    count = 0
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(get_dhash, file): file for file in sorted(file_list)}
        for future in concurrent.futures.as_completed(futures):
            count += 1
            file_hash = future.result()
            if file_hash is None:
                continue
            elif file_hash in hashes:
                dupes[hashes[file_hash]].append(futures[future])
            else:
                hashes[file_hash] = futures[future]
            print_return("Scanned {} files".format(count))
    print("Scanned {} files\n**".format(count))

    for first_file in sorted(dupes.keys()):
        print(first_file)
        for dupe_file in dupes[first_file]:
            print(dupe_file)
        input()


if __name__ == "__main__":
    main()
