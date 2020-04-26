FROM ubuntu:20.04

## CUSTOM CONFIGURATION - PLEASE CHANGE
ARG ADMINPASSWORD="ADMIN!!ChangeME"
ENV PLAYBOOKS_SQLite3PATH="/opt/Playbooks/playbooks.sqlite3"
ENV PLAYBOOKS_PRODUCTION=1
ENV PLAYBOOKS_TIMEZONE="Europe/Berlin"
ENV PLAYBOOKS_SECRET_KEY=""

## STANDARD CONFIGURATION
LABEL name="Playbooks"
ARG DEBIAN_FRONTEND=noninteractive
ARG INSTALL_DIR="/opt"
ARG PLAYBOOKS_DIR="${INSTALL_DIR}/Playbooks"
ARG PLAYBOOK_APP_DIR="${PLAYBOOKS_DIR}/App"
ARG PLAYBOOK_STATIC_DIR="${PLAYBOOK_APP_DIR}/static"
ARG GUNICORN_LOG_DIR="/var/log/gunicorn"
ARG GUNICORN_ACCESS_LOG="${GUNICORN_LOG_DIR}/access.log"

## GLOBAL ENV
ENV PLAYBOOKS_USER="playbooks"
ENV PLAYBOOKS_EXEC_SCRIPT="${PLAYBOOKS_DIR}/run.sh"

# Expose the server port
EXPOSE 8000:8000

### Install tools
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install -y sudo systemd software-properties-common lsb-release nginx python3-pip python3-dev libmysqlclient-dev git net-tools
## mysql-server ufw virtualenv ntpdate

### Configure time based on network
#RUN sudo ntpdate ntp.ubuntu.com
#RUN echo "${TIMEZONE}" > /etc/timezone

# ### Install & Setup MYSQL
# RUN /etc/init.d/mysql restart
# RUN mysqladmin -u root password playbooks
# #RUN echo "mysql-server-5.6 mysql-server/root_password password root" | debconf-set-selections
# #RUN echo "mysql-server-5.6 mysql-server/root_password_again password root" | debconf-set-selections


### Download and install PlayBooks
WORKDIR $INSTALL_DIR
RUN git clone https://github.com/csandker/Playbooks.git
WORKDIR $PLAYBOOKS_DIR
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn
WORKDIR $PLAYBOOK_APP_DIR
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
RUN python3 manage.py collectstatic --noinput
RUN echo "Adding Admin user 'admin' with password: '${ADMINPASSWORD}'"
RUN echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', '', '${ADMINPASSWORD}')" | python3 manage.py shell

### Create User
RUN useradd ${PLAYBOOKS_USER}
RUN adduser ${PLAYBOOKS_USER} www-data
RUN chown -R ${PLAYBOOKS_USER} $PLAYBOOKS_DIR

### Copy Static files (needed to allow nginx serve these files)
# RUN mkdir ${PLAYBOOK_STATIC_DIR}
# RUN cp -r ${PLAYBOOK_APP_DIR}/PlayBooksApp/static/* static/
# RUN cp -r ${PLAYBOOK_APP_DIR}/PlayBooksWeb/static/* static/

### Setup gunicorn
RUN mkdir ${GUNICORN_LOG_DIR}
RUN chown -R root:www-data ${GUNICORN_LOG_DIR}
RUN chmod g+w ${GUNICORN_LOG_DIR}
RUN echo "[Unit]\n\
Description=gunicorn playbooks service\n\
After=network.target\n\
\n\
[Service]\n\
User=${PLAYBOOKS_USER}\n\
Group=www-data\n\
WorkingDirectory=/opt/Playbooks/App/\n\
ExecStart=gunicorn --access-logfile $GUNICORN_ACCESS_LOG --workers 3 --bind unix:/opt/Playbooks/playbooks.sock PlayBooksWeb.wsgi:application\n\
\n\
[Install]\n\
WantedBy=multi-user.target" > /etc/systemd/system/gunicorn_playbooks.service

RUN systemctl enable gunicorn_playbooks.service
#RUN runuser -l ${PLAYBOOKS_USER} -c "gunicorn --access-logfile $GUNICORN_ACCESS_LOG --workers 3 --bind unix:/opt/Playbooks/playbooks.sock PlayBooksWeb.wsgi:application &"
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
RUN systemctl enable nginx
#RUN /etc/init.d/nginx restart

### RUN SCRIPT
RUN echo "#!/bin/sh\n\
echo 'Starting nginx...'\n\
/etc/init.d/nginx restart\n\
echo 'Starting gunicorn as user ${PLAYBOOKS_USER}...'\n\
runuser -l ${PLAYBOOKS_USER} -c 'gunicorn --access-logfile - --workers 3 --bind unix:/opt/Playbooks/playbooks.sock PlayBooksWeb.wsgi:application\n\
" > ${PLAYBOOKS_EXEC_SCRIPT}

### RUN SERVER
#CMD runuser -l ${PLAYBOOKS_USER} -c "gunicorn --access-logfile - --workers 3 --bind unix:/opt/Playbooks/playbooks.sock PlayBooksWeb.wsgi:application &"

CMD ["${PLAYBOOKS_EXEC_SCRIPT}"]