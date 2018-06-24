From python:3

RUN pip install flask
RUN git clone https://github.com/kearch/kearch
RUN cd kearch/packages/kearch_common && pip install -e .
CMD python3 kearch/packages/specialist_query_processor/flask_main.py
