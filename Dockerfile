FROM python:3.9

WORKDIR /

RUN apt-get update
RUN pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src src
COPY tests src

RUN pytest src/

CMD sleep 15
CMD ["python", "src/run.py"]
