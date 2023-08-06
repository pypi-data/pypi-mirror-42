# A Docker Universal Control Plane CLI 

[![asciicast](https://asciinema.org/a/05qkp37lroHzKcfxRfu60scGD.png)](https://asciinema.org/a/05qkp37lroHzKcfxRfu60scGD)


This `ucp-cli login` command will download your user bundle and auth token into the ~/.ucp directory.
With `eval $(ucp-cli env)` you can then access the docker or kubectl context.

Reference: https://docs.docker.com/ee/ucp/user-access/cli/


## Installation

Run the following to install:

```
$ pip install python-ucp-cli

$ eval $(ucp-cli env)

$ docker node ls
...
$ kubectl get node
...

```

## Usage

```bash

$ ucp-cli login --username user1 --password S3cretPassword12345 --url ucp-manager.local

$ eval $(ucp-cli env)

$ docker node ls
...

$ kubectl get node
...

```


## Developer

```
virtualenv venv
ls venv/
. venv/bin/activate
which python

pip install --editable .
```



### Get Started

For usage and help content, pass in the `-h` parameter, for example:

