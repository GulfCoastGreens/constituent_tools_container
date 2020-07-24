FROM python:3.8.3-buster

ARG DIGITALOCEAN_ACCESS_TOKEN
ENV DIGITALOCEAN_ACCESS_TOKEN=${DIGITALOCEAN_ACCESS_TOKEN}

COPY src src
COPY requirements.txt .

RUN pip install -r requirements.txt
# RUN pyinstaller -F src/pyvotertools.py --add-data 'src/florida/sql/*.sql:florida/sql'
# RUN ls -all /dist
# RUN ls /bin
COPY docker-entrypoint.sh /usr/local/bin/
RUN ln -s /usr/local/bin/docker-entrypoint.sh / # backwards compat
ENTRYPOINT ["docker-entrypoint.sh"]
WORKDIR /dist
# RUN ls -all
# CMD ["/dist/pyvotertools"]