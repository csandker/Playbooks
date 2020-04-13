# Playbooks

TBA


## Install 

git clone git@github.com:csandker/Playbooks.git
cd Playbooks
virtualenv -p python3 venv
source venv/bin/activate
pip3 install -r requirements.txt
cd App

python3 manage.py migrate

python3 manage.py createsuperuser

> name: admin
> Email: <blank>
> password: nLZnKZhnSoriJ9NopugN

python3 manage.py runserver

http://127.0.0.1:8000/admin/

> Add User
> SampleUser
> SamplePassword
> Save

> ALLOWED FOLDERS ADD
