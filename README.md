# Lecture Viewer

### Getting Started
##### Docker
To get started, you first need to install docker. Instructions for installing docker can be found [here](https://docs.docker.com/engine/installation/). After you have docker installed, you will need to install docker compose. Follow the instructions [here](https://docs.docker.com/compose/install/).

##### Clone Recursively
This repo uses [git submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules). In order to clone everything correctly, you have to clone recursively:
```
git clone --recursive https://github.com/stanleyrya/lecture-viewer.git
cd lecture-viewer
```
More useful commands for git submodules can be found in [Repository Maintenence](#repository-maintenance) below.

##### Environment File
This application uses environment variables to make it easier to deploy at different locations. You will need to create a file named ```lecture-viewer.env``` in this directory for deployment to work properly. The following environment variables are used throughout the application:

- ```SIGNING_KEY``` - The key used to sign authentication tokens.

Below is an example of what your ```lecture-viewer.env``` should look like using the above environment variables. ```YOUR_VALUE_HERE``` is simply a placeholder for your own value.
```
SIGNING_KEY=YOUR_VALUE_HERE
```

If you decide to run any services manually, make sure to use the same ```lecture-viewer.env``` file.

### To Run
After your environment is all set up, simply run the following commands:
```
docker-compose build
docker-compose up
```
Everything will be exposed on port 80!

### Repository Maintenance
For those of you who are not using a GUI to interact with git, here are some useful commands:
```
# after checking out a commit (for example git pull master), this updates your submodules
git submodule update --recursive

# if you checked out a commit and it added a new submodule, run this command before doing anything else
# it initializes the submodule so commands like the above one will work
git submodule init

# these commands will pull from master for each submodule
git fetch --recurse-submodules
git submodule foreach git pull origin master
git pull
```

### Troubleshooting
###### "Help! docker-compose says files are missing!"
9 times out of 10 this is due to not updating your submodules when changing commits. Assuming you did a recursive clone of this repo, just run:
```
git submodule update --recursive
```

###### "Help! docker-compose fails at npm install!"
You most likely are running docker on Mac or Windows and have recently switched internet connections. When you switch internet connections while your docker-machine is still running, it looses it's connection. Assuming your docker-machine is called default, run:
```
docker-machine restart default
```

###### "Help! I tried updating my submodules recursively but the submodule folder(s) are empty!"
When a new submodule is added to the system and you would like to pull it onto your machine, you must first init the submodule before you are able to update it.
```
git submodule init
git submodule update --recursive
```


###### I get the following warning
```
WARNING: The MEDIA_DIR variable is not set. Defaulting to a blank string.
```

Create a MEDIA_DIR environment variable
for OSX and Linux put this in your .bashrc or equivalent shell rc
```
export MEDIA_DIR=~/.lv-media
```