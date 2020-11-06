# Katana Deployment


## Update Packages

You can do this by connecting to your server via SSH and running the following commands:

```bash
 sudo apt-get update
 sudo apt-get upgrade
```
 
 The first command downloads any updates for packages managed through apt-get.
 The second command installs the updates that were downloaded. After running the above commands, 
 if there are updates to install you will likely be prompted to indicate whether or not you want to install these updates. 
 If this happens, just type "y" and then hit "enter" when prompted.
 
## Install Dependencies
 
 To install the required dependencies run the following command
 
```bash
 sudo apt-get --assume-yes install postgresql postgresql-contrib postgresql-client python-pip python-dev nginx
 sudo -H pip install --upgrade pip
 sudo -H pip install virtualenv virtualenvwrapper uwsgi
```

The above command will install postgres database, python and nginx

## Create a Database

To create a database with PostgreSQL start by running the following command:

```bash
sudo su - postgres
```

Your terminal prompt should now say "postgres@yourserver". If so, run this command to create your database, making sure to replace "mydb" with your desired database name:

Now create your database user with the following command:
```sql
CREATE DATABASE djangopilot OWNER postgres;
ALTER USER postgres WITH PASSWORD 'misstransatlantian';
```

You are now set with a database and a user to access that database. 

## Set Up Your Virtualenv

Run the following commands:
```bash
echo "export WORKON_HOME=~/venvs" >> ~/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
```
Now, source your shell initialization script so that you can use this functionality in your current session:
```bash
source ~/.bashrc
```
 
 To create your virtualenv run the following command, replace `user` with the logged in user:
```bash
mkvirtualenv katana
```

## Move Django Project to Droplet

Copy the source from your local machine over `ssh` using `rsync`:

```bash
rsync -azPh --delete --exclude ".git" -e "ssh -o StrictHostKeyChecking=no" ./ <user>@<ip_address>:~/katana/
```

Find the directory where you set up your virtualenv. Change into this directory with the following command to see source:

```bash
cd /home/<user>/katana
```
Run the following command to install the application requirements:

```bash
pip install -r requirements.txt
```
Next, run the following command is to run the migration:

```bash
python manage.py migrate
python manage.py loaddata data.json
``` 

## Backing Out of the Virtual Environment

Since we are done working on Django portion, we can deactivate our virtual environment:
```bash
deactivate
```

If you need to work on katana, you can do that by using the following command:
```bash
workon katana
```

Again, deactivate when you are finished working on your sites:
```bash
deactivate
```

## Nginx Setup

run the following command to create and edit your site's web server configuration file:

```bash
sudo nano /etc/nginx/sites-available/katana
```

Now enter the following lines of code into the open editor, replace `user` with the logged in user:

```nginx
server {
    listen 80;
    server_name <ip_adress>;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/<user>/katana;
    }
    location /media/ {
        root /home/<user>/;
    }

    location / {
        include         uwsgi_params;
        uwsgi_pass      unix:/run/uwsgi/katana.sock;
    }
}
``` 
Save and exit the file.

Now we need to set up a symbolic link in the /etc/nginx/sites-enabled directory that points to this configuration file. That is how NGINX knows this site is active. Change directories to /etc/nginx/sites-enabled like this:

```bash
cd /etc/nginx/sites-enabled
```

Once there, run this command:

```bash
sudo ln -s ../sites-available/katana
```

Now restart NGINX with the command below and you should be set:

```bash
sudo service nginx restart
```

You may see the following error upon restart:
```bash
server_names_hash, you should increase server_names_hash_bucket_size: 32
```

You can resolve this by editing ` /etc/nginx/nginx.conf `

Open the file and uncomment the following line:

```bash
server_names_hash_bucket_size 64;
```

## Hosting the application

Run the following to command to start the uwisgi server:

```bash
sudo systemctl restart uwsgi
```





