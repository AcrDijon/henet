# coding: utf8
import os
import datetime
from mimetypes import guess_type

from bottle import route, request, app, post, redirect
from bottle_utils.csrf import csrf_token

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
        return media[start:end], total_pages

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
