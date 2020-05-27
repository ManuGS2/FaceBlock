FROM python:3.7-slim
ENV FLASK_APP blockchain_api.py

WORKDIR /server
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD "flask run"