# You must build this Dockerfile at project root.
# > docker build -f packages/specialist_admin/Dockerfile .
From python:3.6

RUN pip install flask

COPY packages/kearch_common /kearch/packages/kearch_common
RUN cd /kearch/packages/kearch_common && pip install -e .

COPY /packages/specialist_admin /kearch/packages/specialist_admin
WORKDIR /kearch/packages/specialist_admin

CMD ["python", "-u", "flask_main.py"]
