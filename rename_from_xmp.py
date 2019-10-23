import PIL.Image
import datetime
import libxmp.utils
import logging
import os
import pathlib
import piexif
import sys

log = logging.getLogger(__name__)


def process(f: pathlib.Path):
    file_date = None
    xmp = libxmp.utils.file_to_dict(str(f))
    for t in xmp.get('http://ns.adobe.com/xap/1.0/'):
        if t[0] == 'xmp:CreateDate':
            file_date = datetime.datetime.strptime(t[1], '%Y-%m-%dT%H:%M:%S%z')
            file_date = file_date.replace(tzinfo=None)
    if file_date is None:
        log.warning(f'Did not find date for {f}')
        return
    log.info(f'CreateDate is {file_date!r}')
    with PIL.Image.open(f) as im:
        exif_dict = piexif.load(im.info['exif'])
        exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = file_date.strftime('%Y:%m:%d %H:%M:%S')
        exif_bytes = piexif.dump(exif_dict)
        file_name = f.parent / file_date.strftime('%Y%m%d_%H%M%S.jpg')
        log.info(f'Saving to {file_name}')
        im.save(file_name, exif=exif_bytes, quality='keep')


def main():
    log_format = os.getenv('LOG_FORMAT', '%(levelname)s [%(name)s] %(message)s')
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    logging.basicConfig(format=log_format, level=log_level, stream=sys.stdout)
    f = pathlib.Path(os.getenv('FILENAME'))
    process(f)


if __name__ == '__main__':
    main()
