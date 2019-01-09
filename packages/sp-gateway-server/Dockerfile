FROM python:3-alpine
ARG KEARCH_COMMON_BRANCH="dev"

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt
RUN git clone https://github.com/kearch/kearch
RUN cd /kearch/packages/kearch_common && git checkout $KEARCH_COMMON_BRANCH && pip install -e .

COPY . /usr/src/app

EXPOSE 10080

ENTRYPOINT ["python3"]

CMD ["-m", "openapi_server"]
