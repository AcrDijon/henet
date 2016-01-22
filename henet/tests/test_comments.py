# encoding: utf8
import unittest
import tempfile
import shutil
import datetime

from henet.comments import Thread


class TestThread(unittest.TestCase):

    def setUp(self):
        self.tempdirs = []

    def tearDown(self):
        for tempdir in self.tempdirs:
            shutil.rmtree(tempdir)

    def get_tempdir(self):
        tempdir = tempfile.mkdtemp()
        self.tempdirs.append(tempdir)
        return tempdir

    def test_storage(self):

        tempdir = self.get_tempdir()
        thread = Thread(tempdir)

        now = datetime.datetime.now()
        later = now + datetime.timedelta(days=1)
        way_later = later + datetime.timedelta(days=15)

        thread.add_comment(u"Mémé", "Ouai **ouai**", date=now)
        thread.add_comment(u"Mémé2", "Ouai **ouai**", date=later)
        thread.add_comment(u"Mémé3", "Ouai **ouai**", date=way_later)

        thread.save()
        thread.load()

        comments = thread.get_comments()
        self.assertEqual(len(comments), 3)
        comment = comments[0]

        # most recent first
        self.assertEqual(comment.title, u"Mémé3")
        self.assertEqual(comment.text, u"Ouai **ouai**")
