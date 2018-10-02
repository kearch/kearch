FROM python:3.6
ARG KEARCH_COMMON_BRANCH="dev"

# Install kearch_common
RUN git clone https://github.com/kearch/kearch
RUN cd /kearch/packages/kearch_common && git checkout $KEARCH_COMMON_BRANCH && pip install -e .

COPY . /kearch/packages/specialist_crawler_parent
WORKDIR /kearch/packages/specialist_crawler_parent

# These lines are for debug. Use when you want local files.
# COPY ./main.py ./main.py

CMD ["python", "-u", "main.py"]
