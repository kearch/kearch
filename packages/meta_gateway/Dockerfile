From python:3.6

RUN pip install flask
RUN git clone https://github.com/kearch/kearch
RUN cd /kearch && git checkout feature/connect-proto
RUN cd /kearch/packages/kearch_common && pip install -e .

COPY . /kearch/packages/meta_gateway
WORKDIR /kearch/packages/meta_gateway

# Following 4 lines are for debug.
# COPY ./meta_gateway.py ./meta_gateway.py
# COPY ./flask_main.py ./flask_main.py
# COPY ./templates ./templates
# CMD python3 flask_main.py
CMD ["python", "-u", "flask_main.py"]
