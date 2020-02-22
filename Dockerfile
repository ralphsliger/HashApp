
FROM python:3.7.4-alpine

WORKDIR /app # Docker creates this for you

COPY requirements.txt .

RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
 && pip install cython \
 && pip install -r requirements.txt --default-timeout=100 future \
 && apk del .build-deps

COPY . .


CMD ["python3", "src/app.py"]