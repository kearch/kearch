FROM node:8-alpine as builder
COPY /packages/sp-admin /kearch/packages/sp-admin
WORKDIR /kearch/packages/sp-admin
RUN yarn && yarn build-prod


# You must build this Dockerfile at project root.
# > docker build -f packages/specialist_admin/Dockerfile .
From python:3.6
ARG KEARCH_COMMON_BRANCH="dev"

RUN apt-get update && apt-get install -y apt-transport-https && \
    curl -sL https://deb.nodesource.com/setup_8.x | bash - && \
    curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && \
    echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list && \
    apt-get update && apt-get install -y yarn

RUN pip install flask
RUN pip install flask-login

COPY packages/kearch_common /kearch/packages/kearch_common
RUN cd /kearch/packages/kearch_common && pip install -e .

COPY packages/kearch_classifier /kearch/packages/kearch_classifier
RUN cd /kearch/packages/kearch_classifier && pip install -e .

RUN python -c "import nltk; nltk.download('punkt')"
RUN python -c "import nltk; nltk.download('stopwords')"

COPY /packages/sp-admin /kearch/packages/sp-admin
COPY --from=builder /kearch/packages/sp-admin/dist /kearch/packages/sp-admin
WORKDIR /kearch/packages/sp-admin

CMD ["python", "-u", "flask_main.py"]
