#!/bin/bash

install_docker() {

}

command_exists() {
	command -v "$@" > /dev/null 2>&1
}

docker_running() {
  "$@" > /dev/null 2>&1
}

if ! command_exists docker; then
  install_docker
fi

if ! docker_running docker ps; then
  echo "Starting docker..."
  open -a "/Applications/Docker Desktop"
  echo "Docker started..."
fi
