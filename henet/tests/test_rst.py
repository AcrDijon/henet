import os
import unittest

from henet.rst.parse import parse_article
from Levenshtein import distance, jaro


SAMPLE_DIR = os.path.join(os.path.dirname(__file__), 'samples')
MUTATED_FILES = [
    '2013-05-06-rotarienne.rst', '2013-05-13-traildesforts.rst',
    '2013-05-26-2207-maxi-race-2013.rst', '2013-06-11-utco.rst',
    '2013-06-20-0022-trail-du-mont-dor.rst',
    '2013-06-26-1230-organisation-ronde-des-etangs-30-juin-2013.rst',
    '2013-07-12-0836-resultats-du-week-end.rst',
    '2013-07-27-1455-compte-rendu-de-julien-harson-sur-litt.rst',
    '2013-11-12-sparnatrail.rst',
    '2013-12-13-1836-saintelyon-2013-par-julien-harson.rst',
    '2014-03-03-1200-marathon-du-vulcain-2-mars-2014.rst']


class TestParse(unittest.TestCase):
    def test_parse(self):
        for file in os.listdir(SAMPLE_DIR):
            if not file.endswith('.rst'):
                continue
            filename = os.path.join(SAMPLE_DIR, file)
            article = parse_article(filename)
            rendered = article.render().strip()

            with open(filename) as f:
                source = f.read().strip()
                source = source.expandtabs(4).decode('utf8')

            if source != rendered:
                lev_ = distance(source, rendered)
                jaro_ = jaro(source, rendered)

                if lev_ > 10 and jaro_ < 0.85 and file not in MUTATED_FILES:
                    print('%d %f %s' % (lev_, jaro_, filename))
                    raise AssertionError(filename)
