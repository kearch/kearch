# You must build this Dockerfile at project root.
# > docker build -f packages/me-admin/Dockerfile .
From python:3.6
ARG KEARCH_COMMON_BRANCH="dev"

RUN pip install flask

COPY packages/kearch_common /kearch/packages/kearch_common
RUN cd /kearch/packages/kearch_common && pip install -e .

COPY packages/kearch_evaluater /kearch/packages/kearch_evaluater
RUN cd /kearch/packages/kearch_evaluater && pip install -e .

COPY /packages/me-admin /kearch/packages/me-admin
WORKDIR /kearch/packages/me-admin

CMD ["python", "-u", "flask_main.py"]
