# not slim because we need github depedencies
# FROM node:lts-buster
# FROM docker:dind
FROM node:12

RUN echo "deb [arch=amd64] http://nginx.org/packages/mainline/ubuntu/ eoan nginx\ndeb-src http://nginx.org/packages/mainline/ubuntu/ eoan nginx" >> /etc/apt/sources.list.d/nginx.list
RUN wget http://nginx.org/keys/nginx_signing.key
RUN apt-key add nginx_signing.key
RUN apt update && apt install -y libasound2 libatk1.0-0 libatk-bridge2.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 libgbm-dev lsb-release xdg-utils wget
RUN apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev wget libbz2-dev
RUN apt-get install -y redis-server

# RUN apt-get install -y supervisor

# Create app directory
WORKDIR /app

# to make use of caching, copy only package files and install dependencies
COPY package.json .

ADD /chat_assistant /app
ADD /supervisor /app
ADD /core /app
ADD /chat_assistant/requirements.txt /app

# RUN apt-get update || : && apt-get install python -y
# RUN apt-get install python -y
# RUN apt-get install python3-pip -y

# RUN apt-get install software-properties-common -y
# RUN add-apt-repository ppa:deadsnakes/ppa   
# RUN apt install python3.7

RUN wget https://www.python.org/ftp/python/3.7.4/Python-3.7.4.tgz
RUN tar -xf Python-3.7.4.tgz

RUN ls

WORKDIR /app/Python-3.7.4

RUN ./configure --enable-optimizations
RUN make -j 8
RUN make altinstall
RUN python3.7 -m pip install --upgrade pip

WORKDIR /app

RUN pip3 install zerorpc
RUN npm install zerorpc
RUN apt-get install -y gunicorn
RUN apt-get install \
	gcc nano \
	postgresql postgresql-contrib -y
RUN apt-get install -y postgresql supervisor
RUN pip3 install -r requirements.txt --use-deprecated=legacy-resolver



# setup postgresql

ADD /scripts/set-psql-password.sh /tmp/set-psql-password.sh
RUN /bin/sh /tmp/set-psql-password.sh
RUN sed -i "/^#listen_addresses/i listen_addresses='*'" /etc/postgresql/9.1/main/postgresql.conf
RUN sed -i "/^# DO NOT DISABLE\!/i # Allow access from any IP address" /etc/postgresql/9.1/main/pg_hba.conf
RUN sed -i "/^# DO NOT DISABLE\!/i host all all 0.0.0.0/0 md5\n\n\n" /etc/postgresql/9.1/main/pg_hba.conf

# set root password
RUN echo "root:root" | chpasswd                        
# clean packages
RUN apt-get clean
RUN rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/*

# expose postgresql port
# EXPOSE 22 5432

# volumes
VOLUME ["/var/lib/postgresql/9.1/main"]



#RUN  yarn ci --verbose  # we should make lockfile or shrinkwrap then use yarn ci for predictable builds
RUN yarn install --production=false

COPY . .

# copy then compile the code

ENV NODE_ENV=production
ENV PORT=3030

EXPOSE 3030
EXPOSE 8000
EXPOSE 8085

# CMD ["scripts/start-bot.sh"]
CMD ["supervisord","-c","/app/service_script.conf"]
