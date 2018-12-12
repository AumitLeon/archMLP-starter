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

### Train container
The train script (yet to be converted into a python module) can be run within the base docker container with minimal overhead. From within the container, given a a set of features (x_train) and labels (y_train):
```
python3 train-model.py xs x_train.csv -ys y_train.csv
```

This will produce a binarized represenation of a trained model in a file called `mod.pk`. This is then used by the prediction container. 

### Prediction Container
Thr prediction base container configurations described in this repo are sufficient to run the three primary containers described in our paper. 

In order to run the prediction contianer, spin up and enter the container as described in [Usage](Usage). Once in the contianer, run the initilization script:
```
./initial.sh
```

Activate the new virtual envrionment:
```
source archMLP/bin/activate
```

To run the prediction server:
```
cd predictions/server/
pip install -r requirements.txt
python3 run_server.py
```

To send the contianer predictions, follow the format specifed in predictions/server/instance29.json:
```json
{ 
    "amount": 355294.91,
    "bType": 0,
    "oldBalanceDest": 1392558.34,
    "newBalanceDest": 1747853.25,
    "oldBalanceOrig": 7842.46,
    "newBalanceOrig": 0,
    "errorBalanceOrig": 347452.45,
    "errorBalanceDest": 0
}
```

To get a prediction, execute the following CURL request:
```curl
curl -H "Content-Type: application/json" -X POST --data @instance29.json http://0.0.0.0:5000/predict
```




