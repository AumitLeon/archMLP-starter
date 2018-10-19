## ArchMLP Base Infrastructure

This project is meant to serve as a base for ArchMLP development. Containerizing our work via Docker will allow us to match our development and production environments. 

### Requirements
Install docker: https://docs.docker.com/v17.09/engine/installation/

### Usage
Build the image and detach from the container: 
```
docker-compose up --build -d
```

To enter the container and run commands within the container: 
```
docker exec -it arch-starter bash
```

To stop the container: 
```
docker stop arch-starter
```

Docker images can take up a lot of space if not properly removed. To remove any stopped containers and all unused images (not just dangling images):
```
docker system prune -a
```

### Development 
Dependencies should be defined within `deps`. Source files should live in `src`. When the container is built, the `src` directory is mounted to `/var/current/`, the working directory once the container is spun up. 

All source files should live in `src` so as to have them available to run in the container. The `Dockerfile` specifies the steps that Docker takes in spinning up the container. `docker-compose.yml` houses the configurations for the services that define our docker config. 

Deployed python modules should be specified within `deps/python/requirements.txt`. We have a step in the `Dockerfile` that will automatically install these requirments. 

If you want a container to have non-python dependencies, create a sub-directory within `deps` that specifies the type of dependency (i.e. `apt` or `misc` for miscellaneous dependencies), and add an `install.sh` script. 

If for some reason you want the container to have have `emacs`, you would create `deps/misc`, and then create an `install.sh` script with the following;
```
sudo apt-get install emacs
```

When the docker container spins up, the following step will install this dependency: 
```
RUN ls /build/deps | xargs -I % -n 1 sh -c "cd /build/deps/% && sh install.sh" 

```