FROM ubuntu:20.04

## CUSTOM CONFIGURATION - PLEASE CHANGE
ARG ADMINPASSWORD="ADMIN!!ChangeME"
## DEFAULT DB PATH INSIDE CONTAINER
#ENV PLAYBOOKS_SQLITE3_PATH="/opt/Playbooks/App/playbooks.sqlite3"
## UNCOMMENT FOR AN OUTSIDE DOCKER DB, NOTE: The '/data' path is inside Docker so you're good to leave it with /data (can be changd though)
ENV PLAYBOOKS_SQLITE3_PATH="/data/playbooks.sqlite3"
ENV PLAYBOOKS_PRODUCTION=1
ENV PLAYBOOKS_TIMEZONE="Europe/Berlin"
ENV PLAYBOOKS_SECRET_KEY="TFcnpdctBlH8V9c1UkUl"

## STANDARD CONFIGURATION
LABEL name="Playbooks"
ARG DEBIAN_FRONTEND=noninteractive
ARG INSTALL_DIR="/opt"
ARG PLAYBOOKS_DIR="${INSTALL_DIR}/Playbooks"
ARG PLAYBOOK_APP_DIR="${PLAYBOOKS_DIR}/App"
ARG PLAYBOOK_SETTINGS_JSON="${PLAYBOOK_APP_DIR}/settings.json"
ARG PLAYBOOK_STATIC_DIR="${PLAYBOOK_APP_DIR}/static"
ARG GUNICORN_LOG_DIR="/var/log/gunicorn"
ARG GUNICORN_ACCESS_LOG="${GUNICORN_LOG_DIR}/access.log"

## GLOBAL ENV
ENV PLAYBOOKS_USER="playbooks"
ENV PLAYBOOKS_EXEC_SCRIPT="${PLAYBOOKS_DIR}/run.sh"

### Install tools
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install -y sudo systemd software-properties-common lsb-release nginx python3-pip python3-dev libmysqlclient-dev git net-tools

### Download and install PlayBooks
WORKDIR $INSTALL_DIR  
RUN git clone -b Dockerise https://github.com/csandker/Playbooks.git
WORKDIR $PLAYBOOKS_DIR
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn
WORKDIR $PLAYBOOK_APP_DIR
RUN python3 manage.py collectstatic --noinput

## PlayBooks Settings
RUN echo "{\n\
    \"SECRET_KEY\": \"${PLAYBOOKS_SECRET_KEY}\",\n\
    \"PROD_ENV\": \"${PLAYBOOKS_PRODUCTION}\",\n\
    \"SQLITE3_PATH\": \"${PLAYBOOKS_SQLITE3_PATH}\",\n\
    \"ALLOWED_HOSTS\": \"*\"\n\
}" > ${PLAYBOOK_SETTINGS_JSON}

### Create User
RUN useradd ${PLAYBOOKS_USER}
RUN adduser ${PLAYBOOKS_USER} www-data
RUN chown -R ${PLAYBOOKS_USER} $PLAYBOOKS_DIR

### Setup gunicorn
RUN mkdir ${GUNICORN_LOG_DIR}
RUN chown -R root:www-data ${GUNICORN_LOG_DIR}
RUN chmod g+w ${GUNICORN_LOG_DIR}

### SYSTEMD Usage - Skipped for Docker
# RUN echo "[Unit]\n\
# Description=gunicorn playbooks service\n\
# After=network.target\n\
# \n\
# [Service]\n\
# User=${PLAYBOOKS_USER}\n\
# Group=www-data\n\
# WorkingDirectory=/opt/Playbooks/App/\n\
# ExecStart=gunicorn --access-logfile $GUNICORN_ACCESS_LOG --workers 3 --bind unix:/opt/Playbooks/playbooks.sock PlayBooksWeb.wsgi:application\n\
# \n\
# [Install]\n\
# WantedBy=multi-user.target" > /etc/systemd/system/gunicorn_playbooks.service

#RUN systemctl enable gunicorn_playbooks.service
#RUN systemctl start gunicorn_playbooks.service

### Setup Nginx
RUN echo "server {\n\
    listen 8000;\n\
    server_name 127.0.0.1;\n\
    location = /favicon.ico {access_log off;log_not_found off;}\n\ 
\n\
    location /static/ {\n\
        root $PLAYBOOK_APP_DIR;\n\    
    }\n\
\n\
    location / {\n\
        include proxy_params;\n\
        proxy_pass http://unix:/opt/Playbooks/playbooks.sock;\n\
    }\n\
}\n\
" > /etc/nginx/sites-available/playbooks

RUN ln -s /etc/nginx/sites-available/playbooks  /etc/nginx/sites-enabled/
## SYSTEMD Usage -- Skipped For Docker
#RUN systemctl enable nginx

### RUN SCRIPT
RUN echo "#!/bin/sh\n\
cd ${PLAYBOOK_APP_DIR}\n\
echo 'Setting Up PlayBooks DB...' \n\
#python3 manage.py makemigrations\n\
python3 manage.py migrate\n\
echo \"Adding Admin user 'admin' with password: '${ADMINPASSWORD}'\"\n\
echo \"from django.contrib.auth import get_user_model; User = get_user_model(); print('Admin user already exists. Moving on...') if User.objects.filter(username='admin').count()>0 else User.objects.create_superuser('admin', '', '${ADMINPASSWORD}')\" | python3 manage.py shell\n\
echo 'Adding Write Acces for everyone to ${PLAYBOOKS_SQLITE3_PATH}'\n\
chmod o+w ${PLAYBOOKS_SQLITE3_PATH}\n\
echo 'Starting nginx...'\n\
/etc/init.d/nginx restart\n\
echo 'Starting gunicorn as user ${PLAYBOOKS_USER}...'\n\
runuser -l ${PLAYBOOKS_USER} -c 'gunicorn --access-logfile - --workers 3 --bind unix:/opt/Playbooks/playbooks.sock PlayBooksWeb.wsgi:application'" > ${PLAYBOOKS_EXEC_SCRIPT}
RUN chmod +x ${PLAYBOOKS_EXEC_SCRIPT}

# Expose the server port
EXPOSE 8000:8000

### RUN SERVER
CMD ["/opt/Playbooks/run.sh"]
