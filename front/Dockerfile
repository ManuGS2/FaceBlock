FROM python:3.7-slim
ENV FLASK_APP face_view.py

WORKDIR /front
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD "flask run"