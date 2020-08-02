FROM python:3.8.3-buster

COPY src src
COPY requirements.txt .

RUN apt-get update && apt-get -y install netcat
RUN pip install -r requirements.txt
RUN pyinstaller -F src/constituent_tools.py --add-data 'src/florida/sql/*.sql:florida/sql'
# RUN ls -all /dist
# RUN ls /bin
COPY docker-entrypoint.sh /usr/local/bin/
RUN ln -s /usr/local/bin/docker-entrypoint.sh / # backwards compat
ENTRYPOINT ["docker-entrypoint.sh"]
# ENTRYPOINT ["/bin/cp"]
WORKDIR /dist
# RUN ls -all
#CMD ["/dist/constituent_tools"]
CMD ["tail","-f","/dev/null"]