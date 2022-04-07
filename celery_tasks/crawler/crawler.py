import requests
from bs4 import BeautifulSoup


class Crawler:
    SYMBOLS = "!@#$%^&*()_-+={[}]|\;:\"<>?/., "
    EXTRACTED_TAGS = ['style', 'script', '[document]', 'head', 'title']

    def __init__(self, url: str):
        self.url = url

    def crawl(self):
        soup = self.request_html(self.url)
        text = self.get_all_text(soup, self.EXTRACTED_TAGS)
        word_list = self.get_all_words(text)
        clean_word_list = self.get_clean_words(word_list, self.SYMBOLS)
        return self.get_word_count(clean_word_list)

    @staticmethod
    def request_html(url):
        source_code = requests.get(url).text
        soup = BeautifulSoup(source_code, 'html.parser')
        return soup

    @staticmethod
    def get_all_text(soup, extracted_tags):
        [s.extract() for s in soup(extracted_tags)]
        return soup.findAll(text=True)

    @staticmethod
    def get_all_words(text):
        word_list = []
        for each_text in text:
            content = each_text
            words = content.lower().split()
            for each_word in words:
                word_list.append(each_word)
        return word_list

    @staticmethod
    def get_clean_words(word_list, symbols):
        clean_list = []
        for word in word_list:
            for i in range(len(symbols)):
                word = word.replace(symbols[i], '')
            if len(word) > 0:
                clean_list.append(word)
        return clean_list

    @staticmethod
    def get_word_count(clean_word_list):
        word_count = {}
        for word in clean_word_list:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1
        return word_count
