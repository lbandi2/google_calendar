# FROM python:3.13-slim
FROM python:3.13-alpine

WORKDIR /app

COPY ./requirements.txt /app

RUN pip install --no-cache-dir --upgrade -r requirements.txt

ENV TZ="America/Bogota"

COPY . /app

# each space of the command is its own item in the list
# port is internal docker port so to run the image specify -p <desired_port>:<internal_port>
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
