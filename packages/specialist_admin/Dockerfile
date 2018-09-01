From python:3.6

RUN pip install flask
RUN git clone https://github.com/kearch/kearch
RUN cd /kearch/packages/kearch_common && pip install -e .

# Following lines are for debug.
# COPY flask_main.py .
# COPY specialist_admin.py .
# RUN mkdir templates
# COPY templates/* templates/

WORKDIR /kearch/packages/specialist_admin

CMD ["python", "-u", "flask_main.py"]
