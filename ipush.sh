#!/bin/bash

git add --all
echo $1
if [ "$1" = "" ]; then
	git commit -m 'default'
else
	git commit -m "$1"
fi
git push
