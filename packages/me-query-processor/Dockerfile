FROM python:3.6
ARG KEARCH_COMMON_BRANCH="dev"

# Install kearch_common
RUN git clone https://github.com/kearch/kearch
RUN cd /kearch/packages/kearch_common && git checkout $KEARCH_COMMON_BRANCH && pip install -e .

COPY . /kearch/packages/me-query-processor
WORKDIR /kearch/packages/me-query-processor

# These lines are for debug. Use when you want local files.
# COPY ./flask_main.py ./flask_main.py
# COPY ./me-query-processor.py ./me-query-processor.py
# COPY ./requirements.txt ./requirements.txt
# COPY ./templates ./templates

RUN pip install -r requirements.txt

CMD ["python", "-u", "flask_main.py"]
