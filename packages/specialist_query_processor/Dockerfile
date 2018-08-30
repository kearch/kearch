From python:3.6

RUN pip install flask
RUN git clone https://github.com/kearch/kearch
RUN cd /kearch && git checkout feature/connect-proto
RUN cd kearch/packages/kearch_common && pip install -e .

COPY . /kearch/packages/specialist_query_processor
WORKDIR /kearch/packages/specialist_query_processor

CMD ["python", "-u", "flask_main.py"]
