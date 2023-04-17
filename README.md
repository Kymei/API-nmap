# SCAAS project 🕵🏼:

It is a python API developped with fastAPI that provides endpoints to:
***
* Create Scans
* Get the next scan to launch
* Get the list of scans done by a user
* Get the result of a scan
* Update the scan status
* Update the result of a scan
***

The scan is launched by another program that can run on a different machine (we can have multiple programs running in parallel).
That way, the API is always ready to accept new requests, and the alternatives programs executes the scans. 

### Install Packages
#### As root :
```
apt update
apt install python3 python3-pip python3-venv python-is-python3 curl git
useradd nmap_api
git clone git@gitlab.priv.sewan.fr:rd/scaas-scanner-as-a-service.git /opt
chown -R nmap_api /opt/scaas-scanner-as-a-service
apt install nmap
Dependencies / Virtual environment
```

#### As nmap_api in ```/opt/scaas-scanner-as-a-service``` :
```
python3 -m venv venv
source venv/bin/activate
pip install -U pip
pip install -r requirements.txt
deactivate
Database config
```

#### As root :
```
apt install mariadb-server
systemctl start mariadb
systemctl enable mariadb
sudo mysql_secure_installation
```
Answer N to the first question then Y to the others:

Update the root_password variable in the file ```/opt/scaas-scanner-as-a-service/makefile ```

In the file ```/opt/scaas-scanner-as-a-service/script_help/create_database.sql``` update 'password'
```GRANT ALL ON nmap_scans.* TO 'nmap'@'localhost' IDENTIFIED BY '<password>'```;

In the file ```/opt/scaas-scanner-as-a-service/database.py update``` 'password'
```DB_PASSWORD = "<password>" ```

### Create database :
#### As nmap_api
```
make builddb
```
remove the root_password variable
 
### Service Creation
#### As root in ```/opt/scaas-scanner-as-a-service```:
```
make service
```