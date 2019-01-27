From python:3.6
ARG KEARCH_COMMON_BRANCH="dev"

RUN pip install flask pytest
RUN git clone https://github.com/kearch/kearch
RUN cd /kearch/packages/kearch_common && git checkout $KEARCH_COMMON_BRANCH && pip install -e .

COPY . /kearch/packages/specialist_gateway
WORKDIR /kearch/packages/specialist_gateway

# Following 4 lines are for debug.
# COPY ./specialist_gateway.py ./specialist_gateway.py
# COPY ./flask_main.py ./flask_main.py
# COPY ./templates ./templates
# CMD python3 flask_main.py
CMD ["python", "-u", "flask_main.py"]
