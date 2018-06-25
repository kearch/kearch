FROM python:3.6

RUN git clone https://github.com/kearch/kearch.git
WORKDIR kearch/packages/specialist_crawler_child

# These lines are for debug. Use when you want local files.
# COPY ./requirements.txt ./requirements.txt
# COPY ./computer_science_url_list_short ./computer_science_url_list
# COPY ./random_url_list_short ./random_url_list
# COPY ./average_document.py ./average_document.py
# COPY ./nb_topic_detect.py ./nb_topic_detect.py
# COPY ./title_topic_detect.py ./title_topic_detect.py
# COPY ./flask_main.py ./flask_main.py
# COPY ./webpage.py ./webpage.py
# COPY ./crawler_child.py ./crawler_child.py
# COPY ./templates ./templates


RUN pip install -r requirements.txt
RUN python -c "import nltk; nltk.download('punkt')"
RUN python -c "import nltk; nltk.download('stopwords')"
RUN mkdir webpage_cache
RUN mkdir average_document_cache
RUN mkdir nb_topic_detect_cache
RUN mkdir title_topic_detect_cache

# This process take a few minutes because it downloads many webpages
RUN python average_document.py random_url_list
RUN python nb_topic_detect.py computer_science_url_list random_url_list
RUN python title_topic_detect.py computer_science_url_list random_url_list

CMD python "flask_main.py"
