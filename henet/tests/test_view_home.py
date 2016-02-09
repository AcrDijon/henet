# encoding: utf8
import time
from henet.tests.support import TestView


class TestHome(TestView):
    def test_home(self):
        resp = self.app.get('/')
        self.assertEqual(resp.status_int, 302)
        resp = resp.follow()
        self.assertEqual(resp.status_int, 200)

    def test_build(self):
        resp = self.app.get('/').follow()
        resp = resp.forms[0].submit()
        text_before = resp.follow().follow().text
        time.sleep(1.1)

        # testing the various alerts
        text_after = self.app.get('/').follow().text
        self.assertTrue(u'Mise à jour démarrée' in text_before)
        self.assertTrue(u'Mise à jour démarrée' not in text_after)
        self.assertTrue(u'Mise à jour terminée' in text_after)
        text_later = self.app.get('/').follow().text
        self.assertTrue(u'Mise à jour démarrée' not in text_later)
        self.assertTrue(u'Mise à jour terminée' not in text_later)
