FROM python:3.10

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY exporter.py .

CMD "python3" "-u" "./exporter.py"
