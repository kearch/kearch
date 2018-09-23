from bs4 import BeautifulSoup
import requests

urls_computer = [
    'https://en.wikipedia.org/wiki/Computer_science',
    'https://en.wikipedia.org/wiki/Programming_language_theory',
    'https://en.wikipedia.org/wiki/Computational_complexity_theory',
    'https://en.wikipedia.org/wiki/Computer_programming',
    'https://en.wikipedia.org/wiki/Computer_scientist',
    'https://en.wikipedia.org/wiki/Complex_system',
    'https://en.wikipedia.org/wiki/Human%E2%80%93computer_interaction',
    'https://en.wikipedia.org/wiki/Computer_accessibility']
urls_computer_ja = [
    'https://ja.wikipedia.org/wiki/%E8%A8%88%E7%AE%97%E6%A9%9F%E7%A7%91%E5%AD%A6',
    'https://ja.wikipedia.org/wiki/%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%9F%E3%83%B3%E3%82%B0_(%E3%82%B3%E3%83%B3%E3%83%94%E3%83%A5%E3%83%BC%E3%82%BF)']
urls_history = [
    'https://en.wikipedia.org/wiki/History']
urls_kyoto = [
    'https://en.wikipedia.org/wiki/Kyoto']
urls_random = [
    'https://en.wikipedia.org/wiki/Life',
    'https://en.wikipedia.org/wiki/Human',
    'https://en.wikipedia.org/wiki/History_of_the_world',
    'https://en.wikipedia.org/wiki/Culture',
    'https://en.wikipedia.org/wiki/Language',
    'https://en.wikipedia.org/wiki/The_arts',
    'https://en.wikipedia.org/wiki/Science',
    'https://en.wikipedia.org/wiki/Technology',
    'https://en.wikipedia.org/wiki/Mathematics']
urls_random_ja = [
    'https://ja.wikipedia.org/wiki/%E3%83%A1%E3%82%A4%E3%83%B3%E3%83%9A%E3%83%BC%E3%82%B8',
    'https://ja.wikipedia.org/wiki/Portal:%E5%93%B2%E5%AD%A6']
urls = urls_random_ja

if __name__ == '__main__':
    for url in urls:
        content = requests.get(url).content
        soup = BeautifulSoup(content, "lxml")
        res = set()
        for l in list(soup.findAll("a")):
            s = l.get('href')
            # CHECK HERE
            if type(s) == str and 'http://ja.wikipedia' in s:
                res.add(s)
            if type(s) == str and s[:6] == '/wiki/':
                res.add('https://ja.wikipedia.org' + s)
        for s in res:
            print(s)
