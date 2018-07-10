FROM python:3.6

# Install kearch_common
RUN git clone https://github.com/kearch/kearch
RUN cd kearch/packages/kearch_common && pip install -e .

# RUN git clone https://github.com/kearch/kearch.git
WORKDIR kearch/packages/meta_query_processor

# These lines are for debug. Use when you want local files.
# COPY ./flask_main.py ./flask_main.py
# COPY ./meta_query_processor.py ./meta_query_processor.py
# COPY ./requirements.txt ./requirements.txt
# COPY ./templates ./templates

RUN pip install -r requirements.txt

CMD python "flask_main.py"
