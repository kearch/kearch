From python:3

RUN pip install flask
RUN git clone https://github.com/kearch/kearch
RUN cd kearch/packages/kearch_common && pip install -e .

# Following 4 lines are for debug.
# COPY ./flask_main.py ./flask_main.py
# COPY ./static ./static
# COPY ./templates ./templates
# CMD python3 flask_main.py
CMD cd kearch/packages/meta_front && python3 kearch/packages/meta_front/flask_main.py
