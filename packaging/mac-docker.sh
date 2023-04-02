#!/bin/bash

# install_docker() {

# }

# command_exists() {
# 	command -v "$@" > /dev/null 2>&1
# }

# docker_running() {
#   "$@" > /dev/null 2>&1
# }

# if ! command_exists docker; then
#   install_docker
# fi

# if ! docker_running docker ps; then
#   echo "Starting docker..."
#   open -a "Docker"
#   echo "Docker started..."
# fi


echo "Starting Docker for Mac...";

open --background --hide -a Docker;

while [[ -z "$(! docker stats --no-stream 2> /dev/null)" ]];
  do echo ".";
  sleep 1
done

sleep 5

echo "";
