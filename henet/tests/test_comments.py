# encoding: utf8
import unittest
import tempfile
import shutil
import datetime
from henet.comments import Thread, ArticleThread, CommentsDB, Comment


class TestComment(unittest.TestCase):
    def setUp(self):
        self.tempdirs = []

    def tearDown(self):
        for tempdir in self.tempdirs:
            shutil.rmtree(tempdir)

    def get_tempdir(self):
        tempdir = tempfile.mkdtemp()
        self.tempdirs.append(tempdir)
        return tempdir

    def test_empty_comment(self):
        comment = Comment()
        comment.save()   # noop

    def test_linked_to_thread(self):
        tempdir = self.get_tempdir()
        thread = Thread(tempdir)
        comment = Comment(thread=thread)
        comment.save()


class TestArticleThread(TestComment):

    def _create_comments(self):
        tempdir = self.get_tempdir()

        # thread 1: 4 comments with 2 inactive
        thread = Thread(tempdir)

        now = datetime.datetime.now()
        later = now + datetime.timedelta(days=1)
        way_later = later + datetime.timedelta(days=15)
        far_later = way_later + datetime.timedelta(seconds=1)

        # linked to 2 articles
        article_thread = ArticleThread(tempdir, '/post/mypost',
                                       thread.uuid)

        article_thread2 = ArticleThread(tempdir, '/post/mypost2',
                                        thread.uuid)

        article_thread.add_comment(u"Ouai **ouai**", date=now, active=True)
        article_thread.add_comment(u"Ouai **ouai2**", date=later)
        article_thread.add_comment(u"Ouai **ouai3**", date=way_later,
                                   active=True)
        article_thread.add_comment(u"Ouai **ouai4**", date=far_later)

        # XXX see how we can sync related objects
        article_thread.save()
        article_thread2.load()
        article_thread2.save()
        thread.load()
        return thread, article_thread, article_thread2, tempdir

    def test_asjson(self):
        thread, a1, a2, tempdir = self._create_comments()
        json = a1.asjson()
        for field in ('article_uuid', 'thread_uuid'):
            self.assertEqual(json[field], getattr(a1, field))

    def test_empty_commemts(self):
        tempdir = self.get_tempdir()
        ath = ArticleThread(tempdir)
        self.assertEquals(ath.asjson()['comments'], [])
        self.assertEquals(len(ath.render().split('\n')), 1)

    def test_activate_comment(self):
        thread, a1, a2, tempdir = self._create_comments()
        c1, c2, c3, c4 = [comment for comment in
                          thread.get_comments(True, True)]
        thread.activate_comment(c1.uuid)
        thread.save()

        # we have 3 active comments now
        comments = thread.get_comments()
        self.assertEqual(len(comments), 3)

        # out of 4
        comments = thread.get_comments(include_inactive=True)
        self.assertEqual(len(comments), 4)
        comment = comments[0]

        # most recent first
        self.assertEqual(comment.text, u"Ouai **ouai4**")

    def test_get_comments(self):
        thread, a1, a2, tempdir = self._create_comments()

        # we have 2 active comments
        comments = thread.get_comments()
        self.assertEqual(len(comments), 2)

        comments = thread.get_comments(include_inactive=True)
        self.assertEqual(len(comments), 4)
        comment = comments[0]

        # most recent first
        self.assertEqual(comment.text, u"Ouai **ouai4**")


class TestCommentsDB(TestArticleThread):
    def test_get_moderation_queue(self):
        thread, a1, a2, tempdir = self._create_comments()

        # let's check the moderation queue
        comments = CommentsDB(tempdir)

        # let's moderate our articles
        cuids = [c.uuid for c in comments.get_moderation_queue()]
        comments.activate_comment(cuids[0])
        comments.reject_comment(cuids[1])

        # noop
        comments.activate_comment("xxx")

        # the queue should be empty now
        self.assertEqual(len(list(comments.get_moderation_queue())), 0)

        # let's check we have 3 active comments now in that thread
        thread.load()
        comments = thread.get_comments()
        self.assertEqual(len(comments), 3)

    def test_get_comments(self):
        thread, a1, a2, tempdir = self._create_comments()

        # the DB allows you to get comments for a given article
        comments = CommentsDB(tempdir)
        res = list(comments.get_comments(a1.article_uuid))
        self.assertEqual(len(res), 2)
