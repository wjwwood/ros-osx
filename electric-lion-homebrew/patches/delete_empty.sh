#!/usr/bin/env bash

for file in *;
  do
    file_size=$(du $file | awk '{print $1}');
    if [ $file_size == 0 ]; then
      echo "Deleting empty file $file with file size $file_size.";
      echo "rm -f $file";
      rm -f $file
    fi;
  done
