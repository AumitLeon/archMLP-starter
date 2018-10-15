FROM ubuntu

RUN apt-get update
RUN apt-get install -y software-properties-common python python-pip curl git

# Make a build directory and sync the project files there
RUN mkdir /build
ADD . /build

# Install dependencies
RUN ls /build/deps | xargs -I % -n 1 sh -c "cd /build/deps/% && sh install.sh" 

# Make a place for the source to live, and copy it there. We don't want it to stay in /build, which will be deleted.
RUN mkdir -p /var/current/
ADD ./src/ /var/current/

# Set working directory 
WORKDIR /var/current

# Clean up build directory
RUN rm -rf /build

# Set the entrypoint
CMD ["bash", "/var/current/test.sh"]
