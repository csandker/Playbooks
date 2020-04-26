FROM ubuntu:20.04
LABEL name="Playbooks"
ARG DEBIAN_FRONTEND=noninteractive
ARG INSTALL_DIR="/opt"
ARG PLAYBOOKS_DIR="${INSTALL_DIR}/Playbooks"
ARG PLAYBOOK_APP_DIR="${PLAYBOOKS_DIR}/App"
ARG PLAYBOOK_STATIC_DIR="${PLAYBOOK_APP_DIR}/static"
ARG GUNICORN_LOG_DIR="/var/log/gunicorn"
ARG GUNICORN_ACCESS_LOG="${GUNICORN_LOG_DIR}/access.log"

## Global ENV
ENV PLAYBOOKS_PRODUCTION=1

RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install -y sudo systemd software-properties-common lsb-release nginx mysql-server python3-pip python3-dev libmysqlclient-dev git ntpdate
## ufw virtualenv

### Configure time based on network
#RUN sudo ntpdate ntp.ubuntu.com

### Download and install PlayBooks
WORKDIR $INSTALL_DIR
RUN git clone https://github.com/csandker/Playbooks.git
WORKDIR $PLAYBOOKS_DIR
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn
WORKDIR $PLAYBOOK_APP_DIR
#RUN python3 manage.py migrate

### Create User
RUN useradd playbooks
RUN adduser playbooks www-data
RUN chown -R playbooks $PLAYBOOKS_DIR

### Copy Static files (needed to allow nginx serve these files)
RUN mkdir ${PLAYBOOK_STATIC_DIR}
RUN cp -r ${PLAYBOOKS_DIR}/PlayBooksApp/static/* static/
RUN cp -r ${PLAYBOOKS_DIR}/PlayBooksWeb/static/* static/

### Setup gunicorn
RUN mkdir GUNICORN_LOG_DIR
RUN printf "
[Unit]
Description=gunicorn playbooks service
After=network.target
   
[Service]
User=playbooks
Group=www-data
WorkingDirectory=/opt/Playbooks/App/
ExecStart=gunicorn --access-logfile ${GUNICORN_LOG_DIR} --workers 3 --bind unix:/opt/Playbooks/playbooks.sock PlayBooksWeb.wsgi:application

[Install]
WantedBy=multi-user.target\n" | tee /etc/systemd/system/gunicorn_playbooks.service

RUN systemctl enable gunicorn_playbooks.service
RUN gunicorn --access-logfile ${GUNICORN_LOG_DIR} --workers 3 --bind unix:/opt/Playbooks/playbooks.sock PlayBooksWeb.wsgi:application &
#RUN systemctl start gunicorn_playbooks.service

### Setup Nginx
RUN printf "
server {
    listen 8000;
    server_name 127.0.0.1;
    location = /favicon.ico {access_log off;log_not_found off;} 

    location /static/ {
        root ${PLAYBOOK_APP_DIR};    
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/opt/Playbooks/playbooks.sock;
    }
}
" | tee /etc/nginx/sites-available/playbooks

RUN ln -s /etc/nginx/sites-available/playbooks  /etc/nginx/sites-enabled/

### Expose the server port
EXPOSE 8000:8000