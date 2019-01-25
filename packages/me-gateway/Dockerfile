From python:3.6
ARG KEARCH_COMMON_BRANCH="dev"

RUN git clone https://github.com/kearch/kearch
RUN cd /kearch/packages/kearch_common && git checkout $KEARCH_COMMON_BRANCH && pip install -e .

COPY . /kearch/packages/meta_gateway
WORKDIR /kearch/packages/meta_gateway

RUN pip install -r requirements.txt

# Following 4 lines are for debug.
# COPY ./meta_gateway.py ./meta_gateway.py
# COPY ./flask_main.py ./flask_main.py
# COPY ./templates ./templates
# CMD python3 flask_main.py
CMD ["python", "-u", "flask_main.py"]
