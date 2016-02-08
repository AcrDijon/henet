import unittest
from henet.article import Article


class TestArticle(unittest.TestCase):
    def test_end_of_line(self):

        # we want to make sure we don't generate windows-style EOL
        article = Article()
        article.set_metadata('title', u'ok')
        article['body'] = u'hey\r\nyou'

        result = article.render()
        self.assertTrue(u'\r\n' not in result)
        self.assertTrue(u'hey\nyou' in result)
