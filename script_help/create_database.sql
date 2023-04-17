CREATE DATABASE nmap_scans;
GRANT ALL ON nmap_scans.* TO 'nmap'@'localhost' IDENTIFIED BY 'nmap';
FLUSH PRIVILEGES;
