import smtplib
import email.utils
from email.mime.text import MIMEText
from email.header import Header
import os
import hashlib
import bson
import datetime

from henet.rst.parse import parse_article as parse
from henet.article import Article
from henet import logger


def by_date(article1, article2):
    now = datetime.datetime.now()

    return -cmp(article1['metadata'].get('date', now).replace(tzinfo=None),
                article2['metadata'].get('date', now).replace(tzinfo=None))


def file_age(path):
    return os.stat(path).st_mtime


def md5(data):
    return hashlib.md5(data).hexdigest()


def parse_article(path, cache_dir, root_path):
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    age = file_age(path)
    cache = os.path.join(cache_dir, md5(str(age)+path.encode('utf8')))
    if os.path.exists(cache):
        with open(cache) as f:
            article = Article(bson.loads(f.read()))
    else:
        article = parse(path)
        article['filename'] = path[len(root_path):].lstrip('/')
        with open(cache, 'w') as f:
            f.write(bson.dumps(article))

    return article


def parse_articles(path, cache_dir, page=-1, page_size=20):
    if isinstance(path, unicode):
        path = path.encode('utf8')
    articles = []
    for root, dirs, files in os.walk(path):
        for file_ in files:
            if not file_.endswith('.rst'):
                continue
            fullpath = os.path.join(root, file_)
            articles.append(parse_article(fullpath, cache_dir, path))

    articles.sort(by_date)
    total_size = len(articles)
    total_pages, rest = divmod(total_size, page_size)
    if rest > 0:
        total_pages += 1

    if page != -1:
        start = page * page_size
        end = start + page_size - 1
        return articles[start:end], total_pages

    return articles, total_pages


def send_email(tos, subject, body, smtp_config):
    msg = MIMEText(body.encode('utf8'), 'plain', 'utf-8')
    msg['To'] = email.utils.formataddr(('Recipient', ','.join(tos)))
    msg['From'] = email.utils.formataddr(('Author', smtp_config['from']))
    msg['Subject'] = Header(subject, 'utf8')

    server = smtplib.SMTP(smtp_config['host'], smtp_config.get('port', 25))
    try:
        server.ehlo()
        if server.has_extn('STARTTLS'):
            server.starttls()
            server.ehlo()

        username = smtp_config.get('username')
        if username is not None:
            server.login(username, smtp_config['password'])
        server.sendmail(smtp_config['from'], tos, msg.as_string())
        logger.debug("Mail sent")
    except Exception:
        logger.exception("Could not send the email")
    finally:
        server.quit()


def hash(directory):
    articles = []
    if isinstance(directory, unicode):
        directory = directory.encode('utf8')

    for root, dirs, files in os.walk(directory):
        for file_ in files:
            if not file_.endswith('.rst'):
                continue
            fullpath = os.path.join(root, file_)
            age = file_age(fullpath)
            articles.append((fullpath, age))

    articles.sort()
    res = hashlib.md5()
    for path, age in articles:
        res.update('%d:' % age)

    return res.hexdigest()


def save_build_hash(directory, cache_dir):
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    filename = os.path.join(cache_dir, md5(directory) + '.age')

    new_hash = hash(directory)
    with open(filename, 'w') as f:
        f.write(new_hash)


def content_changed(directory, cache_dir):
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    filename = os.path.join(cache_dir, md5(directory) + '.age')

    if os.path.exists(filename):
        with open(filename) as f:
            current_hash = f.read()
    else:
        current_hash = ''

    new_hash = hash(directory)
    return new_hash != current_hash
