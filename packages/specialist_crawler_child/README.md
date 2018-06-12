# specialist crawler child
## Setup
```
python3 average_document.py random_url_list
python3 nb_topic_detect.py computer_science_url_list random_url_list
python3 title_topic_detect.py computer_science_url_list random_url_list
python3 flask_main.py
```
## API
### How to crawl a page
```
http://${ip adress of this container}:10080/crawl_a_page?url=${quoted url by urllib.parse.qupte}
```
Examples
```
http://localhost:10080/crawl_a_page?url=https%3A//shedopen.deviantart.com/
http://localhost:10080/crawl_a_page?url=https%3A//en.wikipedia.org/wiki/Haskell_%28programming_language%29
```
## Result
The result is a json value.
This json contains
- url
- summary of a given url
- title words (as a list)
- tfidf values for each word in a given url (as a dictionary)
