FROM python:3.6
ARG KEARCH_COMMON_BRANCH="dev"

COPY packages/kearch_classifier /kearch/packages/kearch_classifier
RUN cd /kearch/packages/kearch_classifier && pip install -e .

COPY packages/kearch_common /kearch/packages/kearch_common
RUN cd /kearch/packages/kearch_common && pip install -e .

COPY packages/sp-crawler-child /kearch/packages/sp-crawler-child
WORKDIR /kearch/packages/sp-crawler-child

RUN pip install -r requirements.txt
RUN python -c "import nltk; nltk.download('punkt')"
RUN python -c "import nltk; nltk.download('stopwords')"

# This process take a few minutes because it downloads many webpages
# You can comment out these 2 lines. If you comment out, cached models are used.
RUN python /kearch/packages/kearch_classifier/kearch_classifier/average_document.py random_url_list en
RUN python /kearch/packages/kearch_classifier/kearch_classifier/classifier.py computer_science_url_list random_url_list en
# If you want to select Japanse, please use
# RUN python average_document.py random_ja_url_list_short ja
# RUN python classifier.py computer_science_ja_url_list random_ja_url_list ja

# Restart flask server periodically to suppress memory usage.
ENV KEARCH_SP_CRAWLER_CHILD_RESTART_SEC=3600

CMD ["python", "-u", "flask_main.py"]
