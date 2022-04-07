import unittest
import requests_mock
from crawler import Crawler
from bs4 import BeautifulSoup


class TestCrawler(unittest.TestCase):

    @requests_mock.mock()
    def test_crawl(self, m):
        m.get('http://aurl.com', text='a response')
        self.assertEqual(Crawler('http://aurl.com').crawl(), {'a': 1, 'response': 1})
        m.get('http://burl.com', text='b response')
        self.assertEqual(Crawler('http://burl.com').crawl(), {'b': 1, 'response': 1})
        m.get('http://curl.com', text='c response')
        self.assertEqual(Crawler('http://curl.com').crawl(), {'c': 1, 'response': 1})

    @requests_mock.mock()
    def test_request_html(self, m):
        m.get('http://aurl.com', text='<p>a response</p>')
        self.assertEqual(Crawler('').request_html('http://aurl.com'), BeautifulSoup('<p>a response</p>', 'html.parser'))

    def test_get_all_text(self):
        soup = BeautifulSoup('<p>a response</p>', 'html.parser')
        self.assertEqual(Crawler('').get_all_text(soup, Crawler.EXTRACTED_TAGS), ['a response'])

    def test_get_all_words(self):
        self.assertEqual(Crawler('').get_all_words(['a response', 's s']), ['a', 'response', 's', 's'])

    def test_clean_words(self):
        self.assertEqual(Crawler('').get_clean_words(['a', 'response', 's', 's', ' '], Crawler.SYMBOLS), ['a', 'response', 's', 's'])

    def test_get_word_count(self):
        self.assertEqual(Crawler('').get_word_count(['a', 'response', 's', 's']), {'a': 1, 'response': 1, 's': 2} )


if __name__ == '__main__':
    unittest.main()

