# encoding: utf8
from henet.tests.support import TestView


_BAD_RST = """
Hey you title
-----------

- one
- two
three

"""


class TestPreview(TestView):
    def test_preview_get(self):
        resp = self.app.get('/preview').follow()
        self.assertEqual(resp.body, 'Chargement...')

    def test_preview(self):
        resp = self.app.post_json('/preview',
                                  params={'rst': '**test**'})
        self.assertTrue('<strong>test</strong>' in resp.body)

    def test_preview_bad_rst(self):
        resp = self.app.post_json('/preview',
                                  params={'rst': _BAD_RST})
        self.assertTrue('Bullet list ends without a blank line' in resp.body)
        self.assertTrue('Title underline too short' in resp.body)

        # calling the cache
        resp = self.app.post_json('/preview', params={'rst': _BAD_RST})
