FROM python:3.6
COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
RUN python -m nltk.downloader punkt stopwords
RUN python average_document.py random_url_list
RUN python nb_topic_detect.py computer_science_url_list random_url_list
RUN python title_topic_detect.py computer_science_url_list random_url_list

CMD ["flask_main.py"]
