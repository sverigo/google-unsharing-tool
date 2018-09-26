#!/bin/sh

if [ -n "$1" ]
then
export EMAIL_ADDRESS=$1
python3 unsharing_tool.py
else
echo "Set email as a parameter"
fi
