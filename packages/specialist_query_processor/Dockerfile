From python:3

RUN pip install flask
RUN git clone https://github.com/kearch/kearch
RUN cd kearch/packages/kearch_common && pip install -e .
RUN cd kearch/packages/specialist_query_processor && python3 flask_main.py
