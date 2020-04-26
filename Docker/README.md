# Production Docker Container

## Requirements

The following requirements must be met to install the docker container:<br>
- Docker installed (Documentation can be found here: https://docs.docker.com/get-docker/)
- XX GB free space  


## Installation



**Install PlayBooks Docker Container**:<br>

```shell
git clone git@github.com:csandker/Playbooks.git
cd Playbooks/Docker
sudo docker build -t playbooks .
docker run -it -v /tmp:/data playbooks ##-p 8000:8000 
```

