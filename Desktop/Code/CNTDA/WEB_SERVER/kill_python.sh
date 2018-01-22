#!/bin/bash

query="$(lsof -i | grep Python)"

count=0
pid=0
for item in $query
do
  if [ $count -eq 1 ]; then
    pid=$item
  fi
  ((count = count + 1)) 
done

kill -9 $pid
