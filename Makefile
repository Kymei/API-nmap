# ==================== VARIABLES ====================
ip_server =
root_password = 
# ==================== END VARIABLES ====================


# ==================== COLORS  ====================

GR	= \033[32;1m	# Green
RE	= \033[31;1m 	# Red
YE	= \033[33;1m 	# Yellow
CY	= \033[36;1m 	# Cyan
PU  = \033[35;1m    # Purple
RC	= \033[0m 		# Reset Colors

# ==================== END COLORS  ====================


# ==================== RULES ====================

# default: install


startdb:
	@echo "$(PU)#############  Starting the database  #############$(RC)"
	sudo /etc/init.d/mysql start

stopdb:
	@echo "$(PU)#############  Stoping the database  #############$(RC)"
	sudo /etc/init.d/mysql stop

builddb:
	@echo "$(GR)&&&&&&&&&&&&&&&&&&&& Build the database &&&&&&&&&&&&&&&&&&&&$(RC)"
	mysql -u root -p$(root_password) < script_help/create_database.sql
	alembic revision --autogenerate -m "Initial commit"
	alembic upgrade head

deletedb:
	@echo "$(GR)&&&&&&&&&&&&&&&&&&&& Build the database &&&&&&&&&&&&&&&&&&&&$(RC)"
	mysql -u root -p$(root_password) < script_help/remove.sql
	rm -rf /opt/scaas-scanner-as-a-service/alembic/versions/*

resetdb:
	@echo "$(GR)&&&&&&&&&&&&&&&&&&&& Build the database &&&&&&&&&&&&&&&&&&&&$(RC)"
	mysql -u root -p$(root_password) < script_help/reset_database.sql
	
uvicorn:
	@echo "$(GR)#############  Starting the server  #############$(RC)"
	uvicorn main:app --reload --host $(ip_server) --port 8001

service:
	@echo "$(GR)#############  Creating the services  #############$(RC)"
	touch /etc/systemd/system/scaas.service
	echo "[Unit]\nDescription=Gunicorn instance to serve Scaas API\nAfter=network.target\n\n[Service]\nUser=nmap_api\nGroup=www-data\nWorkingDirectory=/opt/scaas-scanner-as-a-service\nEnvironment='PATH=/opt/scaas-scanner-as-a-service/venv/bin'\nExecStart=/opt/scaas-scanner-as-a-service/venv/bin/gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind unix:scaas.sock\n\n[Install]\nWantedBy=multi-user.target" > /etc/systemd/system/scaas.service
	rm -rf /etc/nginx/sites-enabled/default /etc/nginx/sites-available/default
	touch /etc/nginx/sites-available/default
	echo "server {\n        listen 80;\n        server_name $(ip_server);\n\n        location / {\n                include proxy_params;\n                proxy_pass http://unix:/opt/scaas-scanner-as-a-service/scaas.sock;\n        }\n}" > /etc/nginx/sites-available/default
	ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/
	systemctl enable nginx
	systemctl start nginx
	systemctl enable scaas
	systemctl start scaas
