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
Dependencies should be defined within `deps`. Source files should live in `src`. When the container is built, the `src` directory is mounted to `/var/current/`, the working directory once the container is spun up. Any files 