FROM python:3.7-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt update

RUN apt install make
RUN apt install libpq-dev gcc -y
RUN apt install ghostscript -y
RUN apt install libglib2.0-0  -y
# Install dos2unix
RUN apt install dos2unix -y

# Add new user
RUN groupadd -r instadjango && useradd -r -g instadjango instadjango


WORKDIR /app
ADD . /app
COPY ./requirements.txt /app/requirements.txt

RUN pip3 install -r requirements.txt
EXPOSE 8000
COPY . /
COPY entrypoint.sh /entrypoint.sh
COPY connect.sh /connect.sh
RUN dos2unix /entrypoint.sh /connect.sh
RUN chmod +x /entrypoint.sh /connect.sh

# Entrypoint
ENTRYPOINT ["sh", "/entrypoint.sh"]