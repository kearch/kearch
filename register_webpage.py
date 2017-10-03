import subprocess
import nltk

def url_to_main_text(url):
    cmd = "w3m " + url
    text = subprocess.Popen(cmd, stdout=subprocess.PIPE,shell=True).communicate()[0]
    return text

# def text_to_word_list(text):


if __name__ == '__main__':
     print(url_to_main_text('https://en.wikipedia.org/wiki/Spotted_green_pigeon'))

