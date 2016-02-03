import os
import unittest
import tempfile

from webtest import TestApp
from henet.app import make_app


HERE = os.path.dirname(__file__)


class TestViews(unittest.TestCase):

    def setUp(self):
        self.config = os.path.join(HERE, 'config.ini')
        hdl, self.config_file = tempfile.mkstemp()
        with open(self.config) as f:
            os.write(hdl, f.read() % {'testdir': HERE})
        os.close(hdl)
        self.app = TestApp(make_app(self.config_file))

    def tearDown(self):
        os.remove(self.config_file)

    def test_home(self):
        resp = self.app.get('/')
        self.assertEqual(resp.status_int, 302)
        resp = resp.follow()
        self.assertEqual(resp.status_int, 200)
