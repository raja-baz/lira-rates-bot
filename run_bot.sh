#!/bin/sh

while [[ 1 ]]
do
  python3 bot.py
  if [[ $? != 5 ]]
  then
    exit
  fi
done

