import os
import unittest
import tempfile
import shutil

from konfig import Config
from webtest import TestApp
from henet.app import make_app


HERE = os.path.dirname(__file__)
content = os.path.join(HERE, 'content')


class TestView(unittest.TestCase):

    def setUp(self):
        self.config = os.path.join(HERE, 'config.ini')
        hdl, self.config_file = tempfile.mkstemp()
        with open(self.config) as f:
            os.write(hdl, f.read() % {'testdir': HERE})
        os.close(hdl)
        environ = {'HTTP_X_FORWARDED_FOR': '168.0.0.1',
                   'REMOTE_ADDR': '127.0.0.1'}
        self.app = TestApp(make_app(self.config_file),
                           extra_environ=environ)
        self.config = Config(unicode(self.config_file))
        self.tmp_content = tempfile.mkdtemp()
        self.save_content = os.path.join(self.tmp_content, 'content')
        shutil.copytree(content, self.save_content)

    def tearDown(self):
        os.remove(self.config_file)
        shutil.rmtree(content)
        shutil.move(self.save_content, content)
        shutil.rmtree(self.tmp_content)
