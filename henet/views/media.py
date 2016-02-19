# coding: utf8
import os
import datetime
from mimetypes import guess_type

from bottle import route, request, app, post, redirect, get, static_file
from bottle_utils.csrf import csrf_token
from PIL import Image

from henet.util import file_age


mimetypes = os.path.join(os.path.dirname(__file__), '..', 'resources',
                         'images', 'mimetypes')
mimetypes = [f for f in os.listdir(mimetypes) if f.endswith('.png')]


def by_date(file1, file2):
    return -cmp(file1['modified'], file2['modified'])


def sizeof_fmt(num, suffix='b'):
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


# XXX share code with henet.util.parse_article(s)
def parse_file(path):
    type = guess_type(path)[0]
    image_type = type.split('/')[1] + '-icon-24x24.png'
    if image_type not in mimetypes:
        image_type = 'txt-icon-24x24.png'

    return {'name': os.path.split(path)[-1],
            'modified': datetime.datetime.fromtimestamp(file_age(path)),
            'image-type': image_type,
            'type': type,
            'size': sizeof_fmt(os.path.getsize(path))}


def parse_files(path, page=-1, page_size=20):
    if isinstance(path, unicode):
        path = path.encode('utf8')

    media = []
    for root, dirs, files in os.walk(path):
        for file_ in files:
            fullpath = os.path.join(root, file_)
            media.append(parse_file(fullpath))

    media.sort(by_date)
    total_size = len(media)
    total_pages, rest = divmod(total_size, page_size)
    if rest > 0:
        total_pages += 1

    if page != -1:
        start = page * page_size
        end = start + page_size - 1
        media = media[start:end]

    # XXX we want to sort images by their HxW ratio, so they tile
    #
    return media, total_pages


@route("/media")
@app.view("media")
@csrf_token
def get_media():
    page = int(request.params.get('page', 0))
    media_dir = app._config['henet']['media_dir']
    files, total_pages = parse_files(media_dir, page)

    return {'files': files, 'page': page,
            'now': datetime.datetime.now(),
            'total_pages': total_pages,
            'current_page': page,
            'csrf_token': request.csrf_token}


@get("/media/<filename>", no_i18n=True)
def get_file(filename):
    media_dir = app._config['henet']['media_dir']
    fullpath = os.path.join(media_dir, filename)
    mimetype = guess_type(fullpath)[0]

    return static_file(filename, root=media_dir,
                       mimetype=mimetype)


@get("/thumbnail/<size>/<filename>", no_i18n=True)
def get_media_thumbnail(size, filename):
    filename = filename.decode('utf8')

    ext = os.path.splitext(filename)[-1].lower()

    if ext not in  ('.jpg', '.png', '.jpeg', '.bmp'):
        redirect('/resources/images/blank.png')

    media_dir = app._config['henet']['media_dir']
    thumbnails_dir = app._config['henet']['thumbnails_dir']

    thumbname = size + '-' + filename
    thumbnail_file = os.path.join(thumbnails_dir, thumbname)

    if not os.path.exists(thumbnail_file):
        image_file = os.path.join(media_dir, filename)
        size = [int(i) for i in size.split('x')]
        image = Image.open(image_file)
        image.thumbnail(size)
        image.save(thumbnail_file, 'JPEG')


    mimetype = guess_type(thumbnail_file)[0]
    return static_file(thumbname, root=thumbnails_dir,
                       mimetype=mimetype)
