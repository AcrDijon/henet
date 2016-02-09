from henet.tests.support import TestView


class TestPages(TestView):
    def test_pages(self):
        resp = self.app.get('/page/pages')
        self.assertEqual(resp.status_int, 302)
        resp = resp.follow()
        self.assertEqual(resp.status_int, 200)

        # adding a page
        create_form = resp.forms[1]
        create_form['title'] = 'New page'
        resp = create_form.submit('page_add_pages')

        # we should be redirected to the page
        article_page = resp.follow().follow()
        self.assertEqual(article_page.status_int, 200)
        self.assertEqual(article_page.form['title'].value, 'New page')

        # let's change its body
        article_page.forms[0]['body'] = 'blah'
        resp = article_page.forms[0].submit()
        body = resp.follow().follow().forms[0]['body'].value
        self.assertEqual(body.strip(), 'blah')

        # let's go back to the category view and suppress it
        resp = self.app.get('/page/pages').follow()
        last_page_suppress_form = resp.forms[0]
        resp = last_page_suppress_form.submit().follow()

        # should be gone
        resp = resp.follow()
        self.assertTrue('new' not in resp.text)
