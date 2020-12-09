#### Katana is a web application developed on Django Web framework that provides a platform for creating, recording, and planning projects as well as generating reports based on those projects. It also lets the user attach relavant files or photos with each peoject and track time spent on each project. It provides selective access to data based on log-in credentials, in order to maintain privacy. Various features such as Milestones, Report Items, Report Item Type, Report Wizards, Time Tracker, Issue Tracker, Workflow, and Notes, utilize JavaScript, CSS, XML, and HTML for front-end UI and PostgreSQL as the database, controlled by Django migrations.

## Instructions for running the application on web browser, from the files included:
## Installing Vagrant

* Go to https://www.vagrantup.com/. This is Vagrant's official website

* Click on Downloads tab or the link provided for downloads

* Select required OS. And it will start the download

* Open downloads and run the setup

* Chose preferences in the setup wizard and start installation

* Download and install VirtualBox from https://www.virtualbox.org/, if you already don't have one

* In Windows you may have to restart the system after the Installation

* Vagrant should be installed
To check if the installation was successful, type the following command in the command Prompt: `vagrant -v`It will display the version of vagrant installed
---



##  Starting vagrant to set up the development environment

* Navigate to the root folder for the project
* Run command `vagrant up`
It will download and setup all the required packages for the project along with setting up the database.
* Once the command is successful ssh into the vagrant box using `vagrant ssh`
* You can now run the server using `/vagrant/manage.py runserver 0:8000`
* Navigate to `0.0.0.0:8000` in browser.

### Credentials for login:

**Username:** admin
**Password:** password123

**Username:** TestUser
**Password:** password123
---

## Dev Server

IP address: 159.89.37.68
Username: katana
Password: GZqN9eboDE7QnFMcVVAdZmsDkBj

Note that password based SSH login has been disabled. To ssh, you should use the keys in this repo (`id_rsa` + `id_rsa.pub`).

Example:  `ssh -i id_rsa katana@159.89.37.68`.
