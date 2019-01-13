FROM node:8-alpine as builder
COPY /packages/sp-admin /kearch/packages/sp-admin
WORKDIR /kearch/packages/sp-admin
RUN yarn && yarn build-prod


# You must build this Dockerfile at project root.
# > docker build -f packages/specialist_admin/Dockerfile .
From python:3.6
ARG KEARCH_COMMON_BRANCH="dev"

RUN pip install flask
RUN pip install flask-login

COPY packages/kearch_common /kearch/packages/kearch_common
RUN cd /kearch/packages/kearch_common && pip install -e .

COPY packages/kearch_classifier /kearch/packages/kearch_classifier
RUN cd /kearch/packages/kearch_classifier && pip install -e .

RUN python -c "import nltk; nltk.download('punkt')"
RUN python -c "import nltk; nltk.download('stopwords')"

COPY /packages/sp-admin /kearch/packages/sp-admin
COPY --from=builder /kearch/packages/sp-admin/static/dist /kearch/packages/sp-admin/static/dist
WORKDIR /kearch/packages/sp-admin

CMD ["python", "-u", "flask_main.py"]
