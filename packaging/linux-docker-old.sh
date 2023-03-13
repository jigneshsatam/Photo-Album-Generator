#!/bin/bash

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

version=4.17.0
arch=amd64

# 4. Download deb
wget https://desktop.docker.com/linux/main/amd64/docker-desktop-$version-$arch.deb


# 5. Install deb
sudo apt-get -y update
sudo apt-get -y install ./docker-desktop-$version-$arch.deb

# 6. Launch
systemctl start docker
