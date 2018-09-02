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
urls = urls_kyoto

if __name__ == '__main__':
    for url in urls:
        content = requests.get(url).content
        soup = BeautifulSoup(content, "lxml")
        res = set()
        for l in list(soup.findAll("a")):
            s = l.get('href')
            if type(s) == str and 'http://en.wikipedia' in s:
                res.add(s)
            if type(s) == str and s[:6] == '/wiki/':
                res.add('https://en.wikipedia.org' + s)
        for s in res:
            print(s)
