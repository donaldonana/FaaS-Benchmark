#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 1 ]; then

  echo "Usage: $0 <ipv4> <build>"
  echo "ipv4 : ipv4 du swift connection"
  echo "build : Use 'push' or 'pull'. "
  exit 1
fi

build=$1

if [ "$build" != "push" ] && [ "$build" != "pull" ]; then

    echo "Invalid build argument. Expected 'push' or 'pull'."
    exit 1   
fi

if [ "$build" == "push" ]; then

    echo "coming soon"
else

    docker pull onanad/action-python-v3.9:text2speech
    docker pull onanad/action-python-v3.9:conversion
    docker pull onanad/action-python-v3.9:censor

fi

wsk action update text2speech --memory 250 --docker onanad/action-python-v3.9:text2speech speech/__main__.py 
wsk action update conversion  --memory 200 --docker onanad/action-python-v3.9:conversion  conversion/__main__.py  
wsk action update censor      --memory 200 --docker onanad/action-python-v3.9:censor      censor/__main__.py  
