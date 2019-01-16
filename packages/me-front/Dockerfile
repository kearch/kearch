FROM node:8-alpine as builder
COPY /packages/me-front /kearch/packages/me-front
WORKDIR /kearch/packages/me-front
RUN yarn && yarn build-prod


From python:3.6
ARG KEARCH_COMMON_BRANCH="dev"

RUN pip install flask

COPY packages/kearch_common /kearch/packages/kearch_common
RUN cd /kearch/packages/kearch_common && pip install -e .

COPY /packages/me-front /kearch/packages/me-front
COPY --from=builder /kearch/packages/me-front/static/dist /kearch/packages/me-front/static/dist
WORKDIR /kearch/packages/me-front

CMD ["python", "-u", "flask_main.py"]
