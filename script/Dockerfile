FROM python:3.10-alpine

COPY ../requirements.txt /requirements.txt

RUN pip install -r requirements.txt

COPY . ./testy

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /testy

#ENTRYPOINT [ "python" ]
ENV PYTHONPATH /testy

#CMD ["cd","bot" ]
CMD ["python","script/run_script.py" ]
#CMD ["ls"]

