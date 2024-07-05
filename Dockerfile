FROM python:3.10.8-slim

RUN apt-get update && apt-get install -y \
    pkg-config \
    gcc \
    python3-dev \
    default-libmysqlclient-dev

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
LABEL name=chaitanyabeemanaboina_chatapp
ENV mysql_config=/usr/bin/mysql_config

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]