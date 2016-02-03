from henet.tests.support import TestView


class TestHome(TestView):
    def test_home(self):
        resp = self.app.get('/')
        self.assertEqual(resp.status_int, 302)
        resp = resp.follow()
        self.assertEqual(resp.status_int, 200)
