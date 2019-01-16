FROM node:8-alpine as builder
COPY /packages/me-front /kearch/packages/me-front
WORKDIR /kearch/packages/me-front
RUN yarn && yarn build-prod


From python:3.6
ARG KEARCH_COMMON_BRANCH="dev"

RUN pip install flask
RUN git clone https://github.com/kearch/kearch
RUN cd /kearch/packages/kearch_common && git checkout $KEARCH_COMMON_BRANCH && pip install -e .

COPY . /kearch/packages/meta_front
COPY --from=builder /kearch/packages/me-front/static/dist /kearch/packages/me-front/static/dist
WORKDIR /kearch/packages/meta_front

# Following 4 lines are for debug.
# COPY ./flask_main.py ./flask_main.py
# COPY ./static ./static
# COPY ./templates ./templates
# CMD python3 flask_main.py
CMD ["python", "-u", "flask_main.py"]
