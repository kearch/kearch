FROM node:8-alpine as builder
COPY /packages/sp-front /kearch/packages/sp-front
WORKDIR /kearch/packages/sp-front
RUN yarn && yarn build-prod


From python:3.6
ARG KEARCH_COMMON_BRANCH="dev"

RUN pip install flask

COPY packages/kearch_common /kearch/packages/kearch_common
RUN cd /kearch/packages/kearch_common && pip install -e .

COPY /packages/sp-front /kearch/packages/sp-front
COPY --from=builder /kearch/packages/sp-front/static/dist /kearch/packages/sp-front/static/dist
WORKDIR /kearch/packages/sp-front

# Following 4 lines are for debug.
# COPY ./flask_main.py ./flask_main.py
# COPY ./static ./static
# COPY ./templates ./templates
# CMD python3 flask_main.py
CMD ["python", "-u", "flask_main.py"]
