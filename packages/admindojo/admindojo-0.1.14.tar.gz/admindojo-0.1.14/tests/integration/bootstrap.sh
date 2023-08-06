#!/usr/bin/env bash
# install inspec
apt update

cd /tmp
git clone https://github.com/rfrail3/tuptime.git
cd tuptime
bash tuptime-install.sh

apt install -y python3-pip


# add inspec alias
echo "alias admindojo=\"admindojo\"" >> /home/vagrant/.bashrc
