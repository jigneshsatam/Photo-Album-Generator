#!/bin/bash

install_docker() {

# dpkg -l | grep -i docker
# sudo apt-get purge -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras docker-scan-plugin

# 0. Uninstall old version
# sudo apt-get remove docker docker-engine docker.io containerd runc docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin dockerd-rootless

# sudo apt-get purge -y docker docker-engine docker.io containerd runc docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin dockerd-rootless docker-ce-rootless-extras docker-scan-plugin

# sudo apt-get purge -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras docker-scan-plugin

# sudo apt-get autoremove -y --purge docker-ce docker-ce-rootless-extras docker-scan-plugin


# 1. Update the apt package index and install packages to allow apt to use a repository over HTTPS:
sudo apt-get update

sudo apt-get -y install \
  ca-certificates \
  curl \
  gnupg \
  lsb-release

# 2. Add Docker’s official GPG key:
sudo mkdir -m 0755 -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor --yes -o /etc/apt/keyrings/docker.gpg

# 3. Use the following command to set up the repository:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# version=4.17.0
# arch=amd64

# # 4. Download deb
# wget https://desktop.docker.com/linux/main/amd64/docker-desktop-$version-$arch.deb

# 4. Update the apt package index:
sudo chmod a+r /etc/apt/keyrings/docker.gpg
sudo apt-get update


# # 5. Install deb
# sudo apt-get -y update
# sudo apt-get -y install ./docker-desktop-$version-$arch.deb

# 5. Install Docker Engine, containerd, and Docker Compose.
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# # 6. Launch
# systemctl start docker

# 6. Create the docker group.
sudo groupadd docker

# 7. Add your user to the docker group.
sudo usermod -aG docker $USER

# 8. Log out and log back in so that your group membership is re-evaluated.
newgrp docker

# 9. Verify that you can run docker commands without sudo.
# docker run hello-world
echo "Docker installed..."
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
  sudo systemctl stop docker.service
  sudo systemctl stop docker
  sudo systemctl stop docker.socket
  sudo systemctl start docker
  echo "Docker started..."
fi

# 9. start docker
