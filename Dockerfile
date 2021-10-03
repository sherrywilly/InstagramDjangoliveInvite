FROM  python:3

ENV PYTHONUNBUFFERED 1
RUN apt update
# Install dos2unix
RUN apt install dos2unix -y


WORKDIR /app
ADD . /app
COPY ./requirements.txt /app/requirements.txt

RUN pip3 install -r requirements.txt
EXPOSE 8000
COPY . /
COPY entry.sh /entry.sh
COPY connect.sh /connect.sh
# Making sure the script is in unix format
RUN dos2unix /entry.sh /connect.sh

# Fix script Permissions
RUN chmod +x /entry.sh /connect.sh

# Entrypoint
ENTRYPOINT ["/entry.sh"]