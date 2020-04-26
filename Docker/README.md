# Production Docker Container

## Requirements

The following requirements must be met to install the docker container:<br>
- Docker Installed
- XX GB free space  

**Install Docker**:<br>

Install Docker with your favorite packer manager or from scratch. Details of how to do this are OS dependent, documentation can be found here: https://docs.docker.com/get-docker/

## Installation



**Install PlayBooks Docker Container**:<br>

```shell
git clone git@github.com:csandker/Playbooks.git
cd Playbooks
cd Docker
sudo docker build -t playbooks .
docker run -it -p 8000:8000 playbooks
```

