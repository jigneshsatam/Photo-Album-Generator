FROM python:alpine3.16

# Installing pip
RUN python -m ensurepip --upgrade

WORKDIR /app

COPY requirements.txt .

# Installing all the requirements
RUN pip install -r requirements.txt

COPY . .

RUN flask --app flaskr init-db

ENTRYPOINT [ "flask" ]

CMD [ "--app", "flaskr", "run", "--host=0.0.0.0", "--debug" ]
