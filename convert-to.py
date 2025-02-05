import argparse
import pathlib
import subprocess


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Convert media files')
    parser.add_argument('format', choices=('jpg', 'mp3', 'mp4'), help='target format')
    parser.add_argument('files', nargs='+', help='files to convert')
    return parser.parse_args()


def to_jpg(source_path: pathlib.Path):
    target_path = source_path.with_suffix('.jpg')
    cmd = [
        '/usr/bin/gm', 'convert',
        str(source_path),
        str(target_path)
    ]
    subprocess.call(cmd)


def to_mp3(source_path: pathlib.Path):
    target_path = source_path.with_suffix('.mp3')
    cmd = [
        '/usr/bin/ffmpeg',
        '-i',
        str(source_path),
        str(target_path)
    ]
    subprocess.call(cmd)


def to_mp4(source_path: pathlib.Path):
    target_path = source_path.with_suffix('.mp4')
    cmd = [
        '/usr/bin/ffmpeg',
        '-i', str(source_path),
        '-c:v', 'libx264',
        '-vf', 'format=yuv420p',
        '-c:a', 'aac',
        '-movflags', '+faststart',
        str(target_path)
    ]
    subprocess.call(cmd)


actions = {
    'jpg': to_jpg,
    'mp3': to_mp3,
    'mp4': to_mp4,
}


def main():
    args = parse_args()
    total = len(args.files)
    action = actions.get(args.format)
    for i, filename in enumerate(args.files, start=1):
        source_path = pathlib.Path(filename).resolve()
        print(f'Processing {source_path} ({i} of {total})')
        action(source_path)


if __name__ == '__main__':
    main()
