 
#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then

  echo "Usage: $0 <ipv4> <build>"
  echo "ipv4 : ipv4 du swift connection"
  echo "build : Use 'push' or 'pull'. "
  exit 1
fi

ipv4=$1

build=$2

if [ "$build" != "push" ] && [ "$build" != "pull" ]; then

    echo "Invalid build argument. Expected 'push' or 'pull'."
    exit 1   
fi


if [ "$build" == "push" ]; then

    docker build -t action-python-v3.9:proc .
    docker tag action-python-v3.9:proc onanad/action-python-v3.9:proc
    docker push onanad/action-python-v3.9:proc
else

    docker pull onanad/action-python-v3.9:proc
fi



wsk action update proc --docker onanad/action-python-v3.9:proc __main__.py --web true -t 125000 -m 1024

wsk action invoke proc --result --param bib moviepy --param file 1Mb.avi --param ipv4 $ipv4


 