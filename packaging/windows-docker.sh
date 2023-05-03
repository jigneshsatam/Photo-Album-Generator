#!/bin/bash

install_docker() {
winget install --exact --id Docker.DockerDesktop --accept-source-agreements --accept-package-agreements
echo "Docker installed..."
}

if ! command_exists docker; then
  install_docker
fi