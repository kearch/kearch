From python:3.6

RUN pip install flask
RUN git clone https://github.com/kearch/kearch
RUN cd /kearch && git checkout feature/connect-proto
RUN cd /kearch/packages/kearch_common && pip install -e .

COPY . /kearch/packages/specialist_front
WORKDIR /kearch/packages/specialist_front

# Following 4 lines are for debug.
# COPY ./flask_main.py ./flask_main.py
# COPY ./static ./static
# COPY ./templates ./templates
# CMD python3 flask_main.py
CMD ["python", "-u", "kearch/packages/specialist_front/flask_main.py"]
