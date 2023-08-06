#!/bin/bash

pip install python-ucp-cli

export UCP_USERNAME=username
export UCP_PASSWORD=password
export UCP_URL=https://ucp.localdomain

ucp-cli login -u $UCP_USERNAME -p $UCP_PASSWORD --url $UCP_URL

eval $(ucp-cli env)
