# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.
  config.vm.box = "ubuntu/xenial64"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # NOTE: This will enable public access to the opened port
  # config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.network "forwarded_port", guest: 8000, host: 8000

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "2048"
  end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  config.vm.provision "shell", inline: <<-SHELL
    set -eu

    sudo apt-get update
    # sudo apt-get -y upgrade

    sudo apt-get install -y postgresql-9.5 python python-dev build-essential python-pip nginx

    cat << EOF | su - postgres -c psql
    CREATE DATABASE djangopilot OWNER postgres;
    ALTER USER postgres WITH PASSWORD 'misstransatlantian';
EOF



    mkdir -p /vagrant/hv/_private_settings
    echo "" > /vagrant/hv/_private_settings/__init__.py
    echo "import os

SECRET_KEY = 'd+7z5a20fqza2i5@_crubf%5j0wj-r925!5tdg&)w#%30wlpfp'

ALLOWED_HOSTS = [
                 '127.0.0.1',
                 'localhost',
                 '0.0.0.0'
                ]

DATABASES = {
              'default': {
                  'ENGINE': 'django.db.backends.postgresql_psycopg2',
                  'NAME': 'djangopilot',
                  'USER': 'postgres',
                  'PASSWORD': 'misstransatlantian',
                  'HOST': 'localhost',
                  'PORT': '',
              }
          }

MEDIA_BASE = os.path.expanduser('~')" > /vagrant/hv/_private_settings/config.py

    sudo -H pip install --upgrade pip
        sudo -H pip install uwsgi

        pip install -r /vagrant/requirements.txt

        python /vagrant/manage.py migrate
        python /vagrant/manage.py loaddata /vagrant/data.json
  SHELL
end
