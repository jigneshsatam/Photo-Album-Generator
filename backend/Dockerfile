FROM python:alpine3.16

# Installing pip
RUN python -m ensurepip --upgrade

WORKDIR /app

RUN apk add --no-cache gcc musl-dev linux-headers

# ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# EXPOSE 5000

COPY requirements.txt .

# Installing all the requirements
RUN pip install -r requirements.txt

COPY . .

RUN flask --app flaskr init-db

ENTRYPOINT [ "flask" ]

CMD [ "--app", "flaskr", "run" ]
