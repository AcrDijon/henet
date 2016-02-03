from henet.tests.support import TestView


class TestCategory(TestView):
    def test_category(self):
        resp = self.app.get('/category/actus')
        self.assertEqual(resp.status_int, 302)
        resp = resp.follow()
        self.assertEqual(resp.status_int, 200)

        # adding an article
        create_form = resp.forms[1]
        create_form['title'] = 'New article'
        resp = create_form.submit('cat_add_actus')

        # we should be redirected to the article
        article_page = resp.follow().follow()
        self.assertEqual(article_page.status_int, 200)
        self.assertEqual(article_page.form['title'].value, 'New article')

        # let's go back to the category view and suppress it
        resp = self.app.get('/category/actus').follow()
        last_article_suppress_form = resp.forms[0]
        resp = last_article_suppress_form.submit().follow()

        # should be gone
        resp = resp.follow()
        self.assertTrue('new' not in resp.text)
