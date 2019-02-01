FROM node:8-alpine as builder
COPY /packages/me-admin /kearch/packages/me-admin
WORKDIR /kearch/packages/me-admin
RUN yarn && yarn build-prod


# You must build this Dockerfile at project root.
# > docker build -f packages/me-admin/Dockerfile .
From python:3.6
ARG KEARCH_COMMON_BRANCH="dev"

RUN pip install flask
RUN pip install flask-login

COPY packages/kearch_common /kearch/packages/kearch_common
RUN cd /kearch/packages/kearch_common && pip install -e .

COPY packages/kearch_evaluator /kearch/packages/kearch_evaluator
RUN cd /kearch/packages/kearch_evaluator && pip install -e .

COPY /packages/me-admin /kearch/packages/me-admin
COPY --from=builder /kearch/packages/me-admin/static/dist /kearch/packages/me-admin/static/dist
WORKDIR /kearch/packages/me-admin

CMD ["python", "-u", "flask_main.py"]
