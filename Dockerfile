FROM python:3.12-alpine

WORKDIR /app

RUN apk add --no-cache postgresql-client

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /app
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
