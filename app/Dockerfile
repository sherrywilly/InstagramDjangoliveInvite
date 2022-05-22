FROM node:16.15.0
RUN apt install g++ make python
WORKDIR /src
COPY ./app /src
COPY ./entry.sh /src
# RUN npm install
EXPOSE 3001
# RUN chmod +x /src/entry.sh
# ENTRYPOINT ["sh", "/src/entry.sh"]

