FROM python:alpine3.7
COPY /parsing /parsing
WORKDIR /parsing
RUN pip install -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/."
CMD python /parsing/main.py