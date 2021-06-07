FROM node:12

RUN echo "deb [arch=amd64] http://nginx.org/packages/mainline/ubuntu/ eoan nginx\ndeb-src http://nginx.org/packages/mainline/ubuntu/ eoan nginx" >> /etc/apt/sources.list.d/nginx.list
RUN wget http://nginx.org/keys/nginx_signing.key
RUN apt-key add nginx_signing.key
RUN apt update && apt install -y libasound2 libatk1.0-0 libatk-bridge2.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 libgbm-dev lsb-release xdg-utils wget
RUN apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev wget libbz2-dev
RUN apt-get install -y redis-server

# Create app directory
WORKDIR /app

# python3.7 setup
RUN wget https://www.python.org/ftp/python/3.7.5/Python-3.7.5.tgz
RUN tar -xf Python-3.7.5.tgz
WORKDIR /app/Python-3.7.5
RUN ./configure --enable-optimizations
RUN make -j 8
RUN make altinstall
RUN python3.7 -m pip install --upgrade pip

WORKDIR /app

# dependecies for zerorpc bridge and rasa app
RUN pip3.7 install zerorpc
RUN pip3.7 install celery
RUN pip3.7 install gunicorn
RUN npm install --save zeromq
RUN npm install --save zerorpc
RUN apt-get install -y supervisor

# to make use of caching, copy only package files and install dependencies
COPY package.json .

ADD /chat_assistant /app
ADD /supervisor /app
ADD /core /app
ADD /chat_assistant/requirements.txt /app

# setup postgresql
RUN apt-get install -y postgresql postgresql-contrib postgresql-client
USER postgres
RUN    /etc/init.d/postgresql start &&\
    psql --command "Alter USER postgres WITH SUPERUSER PASSWORD 'admin123456';" &&\
    createdb -O postgres admin123456
RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/9.6/main/pg_hba.conf
RUN echo "listen_addresses='*'" >> /etc/postgresql/9.6/main/postgresql.conf
USER root
# EXPOSE 5432
VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

# python pakages installation
RUN pip3.7 install -r requirements.txt --use-deprecated=legacy-resolver
RUN pip3.7 install git+https://github.com/huggingface/transformers.git
RUN pip3.7 install rasa[spacy]
RUN python3.7 -m spacy download en_core_web_md
RUN python3.7 -m spacy link en_core_web_md en
RUN yarn install --production=false

COPY . .

# copy then compile the code

ENV NODE_ENV=production
ENV PORT=3030

EXPOSE 3030
EXPOSE 8000

CMD ["supervisord","-c","/app/service_script.conf"]
