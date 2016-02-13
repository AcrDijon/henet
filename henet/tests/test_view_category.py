# encoding: utf8
import os
from henet.tests.support import TestView
from henet.rst.parse import parse_article


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

        # lets make sure we generated a proper article on disk
        cat_dir = dict(self.config['actus'])['path']
        filename = os.path.join(cat_dir, 'new-article.rst')
        parsed = parse_article(filename)
        self.assertEqual(parsed['metadata']['category'], u'Actualités')

        # let's change its body and date
        article_page.forms[0]['body'] = 'blah'
        article_page.forms[0]['date'] = '16/11/2012'
        resp = article_page.forms[0].submit()
        body = resp.follow().follow().forms[0]['body'].value
        self.assertEqual(body.strip(), 'blah')

        # let's create a new article with the same title
        resp = self.app.get('/category/actus')
        self.assertEqual(resp.status_int, 302)
        resp = resp.follow()
        self.assertEqual(resp.status_int, 200)

        # adding the 2nd article
        create_form = resp.forms[2]
        create_form['title'] = 'New article'
        resp = create_form.submit('cat_add_actus')
        filename2 = os.path.join(cat_dir, 'new-article1.rst')
        self.assertTrue(os.path.exists(filename2))
        os.remove(filename2)

        # let's suppress the first article
        resp = self.app.get('/category/actus').follow()
        for form in resp.forms.values():
            if 'new-article' in form.action:
                form.submit()
                break

        # should be gone
        resp = self.app.get('/category/actus').follow()
        self.assertTrue('New article' not in resp.text)

    def test_no_empty_title(self):
        resp = self.app.get('/category/actus')
        self.assertEqual(resp.status_int, 302)
        resp = resp.follow()
        self.assertEqual(resp.status_int, 200)

        # adding an article
        create_form = resp.forms[1]
        resp = create_form.submit('cat_add_actus')

        # we should be redirected to the category with a flash
        # message
        cat_page = resp.follow().follow()
        self.assertTrue('A title is required' in cat_page.text)
