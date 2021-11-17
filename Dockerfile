FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY Flask_App .

# Ensure directory is writeable by root group
RUN chgrp -R 0 . && chmod -R +060 .

ENV FLASK_APP=app.py

USER 1001

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
