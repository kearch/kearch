From python:3.6
ARG KEARCH_COMMON_BRANCH="dev"

RUN pip install flask
RUN git clone https://github.com/kearch/kearch
RUN cd /kearch/packages/kearch_common && git checkout $KEARCH_COMMON_BRANCH && pip install -e .

COPY . /kearch/packages/specialist_query_processor
WORKDIR /kearch/packages/specialist_query_processor

CMD ["python", "-u", "flask_main.py"]
