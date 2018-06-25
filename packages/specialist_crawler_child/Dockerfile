FROM python:3.6
RUN git clone https://github.com/kearch/kearch.git
WORKDIR kearch/packages/specialist_crawler_child

RUN pip install -r requirements.txt
RUN python -m nltk.downloader punkt stopwords
RUN mkdir webpage_cache
RUN mkdir average_document_cache
RUN mkdir nb_topic_detect_cache
RUN mkdir title_topic_detect_cache

# This process take a few minutes because it downloads many webpages
RUN python average_document.py random_url_list

RUN python nb_topic_detect.py computer_science_url_list random_url_list
RUN python title_topic_detect.py computer_science_url_list random_url_list

CMD python "flask_main.py"
