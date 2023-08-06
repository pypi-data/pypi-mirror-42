Inventory of all Widw Area Network links supplied by various Telecom Service Providers. 
For this project  it is assumed that  there was a leagacy monolithic application which used to 
serve the purpose of  these link inventory management  and the  inventory data is alrady available in a 
pre exising  Microsoft SQL  database. 

This microservice will first establish connection with the pre-existing database instead of creating one and 
enable rest api to query the data.  In future it is expected to provide new features in link inventory 
management  and will become independent with its own database. 





install pyodbc   - For configuring ubuntu16.04 to connect to MS SQL server you may follow a detial article here 
https://wordpress.com/post/bhujaykbhatta.wordpress.com/1339  or follow the section below for a summary
===========================

	lsb_release -a
No LSB modules are available.
Distributor ID: Ubuntu
Description:    Ubuntu 16.04.4 LTS
Release:        16.04
Codename:       xenial
============================================

	sudo su 
	curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
	curl https://packages.microsoft.com/config/ubuntu/16.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
	sudo apt-get update
	sudo ACCEPT_EULA=Y apt-get install msodbcsql17
	sudo ACCEPT_EULA=Y apt-get install mssql-tools
	sudo apt-get install unixodbc-dev  freetds-bin  freetds-dev tdsodbc
	exit
	#install pyodbc within virtual environment
	pip install pyodbc 
	pip install mssql-cli
	
	sudo mv /etc/odbcinst.ini  /etc/odbcinst.ini.bak
	
	sudo vi /etc/odbcinst.ini
	
	[FreeTDS]
	Description = v0.91 with protocol v7.2
	Driver = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so
	Setup=/usr/lib/i386-linux-gnu/odbc/libtdsS.so
	FileUsage = 1
	UsageCount = 1
	
	
	sudo vi /etc/freetds/freetds.conf
    
    [global]
        # TDS protocol version
		; tds version = 4.2

        # Whether to write a TDSDUMP file for diagnostic purposes
        # (setting this to /tmp is insecure on a multi-user system)
		; dump file = /tmp/freetds.log
		; debug flags = 0xffff

        # Command and connection timeouts
		; timeout = 10
		; connect timeout = 10

        # If you get out-of-memory errors, it may mean that your client
        # is trying to allocate a huge buffer for a TEXT field.
        # Try setting 'text size' to a more reasonable limit
        text size = 64512
		
		# A typical Sybase server
		[egServer50]
		        host = symachine.domain.com
		        port = 5000
		        tds version = 5.0
		
		# A typical Microsoft server
		[egServer70]
		        host = ntmachine.domain.com
		        port = 1433
		        tds version = 7.0
		# A typical Microsoft server
		[MSSQL]
        host = dbserver
        port = 1433
        tds version = 7.0
    
    
    sudo vi /etc/odbc.ini
    
    [MSSQL]
	Driver = FreeTDS
	ServerName = MSSQL  #  maps it to DSN name not the actual host name 
	Port = 1433
	TDS_Version = 7.2
	    
    
    

Insttall a Microsoft Sql  docker container with persistent volume
	
	sudo docker pull mcr.microsoft.com/mssql/server:2017-latest
	#sudo docker run -e 'ACCEPT_EULA=Y' -e 'SA_PASSWORD=welcome@123'    -p 1433:1433 --name sql1    -d mcr.microsoft.com/mssql/server:2017-latest
  

for data persistance with volume  - 

    sudo docker run -e 'ACCEPT_EULA=Y' -e 'MSSQL_SA_PASSWORD=welcome@123' --name sql1 -p 1433:1433 -v sqlvolume:/var/opt/mssql -d mcr.microsoft.com/mssql/server:2017-latest
    docker volume ls
 
the volume is created at the host level by the docker, even if the container is deleted the volume is persisted
and the next docker run command with -v sqlvolume will mount this existing volume

DRIVER              VOLUME NAME
local               sqlvolume

for data persistence with host directory

    sudo docker run -e 'ACCEPT_EULA=Y' -e 'MSSQL_SA_PASSWORD=welcome@123' -p 1433:1433 -v <host directory>:/var/opt/mssql -d mcr.microsoft.com/mssql/server:2017-latest

    sudo docker exec -it sql1 "bash"
    /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P 'welcome@123
    CREATE DATABASE infooper
    SELECT Name from sys.Databases
    CREATE LOGIN user1  WITH PASSWORD = 'user@1234';
    CREATE USER user1 FOR LOGIN user1;
	GO  

    GRANT ALL PRIVILEGES ON infooper.* TO 'user1'@'localhost';
    GO

From remote computer , pip install mssql-cli  or  https://github.com/dbcli/mssql-cli/blob/master/doc/installation/linux.md#ubuntu-1604 
and run the client commands

    telnet dbserver 1433

    mssql-cli  -S 192.168.111.141 -U SA  -d infooper -P welcome@123
    CREATE TABLE vw_comm_links (serial_no INT  NOT NULL PRIMARY KEY, circuit_id NVARCHAR(50), division_name NVARCHAR(50), fa_end NVARCHAR(50), bandwidth NVARCHAR(50), link_type NVARCHAR(50), )
    INSERT INTO vw_comm_links VALUES (1, 'circuitid1', 'division1', 'faend1', '10MB', 'MPLS' );
    INSERT INTO vw_comm_links VALUES (2, 'circuitid2', 'division2', 'faend2', '5MB', 'PTP' ); 
    INSERT INTO vw_comm_links VALUES (3, 'circuitid3', 'division3', 'faend3', '20MB', 'MPLS' );
    GO
    SELECT * FROM vw_comm_links 
    GO
    QUIT
    
test that  tds  is working

    isql -v MSSQL SA welcome@123
    

install the application  within a virtual environment

       virtualenv -p python3 venv
       source venv/bin/activate
       pip install linkInventory
       
    
The main configuration file nfor the application  is /etc/tokenleader/linvInventory_configs.yml

		sudo vi /etc/tokenleader/linkInventory_configs.yml
		
		host_name: 0.0.0.0 # for docker this should 0.0.0.0
		host_port: 5004
		ssl: disabled # not required other than testing the flaks own ssl. ssl should be handled by apache
		ssl_settings: adhoc
		database:
		  DRIVER: '{FreeTDS}'
		  TDS_Verson: 7.0
		  Server: dbserver
		  Port: 1433
		  Database: infooper
		  UID:  SA
		  db_pwd_key_map: db_pwd
		  engine_connect_string: 'mssql+pyodbc:///odbc_connect={}'
		
		secrets:
		  secrets_file_location: linkInventory/tests/test_data/secrets.yml # where you have write access
		  fernet_key_location: linkInventory/tests/test_data/fernetkeys # where you have write access and preferebly separated from secrets_file_location
		  db_pwd_key_map: db_pwd # when using encrypt-pwd command use this value for --kemap
		  tokenleader_pwd_key_map: tl_pwd
		  
generated an encrypted password for the db 

        encrypt-pwd -k db_pwd -p <your password here>
        

start the service 
           
           linv-start
 	
 	
 
 
	


