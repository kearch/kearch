FROM python:3.6
ARG KEARCH_COMMON_BRANCH="dev"

# Install kearch_common
COPY packages/kearch_classifier /kearch/packages/kearch_classifier
RUN cd /kearch/packages/kearch_classifier && pip install -e .

# Install kearch_common
COPY packages/kearch_common /kearch/packages/kearch_common
RUN cd /kearch/packages/kearch_common && pip install -e .

COPY packages/me-evaluater /kearch/packages/me-evaluater
WORKDIR /kearch/packages/me-evaluater

RUN pip install -r requirements.txt

CMD ["python", "-u", "flask_main.py"]
