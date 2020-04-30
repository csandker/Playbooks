# Production Docker Container

## Requirements

The following requirements must be met to install the docker container:<br>
- Docker installed (Documentation can be found here: https://docs.docker.com/get-docker/)
- 1GB free space  


## Installation

**Before building the Docker container, you must decide whether you want to have the PlayBooks database wihtin the docker container or outside of it**.<br>
Having the DB inside means, it will get deleted once the docker container gets delted.<br>

**Building With DB inside the Docker Container**:

```shell
git clone https://github.com/csandker/Playbooks.git
cd Playbooks/Docker
## Check out the Dockerfile, for configurable settings e.g. the SECRET KEY or PRODUCTION deployment (relevant for error messages)
## nano|vim|whatever Dockerfile; edit  "ADMINPASSWORD" , "PLAYBOOKS_PRODUCTION", "PLAYBOOKS_SECRET_KEY", ...
sudo docker build -t playbooks .
## If you  want the DB will inside the Docker container
sudo docker run -it -p 8000:8000/tcp --name playbooks playbooks
```

Find Playbooks at http://127.0.0.1:8000/

**Building With DB inside the Docker Container**:

If you want to have your database outside the docker container (which makes sense for the long run), edit the Dockerfile and change the following line ```ENV PLAYBOOKS_SQLITE3_PATH="/data/playbooks.sqlite3"``` (this will be the path within the docker container, read below for how this works)

```shell
git clone https://github.com/csandker/Playbooks.git
cd Playbooks/Docker
nano Dockerfile ## change "PLAYBOOKS_SQLITE3_PATH" and other keys such as "PLAYBOOKS_PRODUCTION", "PLAYBOOKS_SECRET_KEY", ...
sudo docker build -t playbooks .
## Example: you specified '/data/playbooks.sqlite3' as your DB location, map /data to a local path by using docker Volumes (-v)
## In the example below your local /tmp dir will be mapped to the container's /data dir 
## Please note the DB that will be created at your local path will be made world-readable. It needs to be cause the docker user running the application is not existing on your local System. 
sudo docker run -it -p 8000:8000/tcp -v /tmp:/data --name playbooks playbooks ## Note that /data the endpoint defined in the Dockerfile
```

Find Playbooks at http://127.0.0.1:8000/

**Restart a stopped/exited docker container**:

```shell
sudo docker start -ai playbooks
```