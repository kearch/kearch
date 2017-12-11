from bs4 import BeautifulSoup
import requests

url = 'https://en.wikipedia.org/wiki/Computer_science'
# url = 'https://en.wikipedia.org/wiki/Portal:Featured_content'

if __name__ == '__main__':
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
