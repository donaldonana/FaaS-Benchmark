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
    docker pull onanad/action-python-v3.9:profanity
fi

# demo package for web action
wsk package update demo
# text to speech acion
wsk action update guest/demo/text2speech --docker onanad/action-python-v3.9:text2speech speech/__main__.py --web true
# conversion acion
wsk action update guest/demo/conversion --docker onanad/action-python-v3.9:conversion conversion/__main__.py  --web true
# profanity acion
wsk action update guest/demo/profanity --docker onanad/action-python-v3.9:profanity profanity/__main__.py --web true 
# Sequence S2: text2speech--->conversion
wsk action update guest/demo/S2  --sequence demo/text2speech,demo/conversion  --web true
# censor acion
wsk action update censor --docker onanad/action-python-v3.9:censor   censor/__main__.py  
# coordinator acion
wsk action update coord coordinator/__main__.py

