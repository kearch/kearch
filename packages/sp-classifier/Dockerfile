# You must build this Dockerfile at project root.
# > docker build -f packages/specialist_classifier/Dockerfile .
From python:3.6
ARG KEARCH_COMMON_BRANCH="dev"

RUN pip install flask pytest

COPY packages/kearch_common /kearch/packages/kearch_common
RUN cd /kearch/packages/kearch_common && pip install -e .

COPY packages/kearch_classifier /kearch/packages/kearch_classifier
RUN cd /kearch/packages/kearch_classifier && pip install -e .

COPY /packages/sp-classifier /kearch/packages/sp-classifier
WORKDIR /kearch/packages/sp-classifier

CMD ["python", "-u", "flask_main.py"]
