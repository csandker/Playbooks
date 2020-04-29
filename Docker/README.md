# Production Docker Container

## Requirements

The following requirements must be met to install the docker container:<br>
- Docker installed (Documentation can be found here: https://docs.docker.com/get-docker/)
- 1GB free space  


## Installation



**Install PlayBooks Docker Container**:

Check out the Dockerfile for configurable settings.<br>
**Notice**: If you want to have your database outside the docker container (which makes sense for the long run), edit the Dockerfile and change the following line ```ENV PLAYBOOKS_SQLITE3_PATH="/data/playbooks.sqlite3"``` (this will be the path within the docker container, read below for how this works)


```shell
git clone git@github.com:csandker/Playbooks.git
cd Playbooks/Docker
sudo docker build -t playbooks .
## If you  want the DB will inside the Docker container
sudo docker run -it -p 8000:8000/tcp -v /tmp:/data playbooks
## If you specified a local path for your DB, make the DB available by using Volumes 
## Example: you specified '/data/playbooks.sqlite3' as your DB location, map /data to a local path by using docker Volumes (-v)
## In the example below your local /tmp dir will be mapped to the container's /data dir 
sudo docker run -it -p 8000:8000/tcp -v /tmp:/data playbooks
```


