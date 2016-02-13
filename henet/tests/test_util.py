# encoding: utf8
import unittest
from mock import patch
from henet.util import send_email


class TestUtil(unittest.TestCase):

    def test_send_email(self):
        tos = [u'tarek@ziade.org']
        subject = u'Hello'
        body = u'Café'
        smtp_config = {'host': 'localhost', 'port': 25,
                       'from': 'henet@local.com'}

        with patch("smtplib.SMTP") as mock_smtp:
            send_email(tos, subject, body, smtp_config)

            instance = mock_smtp.return_value
            self.assertTrue(instance.sendmail.called)
            self.assertEqual(instance.sendmail.call_count, 1)
